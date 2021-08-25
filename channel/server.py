# -*- coding: utf-8 -*-

from typing import Text
import requests
from fastapi import FastAPI, HTTPException

from src.register import register_method
from src.logout import logout_method
from src.models import RegDataPack, TextResponse, JsonResponse, MessagePack

message_channel = FastAPI()

@message_channel.post("/api/register", response_model=TextResponse)
async def register(regData: RegDataPack):
    try:
        return await register_method(regData)
    except Exception as ept:
        raise HTTPException(status_code=400, detail=f"server register failed: [{ept}]")

@message_channel.delete("/api/logout", response_model=TextResponse)
async def logout(regData: RegDataPack):
    try:
        return await logout_method(regData)
    except Exception as ept:
        raise HTTPException(status_code=400, detail=f"server logout failed: [{ept}]")

@message_channel.post("/api/broadcast", response_model=TextResponse)
async def broadcast():# to all
    return {"message": "message broadcasted!"}

@message_channel.post("/api/to_qq", response_model=TextResponse)
async def message_to_qq(msgPack: MessagePack):
    try:
        resp = requests.get(f"http://mc-gocq:9091/send_msg?user_id=765892480&message=test")
        assert resp.status_code == 200, f"{resp.status_code} not allowed"
        return {"message": "message send success!"}
    except Exception as ept:
        raise HTTPException(status_code=400, detail=f"send message error: [{ept}]")