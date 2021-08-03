# -*- coding: utf-8 -*-

from fastapi import FastAPI, HTTPException

from .register import register_method
from .logout import logout_method
from .models import RegDataPack, TextResponse, JsonResponse

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