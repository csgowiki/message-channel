# -*- coding: utf-8 -*-
import time

from .models import RedisEntity, RegDataPack
from .redis import getAllKeys, getValueFromKey, setValueByKey

def logout_method(regData: RegDataPack):
    return {"message": "server logout success!"}