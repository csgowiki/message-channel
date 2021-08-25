# -*- coding: utf-8 -*-
from src.models import RegDataPack
from src.redis_utils import getValueFromKey, setValueByKey, delKey

async def logout_method(regData: RegDataPack):
    _, entList = getValueFromKey(regData.qq_group)
    assert _, 'qq group not registed'
    content_length = len(entList.content)
    for entIdx in range(content_length):
        if (
            entList.content[entIdx].sv_host,
            entList.content[entIdx].sv_port
        ) == (regData.sv_host, regData.sv_port):
            del entList.content[entIdx]
            if len(entList.content) == 0:
                delKey(regData.qq_group)
            else:
                setValueByKey(regData.qq_group, entList)

            return {"message": "server logout success!"}
    return {"message": "server not registed!"}