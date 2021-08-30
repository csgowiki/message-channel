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
    return True

async def decode_servers_info(servers_info: list) -> str:
    header = "====服务器列表====\n"
    bodys = []
    for servers in servers_info:
        msg = f"服务器编号：{servers['server_id']}\n"
        msg += f"服务器名称：{servers['remark']}\n"
        msg += f"当前地图：{servers['current_map']}\n"
        msg += f"在线：{len(servers['players_info'])}人"
        bodys.append(msg)
    bodys_ = '\n\n'.join(bodys)
    return header + bodys_

async def send_message_to_qq(msgPack: CSGOMessagePack, servers_info: list = []):
    if msgPack.message_type == 0:
        postMsg = f'[{msgPack.sv_remark}] {msgPack.sender}：{msgPack.message}'
    elif msgPack.message_type == 1:
        postMsg = await decode_servers_info(servers_info)
    else:
        raise HTTPException(status_code=400, detail=f"message_type {msgPack.message_type} is not allowed")
    resp = requests.get(f"{__GOCQHTTP_URL__}/send_msg?group_id={msgPack.qq_group}&message={postMsg}")
    assert resp.status_code == 200, f"can't send message to qq; {resp.status_code} is not allowed"

async def send_message_to_csgo(msgPack: QQMessagePack, ent: RedisEntity, token: str):
    soc = socket.socket() # TCP
    soc.connect((ent.sv_host, ent.sv_port))
    senddict = msgPack.dict()
    senddict['auth_token'] = token
    soc.send(ujson.dumps(senddict).encode('utf-8'))
    ret = soc.recv(1024 * 20).decode('utf-8')
    if msgPack.message_type == 0 and ret == 'ok':
        return True, None
    if msgPack.message_type == 1:
        try:
            jsonret = ujson.loads(ret.strip())
            player_len = len(jsonret['players_info'])
            for idx in range(player_len):
                jsonret['players_info'][idx] = zip(
                    ['player_name', 'steamid', 'ping'],
                    jsonret['players_info'][idx]
                )
            return True, jsonret
        except Exception as ept:
            print(f'[Error] send_message_to_csgo: {ept}')
            return False, None
    elif msgPack.message_type == 2 and ret == 'ok':
        return True, None
    return False, None

async def broadcast_from_csgo(msgPack: CSGOMessagePack, token: str):
    assert await valify(msgPack), 'qq group/server is not registed'
    await send_message_to_qq(msgPack)
    # to other csgo-server
    failed_server_list = []
    _, entList = getValueFromKey(msgPack.qq_group)
    for ent in entList.content:
        if (ent.sv_host, ent.sv_port) != (msgPack.sv_host, msgPack.sv_port):
            if not (await send_message_to_csgo(msgPack, token))[0]:
                failed_server_list.append(ent.sv_remark)
    
    if len(failed_server_list) != 0:
        raise HTTPException(status_code=401, detail=f"those server may not recieve message: {str(failed_server_list)}")

    return {"message": "message send success!"}

async def broadcast_from_qq(msgPack: QQMessagePack, token: str):
    assert await valify_qq(msgPack), 'qq group/server is not registed'
    # preprocess server info
    if msgPack.message_type == 1:
        _, servers_info = await get_server_info(msgPack.qq_group, token, msgPack.server_id)
        if not _:
            raise HTTPException(status_code=401, detail=f"those server may not recieve message: {str(servers_info)}")
        await send_message_to_qq(msgPack, servers_info)
        return {'message': 'message send success!'}
    #########################

    failed_server_list = []
    success_server_list = []
    _, entList = getValueFromKey(msgPack.qq_group)
    if msgPack.server_id == -1:
        for ent in entList.content:
            if not (await send_message_to_csgo(msgPack, ent, token))[0]:
                failed_server_list.append(ent.sv_remark)
            else:
                success_server_list.append(ent.sv_remark)
    else:
        await send_message_to_csgo(msgPack, entList.content[msgPack.server_id], token)
    
    if len(failed_server_list) != 0:
        raise HTTPException(status_code=401, detail=f"those server may not recieve message: {str(failed_server_list)}")

    if len(success_server_list) == 0:
        return {"message": "message is send to no server"}
    return {"message": "message send success!"}

async def get_server_info(qqgroup: int, token:str, server_id: int = -1):
    _, entList = getValueFromKey(qqgroup)
    assert _ and len(entList.content) > server_id and isinstance(server_id, int) and server_id >= -1, 'qq group/server is not registed'
    msgPack = QQMessagePack(
        **{
            'server_id': server_id,
            'qq_group': qqgroup,
            'qq_group_name': 'unknown',
            'sender': 'unknown',
            'message_type': 1,
            'message': 'unknown'
        }
    )
    failed_server_list = []
    servers_info = []
    if server_id == -1:
        for ent_idx in range(len(entList.content)):
            _, server_info = await send_message_to_csgo(msgPack, entList.content[ent_idx], token)
            if _:
                server_info['server_id'] = ent_idx
                server_info['remark'] = entList.content[ent_idx].sv_remark
                servers_info.append(server_info)
            else:
                print(f'[Error] server info failed: <{entList.content[ent_idx].sv_remark}>')
                failed_server_list.append(entList.content[ent_idx].sv_remark)
    else:
        _, server_info = await send_message_to_csgo(msgPack, entList.content[msgPack.server_id], token)
        if _:
            server_info['server_id'] = server_id
            server_info['remark'] = entList.content[server_id].sv_remark
            servers_info.append(server_info)
        else:
            failed_server_list.append(entList.content[server_id].sv_remark)
    
    if len(failed_server_list) != 0:
        return False, failed_server_list
    return True, servers_info