# -*- coding: utf-8 -*-

from typing import List, Tuple
import redis
import ujson

from .models import RedisEntity, RedisEntityList, RegDataPack

__PREFIX__ = 'csgowiki-message-channel'

gRedis = redis.Redis(host='localhost', port=6379, decode_responses=True)

def __construct_rediskey_from_intkey(intkey: int):
    return f'{__PREFIX__}{intkey}'

def getAllKeys() -> List[int]:
    keys = gRedis.keys()
    keys = filter(lambda x: x.startswith(__PREFIX__), keys)
    keys = list(map(lambda x: int(x.strip(__PREFIX__)), keys))
    return keys

def getValueFromKey(qq_key: int) -> Tuple[bool, RedisEntityList]:
    redis_value = gRedis.get(__construct_rediskey_from_intkey(qq_key))
    if not redis_value:
        return False, RedisEntityList(**{'content': []})
    return True, RedisEntityList(**{'content': ujson.loads(redis_value)})

def setValueByKey(qq_key: int, value: RedisEntityList) -> bool:
    ret = gRedis.set(f'{__PREFIX__}{qq_key}', ujson.dumps(value.dict()['content']))
    return ret