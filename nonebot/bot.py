import nonebot
import config

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.run(host='mc-nonebot', port=9092, debug=False)