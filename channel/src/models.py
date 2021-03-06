# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Union
from pydantic import BaseModel

class TextResponse(BaseModel):
    message: str

class JsonResponse(BaseModel):
    message: str
    results: Union[Dict, List]

class RegDataPack(BaseModel):
    sv_host: str
    sv_port: int
    qq_group: int
    sv_remark: Optional[str] = "unknown"

class RedisEntity(BaseModel):
    sv_host: str
    sv_port: int
    sv_remark: str
    timestamp: float

class RedisEntityList(BaseModel):
    content: List[Optional[RedisEntity]]

class CSGOMessagePack(BaseModel):
    sv_host: str
    sv_port: int
    qq_group: int
    sv_remark: str
    sender: str
    message_type: int
    message: str

class QQMessagePack(BaseModel):
    server_id: Optional[int] = -1
    qq_group: int
    qq_group_name: str
    sender: str
    message_type: int
    message: str
