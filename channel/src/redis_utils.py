# -*- coding: utf-8 -*-

from typing import List, Tuple
import redis
import ujson

from src.models import RedisEntity, RedisEntityList, RegDataPack

__PREFIX__ = '[message-channel]'

gRedis = redis.Redis(host='mc-redis', port=6379, decode_responses=True)

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
    def cmp(ent: RedisEntity):
        return (ent['sv_host'], ent['sv_port'])
    contentList = value.dict()['content']
    contentList.sort(key=cmp)
    ret = gRedis.set(__construct_rediskey_from_intkey(qq_key), ujson.dumps(contentList))
    return ret

def delKey(qq_key: int) -> bool:
    ret = gRedis.delete(__construct_rediskey_from_intkey(qq_key))
    return ret