from os import path
import nonebot
import sys
sys.path.append('/var/lib/message-channel')
try:
    import nonebot_config as config
except:
    import nonebot.default_config as config

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'plugins'),
        'plugins'
    )
    nonebot.run()