import json
from aiocqhttp import message
import requests
import aiocqhttp
from nonebot import get_bot, on_notice, NoticeSession
from .. import config

bot = get_bot()

async def parseCommand(messages: aiocqhttp.message.Message) -> dict:
    '''
    {
        'success': <bool>,      # 是否解析成功
        'command_type': <int>,  # 0 转发，1 状态，2 执行
        'server_id': <int>,     # 服务器编号，-1为全部服务器
        'content': <str>        # 内容
    }
    '''
    retjson = {'success': False}
    # --- parse trigger ---
    if len(messages) == 0 or messages[0]['type'] != 'text':
        return retjson
    if len(config.COMMAND_TRIGGER) != 0 and messages[0]['data']['text'][0] not in config.COMMAND_TRIGGER:
        return retjson
    if len(config.COMMAND_TRIGGER) != 0:
        messages[0]['data']['text'] = messages[0]['data']['text'][1:]  # trim 1st char
    # --- parse server id ---
    firstMessages = messages[0]['data']['text'][1:].split(' ')
    if len(firstMessages) <= 1:
        return retjson
    if len(firstMessages[0]) == 0: # 未指定server id
        retjson['server_id'] = -1
    else:
        retjson['server_id'] = int(firstMessages[0])
    # --- parse command ---
    idx = 1
    for x in range(1, len(firstMessages)):
        if len(firstMessages[x]) != 0:
            idx = x
            break
    if firstMessages[idx] == '状态':
        retjson['command_type'] = 1
        retjson['success'] = True
        return retjson
    elif firstMessages[idx] == '执行':
        retjson['command_type'] = 2
        idx += 1
    elif firstMessages[idx] == '转发':
        retjson['command_type'] = 0
        idx += 1
    else:
        retjson['command_type'] = 0

    # --- parse content ---
    retjson['content'] = ''
    if idx < len(firstMessages):
        retjson['content'] = ' '.join(firstMessages[idx:])
    
    for msg in messages[1:]:
        if msg['type'] == 'image':
            retjson['content'] += '[图片]'
        elif msg['type'] == 'face':
            retjson['content'] += '[表情]'
        elif msg['type'] == 'text':
            retjson['content'] += msg['data']['text']
        else:
            retjson['content'] = '[其他]'

    retjson['success'] = True
    return retjson

@on_notice('notify')
async def poke(session: NoticeSession):
    if (session.event.sub_type == 'poke' and session.event.target_id == (await bot.get_login_info())['user_id']):
        if not session.event.group_id: return
        # group_info = bot.get_group_info(group_id=session.event.group_id)
        # data = {
        #     'qq_group': group_info['group_id'],
        #     'qq_group_name': group_info['group_name'],
        #     'server_num': -1,
        #     'sender': 'None',
        #     'message': '',
        #     'message_type': 1
        # }
        # url = f'http://mc-core:8000/api/broadcast_from_qq?token={config.ACCESS_TOKEN}'
        # resp = requests.post(url, data=data)
        # if resp.status_code == 200:
        #     await bot.send_group_msg 


@bot.on_message('group')
async def trigger(event: aiocqhttp.Event):
    try:
        mc_command = await parseCommand(event.message)
        if not mc_command['success']: return
    except Exception as ept:
        print(f'[Error] {ept}')
        return
    # 执行 权限
    if mc_command['command_type'] == 2 and event.sender['user_id'] not in config.SUPERUSERS:
        await bot.send_group_msg(
            group_id=event.group_id,
            message=message.MessageSegment.at(event.sender['user_id']) + "你没有权限使用该指令" + message.MessageSegment.face(28)
        )
        return
