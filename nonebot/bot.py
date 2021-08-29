from os import path
import nonebot
import sys
sys.path.append('/var/lib/message-channel')
import nonebot_config

if __name__ == '__main__':
    nonebot.init(nonebot_config)
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'plugins'),
        'plugins'
    )
    nonebot.run()