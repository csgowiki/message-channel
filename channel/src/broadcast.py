# -*- coding: utf-8 -*-
import requests
from src.models import MessagePack
from src.redis_utils import getValueFromKey

__GOCQHTTP_URL__ = "http://mc-gocq:9091"

def valify(msgPack: MessagePack) -> bool:
    _, entList = getValueFromKey(msgPack.qq_group)
    for ent in entList.content:
        if (ent.sv_host, ent.sv_port) == (msgPack.sv_host, msgPack.sv_port):
            return True
    return False

def send_message_to_qq(msgPack: MessagePack):
    postMsg = f'[{msgPack.sv_remark}] {msgPack.sender}：{msgPack.message}'
    resp = requests.get(f"{__GOCQHTTP_URL__}/send_msg?group_id={msgPack.qq_group}&message={postMsg}")
    assert resp.status_code == 200, f"can't send message to qq; {resp.status_code} is not allowed"

def send_message_to_csgo(msgPack: MessagePack):
    pass

async def broadcast_from_csgo(msgPack: MessagePack):
    assert valify(msgPack), 'qq group not registed'
    send_message_to_qq(msgPack)
    # to other csgo-server
    _, entList = getValueFromKey(msgPack.qq_group)
    for ent in entList.content:
        if (ent.sv_host, ent.sv_port) != (msgPack.sv_host, msgPack.sv_port):
            send_message_to_csgo(msgPack)

    return {"message": "message send success!"}