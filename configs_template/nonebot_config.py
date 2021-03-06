# NONEBOT 相关设置
import os, yaml

from nonebot.default_config import *

if os.path.exists('/var/lib/message-channel/core.yml'):
    with open('/var/lib/message-channel/core.yml', 'r', encoding='utf-8') as iFile:
        config_ = yaml.safe_load(iFile)
else:
    config_ = {
        'access_token': '123456'
    }

##### 不建议更改
MC_ACCESS_TOKEN = config_['access_token'] # 确保与core.yml中的access_token相同
DEBUG = False
HOST = 'mc-nonebot'
PORT = 9092       # 该端口不用开放公网
#####

# 多个超级用户QQ用英文逗号隔开，QQ号使用整数类型，不要填写str
SUPERUSERS = { 765892480 }  # 超级用户的QQ号，拥有Bot控制的最高权限，可以触发 <执行> 命令

# 低权限管理员，只拥有某些服务器编号的执行权限
STAFFS = {
#    '123': [0],    # QQ号：[服务器编号]
}

COMMAND_TRIGGER = ['.', '。', '!', '！']   # 转发命令的前缀，设为[]空即为所有群内聊天内容都转发

COMMAND_FAILED_NOTICE = True  # 如果消息发送失败，机器人是否私聊通知指令发起者。 **开启该功能需要机器人是管理员或群主**

# QQ机器人命令格式
#
#       <前缀><服务器编号: 可选> <命令> <内容>
#
# 其中：
# - <前缀> 为COMMAND_TRIGGER中定义的单字符前缀，满足其中一种即可触发
# - <服务器编号> 使用状态查询即可查看服务器编号，从0开始，由message channel自动编号，必须是大于等于0的整数
# - <命令> 目前支持的命令有：
#       - 转发: 默认命令，如果没有指定命令都为转发消息至CSGO服务器
#       - 状态: 查询指定服务器，或所有服务器的状态（包括服务器编号)
#       - 执行: 执行服务器指令，例如sm_ban sm_kick
# - <内容> 转发服务器的内容，**注意** <前缀>与<内容>间有一个空格才能正常转发
#
#
# 举例：
# 如果我在某QQ绑定了2台游戏服务器信息，服务器编号分别为0和1
# 1. 
#   群内指令：. 今天天气真好
#   效果：将"今天天气真好"转发至所有游戏服务器中
#
# 2.
#   群内指令：.1 今天天气真好
#   效果：将"今天天气真好"转发至1号服务器中
# 
# 3. 
#   群内指令：.0 状态
#   效果：查询0号服务器状态
#
# 4.
#   群内指令：! 状态
#   效果：查询所有服务器状态（返回服务器编号），注意<前缀>与<内容>间有一个空格
#
# 5.
#   群内指令：.1 执行 sm_kick 76561198295959028 恶意骚扰
#   效果：将steamid为76561198295959028的玩家以"恶意骚扰"原因踢出服务器
#
# 6.
#   群内指令：!-1 状态
#   效果：解析失败，无效果