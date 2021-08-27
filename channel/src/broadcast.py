# -*- coding: utf-8 -*-
import socket
import requests
import ujson
from src.models import CSGOMessagePack, QQMessagePack, RedisEntity
from src.redis_utils import getValueFromKey
from fastapi import HTTPException

__GOCQHTTP_URL__ = "http://mc-gocq:9091"

socket.setdefaulttimeout(1.0)

async def valify(msgPack: CSGOMessagePack) -> bool:
    _, entList = getValueFromKey(msgPack.qq_group)
    for ent in entList.content:
        if (ent.sv_host, ent.sv_port) == (msgPack.sv_host, msgPack.sv_port):
            return True
    return False

async def valify_qq(msgPack: QQMessagePack) -> bool:
    _, entList = getValueFromKey(msgPack.qq_group)
    if not _: return False
    if msgPack.server_id == -1: return True
    if msgPack.server_id < -1: return False
    if len(entList.content) <= msgPack.server_id: return False

async def send_message_to_qq(msgPack: CSGOMessagePack):
    postMsg = f'[{msgPack.sv_remark}] {msgPack.sender}：{msgPack.message}'
    resp = requests.get(f"{__GOCQHTTP_URL__}/send_msg?group_id={msgPack.qq_group}&message={postMsg}")
    assert resp.status_code == 200, f"can't send message to qq; {resp.status_code} is not allowed"

async def send_message_to_csgo(msgPack: QQMessagePack, ent: RedisEntity):
    # soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc = socket.socket() # TCP
    soc.connect((ent.sv_host, ent.sv_port))
    # soc.sendto(ujson.dumps(msgPack.dict()).encode('utf-8'), (msgPack.sv_host, msgPack.sv_port))
    soc.send(ujson.dumps(msgPack.dict()).encode('utf-8'))
    ret = soc.recv(102400).decode('utf-8')
    if msgPack.message_type == 0 and ret == 'ok':
        return True
    if msgPack.message_type == 1:
        try:
            jsonret = ujson.loads(ret)
            return True, jsonret
        except Exception as ept:
            return False
    return False

async def broadcast_from_csgo(msgPack: CSGOMessagePack):
    assert await valify(msgPack), 'qq group/server is not registed'
    await send_message_to_qq(msgPack)
    # to other csgo-server
    failed_server_list = []
    _, entList = getValueFromKey(msgPack.qq_group)
    for ent in entList.content:
        if (ent.sv_host, ent.sv_port) != (msgPack.sv_host, msgPack.sv_port):
            if not await send_message_to_csgo(msgPack):
                failed_server_list.append(ent.sv_remark)
    
    if len(failed_server_list) != 0:
        raise HTTPException(status_code=401, detail=f"those server may not recieve message: {str(failed_server_list)}")

    return {"message": "message send success!"}

async def broadcast_from_qq(msgPack: QQMessagePack):
    assert await valify_qq(msgPack), 'qq group/server is not registed'
    failed_server_list = []
    success_server_list = []
    _, entList = getValueFromKey(msgPack.qq_group)
    if msgPack.server_id == -1:
        for ent in entList.content:
            if not await send_message_to_csgo(msgPack, ent):
                failed_server_list.append(ent.sv_remark)
            else:
                success_server_list.append(ent.sv_remark)
    else:
        await send_message_to_csgo(msgPack, entList.content[msgPack.server_id])
    
    if len(failed_server_list) != 0:
        raise HTTPException(status_code=401, detail=f"those server may not recieve message: {str(failed_server_list)}")

    if len(success_server_list) == 0:
        return {"message": "message is send to no server"}
    return {"message": "message send success!"}