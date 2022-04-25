from flask import Request
from typing import cast
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage, Source, LocationSendMessage
from bson.objectid import ObjectId
from trackme.contants import *
import trackme.database.redis as redis_repository
from trackme.helper.line_bot import *
from trackme.database.mongo.collections import Users
from trackme.exceptions.bot_message_exception import BotMessageException
from trackme.validation.add_linked_account import AddLinkedAccount
from trackme.validation.add_bot_channel import AddBotChannel
from trackme.helper.location import *

PLATFORM = 'line'

# initialize connector
api = LineBotApi(LINE_BOT_ACCESS_TOKEN)
handler = WebhookHandler(LINE_BOT_CHANNEL_SECRET)
user_collection = Users()


def process_webhook(request: Request):
    signature = request.headers.get('X-Line-Signature')
    data = request.get_data(as_text=True)
    handler.handle(data, signature)


@handler.add(MessageEvent, message=TextMessage)
def echo(event: MessageEvent) -> None:
    try:
        message = cast(TextMessage, event.message)
        msg_arr = message.text.split(' ')
        keyword = msg_arr[0]
        rest_msg = ' '.join(msg_arr[1:])

        if keyword == '/me':
            register_user(rest_msg, event)
        elif keyword == '/register':
            register_channel(rest_msg, event)
        elif keyword == '/track':
            track_location(rest_msg, event)
        else:
            handle_indirect_mention(message.text, event)
    except BotMessageException as e:
        api.reply_message(event.reply_token, TextSendMessage(text=str(e)))
    except Exception as e:
        print(e)
        api.reply_message(
            event.reply_token,
            TextSendMessage(text=str('There is trouble with the server. Please try again later')))


def register_user(bot_token: str, event: MessageEvent):
    bot_token = bot_token.strip().split(' ')
    if len(bot_token) != 1:
        raise BotMessageException('Usage: /me <token>')

    bot_token = bot_token[0]
    uid = redis_repository.get_key(f'user_token_{bot_token}')
    if uid is None:
        raise BotMessageException(
            'Token expired or not found. Please re-generate the token from the app')

    source = cast(Source, event.source)
    if source.type != 'user':
        raise BotMessageException(
            'User registration can only be done by sending direct message to bot')

    profile_info = get_user_info(api, source.sender_id)
    update_data = AddLinkedAccount.validate({
        'id': source.sender_id,
        'display_name': profile_info.get('display_name'),
        'photo_url': profile_info.get('photo_url'),
        'platform': PLATFORM
    })
    result = user_collection.update_one({'_id': ObjectId(uid)}, {
        '$addToSet': {
            'linked_accounts': update_data,
        },
    })
    if result.get('total_matched') != 1:
        raise BotMessageException(
            'There is problem a problem in registering user. Please try again')

    user = user_collection.find_by_id(uid)
    api.reply_message(
        event.reply_token,
        TextSendMessage(text=f'Registration successful for linking account {user.username}'),
    )


def register_channel(bot_token: str, event: MessageEvent):
    bot_token = bot_token.strip().split(' ')
    if len(bot_token) != 1:
        raise BotMessageException('Usage: /register <token>')

    bot_token = bot_token[0]
    uid = redis_repository.get_key(f'channel_token_{bot_token}')
    if uid is None:
        raise BotMessageException(
            'Token expired or not found. Please re-generate the token from the app')

    source = cast(Source, event.source)
    if source.type == 'user':
        profile_info = get_user_info(api, source.sender_id)
    elif source.type == 'group':
        profile_info = get_group_info(api, source.group_id)
    else:
        raise BotMessageException('This channel is not supported. Bot only supports user or group')

    update_data = AddBotChannel.validate({
        'id': source.sender_id,
        'type': source.type.capitalize(),
        'display_name': profile_info.get('display_name'),
        'photo_url': profile_info.get('photo_url'),
        'platform': PLATFORM,
        'indirect_mention_notif': False
    })
    result = user_collection.update_one({'_id': ObjectId(uid)}, {
        '$addToSet': {
            'bot_channels': update_data,
        },
    })
    if result.get('total_matched') != 1:
        raise BotMessageException(
            'There is problem a problem in registering channel. Please try again')

    user = user_collection.find_by_id(uid)
    api.reply_message(
        event.reply_token,
        TextSendMessage(text=f'Registration successful for tracking {user.username}'),
    )


def track_location(alias: str, event: MessageEvent):
    alias = alias.strip().split(' ')
    if len(alias) != 1:
        raise BotMessageException('Usage: /track <alias>')

    alias = alias[0]
    source = cast(Source, event.source)
    user = user_collection.find_one({
        '$and': [
            {
                '$or': [
                    {
                        'aliases': alias
                    },
                    {
                        'username': alias
                    },
                ]
            },
            {
                'bot_channels.id': source.sender_id
            },
        ]
    })

    if user is None:
        raise BotMessageException(
            'Alias not found or you don\'t have permission to track that user')

    result = get_last_location(user.uid)

    if result is None:
        raise BotMessageException(f'Location log of {alias} not found within one week')

    closest_location = get_closest_highlight_location(
        result.get('latitude'),
        result.get('longitude'),
        user.locations,
    )

    msg = f'{alias}\'s last known location'
    if closest_location is not None:
        location_name = closest_location.get('name')
        msg = f'{alias} is at {location_name}'

    api.reply_message(
        event.reply_token,
        LocationSendMessage(
            title=msg,
            address=result.get('timestamp'),
            latitude=result.get('latitude'),
            longitude=result.get('longitude'),
        ),
    )


def push_location_msg(username: str, channel_ids: List[str], location_name: str, is_leaving: bool):
    verb = 'arrived at'
    if is_leaving:
        verb = 'left'

    for id in channel_ids:
        api.push_message(id, TextSendMessage(text=f'{username} has {verb} {location_name}'))


def push_low_battery_alert(username: str, channel_ids: List[str]):
    for id in channel_ids:
        api.push_message(
            id,
            TextSendMessage(
                text=
                f'{username} has low battery, so he/she might not be able to respond to any messages',
            ),
        )


def handle_indirect_mention(whole_text: str, event: MessageEvent):
    source = cast(Source, event.source)
    if source.type != 'group':
        return

    users = user_collection.find_all({
        'bot_channels.id': source.sender_id,
        'bot_channels.indirect_mention_notif': True,
    })

    if len(users) > 0:
        sender_name = get_group_member_info(
            api,
            source.group_id,
            source.user_id,
        ).get('display_name')
        group_name = get_group_info(api, source.group_id).get('display_name')
        msg = f'{sender_name} mentioned you in {group_name}:\n\n{whole_text}'

        for user in users:
            possible_aliases = user.aliases + [user.username]
            if any(alias in whole_text for alias in possible_aliases):
                line_account = list(
                    filter(
                        lambda item: item.get('platform') == PLATFORM,
                        user.linked_accounts,
                    ))

                if len(line_account) == 1:
                    api.push_message(line_account[0].get('id'), TextSendMessage(text=msg))
