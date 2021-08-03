# -*- coding: utf-8 -*-
from .models import RegDataPack
from .redis import getValueFromKey, setValueByKey

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
            setValueByKey(regData.qq_group, entList)
            return {"message": "server logout success!"}
    return {"message": "server not registed!"}