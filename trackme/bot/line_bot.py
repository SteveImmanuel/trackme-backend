import re
import pytz
import trackme.database.redis as redis_repository

from flask import Request
from typing import cast
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage, Source, LocationSendMessage
from bson.objectid import ObjectId
from trackme.contants import *
from trackme.database.mongo.collections import Users
from trackme.exceptions.bot_message_exception import BotMessageException
from trackme.validation.add_bot_channel import AddBotChannel
from trackme.validation.delete_bot_channel import DeleteBotChannel
from trackme.database.influx.location_repository import LocationRepository
from trackme.models.location import Location
from trackme.helper.location import *

# initialize connector
api = LineBotApi(LINE_BOT_ACCESS_TOKEN)
handler = WebhookHandler(LINE_BOT_CHANNEL_SECRET)
user_collection = Users()
location_repo = LocationRepository()


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

        if keyword == '/register':
            register_channel(rest_msg, event)
        elif keyword == '/unregister':
            unregister_channel(rest_msg, event)
        elif keyword == '/track':
            track_location(rest_msg, event)
    except BotMessageException as e:
        api.reply_message(event.reply_token, TextSendMessage(text=str(e)))
    except Exception as e:
        print(e)
        api.reply_message(
            event.reply_token,
            TextSendMessage(text=str('There is trouble with the server. Please try again later')))


def register_channel(bot_token: str, event: MessageEvent):
    bot_token = bot_token.lstrip().split(' ')
    if len(bot_token) != 1:
        raise BotMessageException('Usage: /register <token>')

    bot_token = bot_token[0]
    uid = redis_repository.get_key(f'bot_token_{bot_token}')
    if uid is None:
        raise BotMessageException(
            'Token expired or not found. Please re-generate the token from the app')

    source = cast(Source, event.source)
    if source.type == 'user':
        profile_info = api.get_profile(source.sender_id)
        display_name = profile_info.display_name
        photo_url = profile_info.picture_url
    elif source.type == 'group':
        profile_info = api.get_group_summary(source.sender_id)
        display_name = profile_info.group_name
        photo_url = profile_info.picture_url
    else:
        raise BotMessageException('This channel is not supported. Bot only supports user or group')

    update_data = AddBotChannel.validate({
        'id': source.sender_id,
        'type': source.type.capitalize(),
        'display_name': display_name,
        'photo_url': photo_url
    })
    result = user_collection.update_one({'_id': ObjectId(uid)}, {
        '$addToSet': {
            'bot_channels': update_data,
        },
    })
    if result.get('total_matched') != 1:
        raise BotMessageException(
            'There is problem a problem in registering user. Please try again')

    user = user_collection.find_one({'_id': ObjectId(uid)})
    api.reply_message(event.reply_token,
                      TextSendMessage(text=f'Registration successful for tracking {user.username}'))


def unregister_channel(bot_token: str, event: MessageEvent):
    bot_token = bot_token.lstrip().split(' ')
    if len(bot_token) != 1:
        raise BotMessageException('Usage: /unregister <token>')

    bot_token = bot_token[0]
    uid = redis_repository.get_key(f'bot_token_{bot_token}')
    if uid is None:
        raise BotMessageException(
            'Token expired or not found. Please re-generate the token from the app')

    source = cast(Source, event.source)
    delete_data = DeleteBotChannel.validate({'id': source.sender_id})

    result = user_collection.update_one({'_id': ObjectId(uid)}, {
        '$pull': {
            'bot_channels': delete_data,
        },
    })
    if result.get('total_matched') != 1:
        raise BotMessageException(
            'There is problem a problem in unregistering user. Please try again')

    user = user_collection.find_one({'_id': ObjectId(uid)})
    api.reply_message(event.reply_token,
                      TextSendMessage(text=f'Unregistration successful for user {user.username}'))


def track_location(alias: str, event: MessageEvent):
    alias = alias.lstrip().split(' ')
    if len(alias) != 1:
        raise BotMessageException('Usage: /track <alias>')

    alias = alias[0]
    source = cast(Source, event.source)

    user = user_collection.find_one({
        '$and': [
            {
                '$or': [
                    {
                        'alias': alias
                    },
                    {
                        'username': alias
                    },
                ]
            },
            {
                'bot_channels.channel_id': source.sender_id
            },
        ]
    })

    if user is None:
        raise BotMessageException('Alias not found')

    result = get_location_cache(user.uid)
    if result is None:
        data = {'uid': user.uid, 'start': '-1w'}
        result = location_repo.find_latest_one(data)
        result.timestamp = result.timestamp.astimezone(pytz.timezone(TIMEZONE))
        result.timestamp = result.timestamp.strftime('%a, %d %b %I:%M %p')
        result = result.to_dict()
        set_location_cache(result)

    if result is None:
        raise BotMessageException(f'Location log of {alias} not found within one week')

    api.reply_message(
        event.reply_token,
        LocationSendMessage(title=f'{alias}\'s last known location',
                            address=result.get('timestamp'),
                            latitude=result.get('latitude'),
                            longitude=result.get('longitude')))


def push_location_msg(channel_id: str, location: Location):
    pass
