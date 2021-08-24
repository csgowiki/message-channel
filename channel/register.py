# -*- coding: utf-8 -*-
import time

from models import RedisEntity, RegDataPack
from redis_utils import getValueFromKey, setValueByKey

async def register_method(regData: RegDataPack):
    _, entList = getValueFromKey(regData.qq_group)
    for ent in entList.content:
        if (ent.sv_host, ent.sv_port) == (regData.sv_host, regData.sv_port):
            # modify sv_remark & timestamp
            ent.sv_remark = regData.sv_remark
            ent.timestamp = time.time()
            setValueByKey(regData.qq_group, entList)
            return {"message": "server message existed, update timestamp & sv_remark"}

    entList.content.append(RedisEntity(
        sv_host=regData.sv_host,
        sv_port=regData.sv_port,
        sv_remark=regData.sv_remark,
        timestamp=time.time()
    ))
    setValueByKey(regData.qq_group, entList)
    return {"message": "server register success!"}