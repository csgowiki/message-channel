# -*- coding: utf-8 -*-
import os, yaml
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.register import register_method
from src.logout import logout_method
from src.broadcast import broadcast_from_csgo, broadcast_from_qq, get_server_info
from src.models import RegDataPack, TextResponse, JsonResponse, CSGOMessagePack, QQMessagePack

config_dir = '/var/lib/message-channel'

message_channel = FastAPI()

message_channel.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.path.exists(os.path.join(config_dir, 'core.yml')):
    with open('/var/lib/message-channel/core.yml', 'r', encoding='utf-8') as iFile:
        config = yaml.safe_load(iFile)
else:
    config = {
        'access_token': '123456'
    }

async def verify_token(token: str):
    assert token == config.get('access_token'), 'token invalid'

@message_channel.post("/api/register", response_model=TextResponse)
async def register(regData: RegDataPack, token: str):
    try:
        await verify_token(token)
        return await register_method(regData)
    except Exception as ept:
        raise HTTPException(status_code=400, detail=f"server register failed: [{ept}]")

@message_channel.post("/api/logout", response_model=TextResponse)
async def logout(regData: RegDataPack, token: str):
    try:
        await verify_token(token)
        return await logout_method(regData)
    except Exception as ept:
        raise HTTPException(status_code=400, detail=f"server logout failed: [{ept}]")

@message_channel.post("/api/broadcast", response_model=TextResponse)
async def broadcast():# to all
    return {"message": "message broadcasted!"}

@message_channel.post("/api/broadcast_from_csgo", response_model=TextResponse)
async def broadcast_csgo(msgPack: CSGOMessagePack, token: str):
    try:
        await verify_token(token)
        return await broadcast_from_csgo(msgPack, token)
    except Exception as ept:
        raise HTTPException(status_code=400, detail=f"send message error: [{ept}]")

@message_channel.post("/api/broadcast_from_qq", response_model=TextResponse)
async def broadcast_qq(msgPack: QQMessagePack, token: str):
    try:
        await verify_token(token)
        return await broadcast_from_qq(msgPack, token)
    except Exception as ept:
        raise HTTPException(status_code=400, detail=f"send message error: [{ept}]")

@message_channel.get("/api/server_info", response_model=JsonResponse)
async def server_info(qq_group: int, server_id: int=-1):
    try:
        token = config.get('access_token')
        await verify_token(token)
        _, servers_info = await get_server_info(qq_group, token, server_id)
        if not _:
            raise HTTPException(status_code=401, detail=f"those server may not recieve message: {str(servers_info)}")
        return {'message': 'send message success!', 'results': servers_info}
    except Exception as ept:
        raise HTTPException(status_code=400, detail=f"send message error: [{ept}]")

if __name__ == '__main__':
    keyfile_path = os.path.join(config_dir, 'private.key')
    certfile_path = os.path.join(config_dir, 'fullchain.crt')
    if os.path.exists(keyfile_path) and os.path.exists(certfile_path):
        uvicorn.run(
            message_channel,
            host="0.0.0.0",
            port=8000,
            ssl_keyfile=keyfile_path,
            ssl_certfile=certfile_path
        )
    else:
        uvicorn.run(message_channel, host="0.0.0.0", port=8000)