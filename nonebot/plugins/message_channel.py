import os
from aiocqhttp import message
import requests
import aiocqhttp
from nonebot import get_bot, on_notice, NoticeSession, on_websocket_connect

import sys
sys.path.append('/var/lib/message-channel')
try:
    import nonebot_config as config
except:
    import nonebot.default_config as config

config_dir = '/var/lib/message-channel'
message_channel_host = 'http://mc-core:8000'

bot = get_bot()

bot_user_id = 0 # Bot的QQ号，会自动获取

@on_websocket_connect
async def connect(event: aiocqhttp.Event):
    global bot_user_id, message_channel_host
    bot_user_id =  (await bot.get_login_info())['user_id']
    keyfile_path = os.path.join(config_dir, 'private.key')
    certfile_path = os.path.join(config_dir, 'fullchain.crt')
    if os.path.exists(keyfile_path) and os.path.exists(certfile_path):
        message_channel_host = 'https://mc-core:8000'

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
    firstMessages = messages[0]['data']['text'].split(' ')
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
        retjson['content'] = ''
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
    if session.event.sub_type == 'poke' and session.event.target_id == bot_user_id:
        if not session.event.group_id: return
        group_info = await bot.get_group_info(group_id=session.event.group_id)
        data = {
            'qq_group': group_info['group_id'],
            'qq_group_name': group_info['group_name'],
            'server_id': -1,
            'sender': 'None',
            'message': '',
            'message_type': 1
        }
        url = f'{message_channel_host}/api/broadcast_from_qq?token={config.MC_ACCESS_TOKEN}'
        resp = requests.post(url, json=data, headers={"Content-Type": "application/json"}, verify=False)
        if resp.status_code != 200:
            if config.COMMAND_FAILED_NOTICE:
            # 检查Bot是否是管理员或群主
                botinfo = await bot.get_group_member_info(group_id=session.event.group_id, user_id=bot_user_id)
                if botinfo['role'] in ['owner', 'admin']:
                    await bot.send_private_msg(
                        user_id=session.event.sender_id,
                        group_id=session.event.group_id,
                        message=message.MessageSegment.face(36) + f'消息发送出现错误：{resp.content.decode("utf-8")}'
                    )
                else:
                    print(f'[ERROR] 消息发送出现异常，但是Bot不是QQ群管理员，无法私聊发送者报错内容：{resp.content.decode("utf-8")}')


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
        # STAFFS ?
        auth_server = config.STAFFS.get(str(event.sender['user_id']))
        if (not auth_server) or (isinstance(auth_server, list) and mc_command['server_id'] not in auth_server):
            await bot.send_group_msg(
                group_id=event.group_id,
                message=message.MessageSegment.reply(event.message_id) + "你没有权限使用该指令" + message.MessageSegment.face(28)
            )
            return
    # 执行 内容
    if mc_command['command_type'] == 2 and len(mc_command['content'].strip()) == 0:
        await bot.send_group_msg(
            group_id=event.group_id,
            # message=message.MessageSegment.at(event.sender['user_id']) + "执行内容不能为空"
            message=message.MessageSegment.reply(event.message_id) + "执行内容不能为空"
        )
    group_info = await bot.get_group_info(group_id=event.group_id)
    sender_name = event.sender['nickname']
    if len(event.sender['card']) != 0:
        sender_name = event.sender['card']
    data = {
        'qq_group': group_info['group_id'],
        'qq_group_name': group_info['group_name'],
        'sender': sender_name,
        'server_id': mc_command['server_id'],
        'message_type': mc_command['command_type'],
        'message': mc_command['content']
    }
    url = f'{message_channel_host}/api/broadcast_from_qq?token={config.MC_ACCESS_TOKEN}'
    resp = requests.post(url, json=data, headers={"Content-Type": "application/json"}, verify=False)

    if resp.status_code == 200:
        if mc_command['command_type'] == 2:
            await bot.send_group_msg(
                group_id=event.group_id,
                message=message.MessageSegment.reply(event.message_id) + '命令已发送至目标服务器执行'
            )
    else:
        if config.COMMAND_FAILED_NOTICE:
            # 检查Bot是否是管理员或群主
            botinfo = await bot.get_group_member_info(group_id=event.group_id, user_id=bot_user_id)
            if botinfo['role'] in ['owner', 'admin']:
                await bot.send_private_msg(
                    user_id=event.sender['user_id'],
                    group_id=event.group_id,
                    message=message.MessageSegment.face(36) + f'消息发送出现错误：{resp.content.decode("utf-8")}'
                )
            else:
                print(f'[ERROR] 消息发送出现异常，但是Bot不是QQ群管理员，无法私聊发送者报错内容：{resp.content.decode("utf-8")}')


