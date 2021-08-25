# -*- coding: utf-8 -*-
import os, yaml
from fastapi import FastAPI, HTTPException

from src.register import register_method
from src.logout import logout_method
from src.broadcast import broadcast_from_csgo, broadcast_from_qq
from src.models import RegDataPack, TextResponse, JsonResponse, MessagePack

message_channel = FastAPI()

if os.path.exists('config.yml'):
    with open('config.yml', 'r', encoding='utf-8') as iFile:
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

@message_channel.delete("/api/logout", response_model=TextResponse)
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
async def broadcast_csgo(msgPack: MessagePack, token: str):
    try:
        await verify_token(token)
        return await broadcast_from_csgo(msgPack)
    except Exception as ept:
        raise HTTPException(status_code=400, detail=f"send message error: [{ept}]")

@message_channel.post("/api/broadcast_from_qq", response_model=TextResponse)
async def broadcast_qq(msgPack: MessagePack, token: str):
    try:
        await verify_token(token)
        return await broadcast_from_qq(msgPack)
    except Exception as ept:
        raise HTTPException(status_code=400, detail=f"send message error: [{ept}]")