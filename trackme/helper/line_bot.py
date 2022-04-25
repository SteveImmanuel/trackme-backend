from typing import Dict
from linebot import LineBotApi
from linebot.models.responses import Group, Profile
import trackme.database.redis as redis_repository


def set_info_cache(hash_key: str, data: Dict):
    for key, value in data.items():
        redis_repository.hset_key(hash_key, key, value)


def get_info_cache(hash_key: str):
    attrib_key = ['display_name', 'photo_url']
    result = {}
    for key in attrib_key:
        result[key] = redis_repository.hget_key(hash_key, key)
    return result


def get_group_info(api: LineBotApi, group_id: str) -> Dict:
    hash_key = 'group_info_' + group_id
    result = {}

    if not redis_repository.is_key_exist(hash_key):
        try:
            info = api.get_group_summary(group_id)
            result = {
                'display_name': info.group_name,
                'photo_url': info.picture_url,
            }
            set_info_cache(hash_key, result)
            return result
        except:
            result = {
                'display_name': 'Group',
                'photo_url': '',
            }

        return result

    return get_info_cache(hash_key)


def get_user_info(api: LineBotApi, user_id: str) -> Dict:
    hash_key = 'user_info_' + user_id
    result = {}

    if not redis_repository.is_key_exist(hash_key):
        try:
            info = api.get_profile(user_id)
            result = {
                'display_name': info.display_name,
                'photo_url': info.picture_url,
            }
            set_info_cache(hash_key, result)
        except:
            result = {
                'display_name': 'Someone',
                'photo_url': '',
            }

        return result

    return get_info_cache(hash_key)


def get_group_member_info(api: LineBotApi, group_id: str, user_id: str) -> Dict:
    hash_key = 'user_info_' + user_id
    result = {}

    if not redis_repository.is_key_exist(hash_key):
        try:
            info = api.get_group_member_profile(group_id, user_id)
            result = {
                'display_name': info.display_name,
                'photo_url': info.picture_url,
            }
            set_info_cache(hash_key, result)
        except:
            result = {
                'display_name': 'Someone',
                'photo_url': '',
            }

        return result

    return get_info_cache(hash_key)