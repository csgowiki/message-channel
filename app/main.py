# -*- coding: utf-8 -*-

from fastapi import FastAPI, HTTPException

from .register import register_method
from .models import RegDataPack, TextResponse, JsonResponse

message_channel = FastAPI()

@message_channel.post("/api/register", response_model=TextResponse)
async def register(datapack: RegDataPack):
    try:
        return await register_method(datapack)
    except Exception as ept:
        raise HTTPException(status_code=400, detail=f"server register failed: [{ept}]")