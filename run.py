import hoshino
import asyncio

bot = hoshino.init()
app = bot.asgi

if __name__ == "__main__":
    try:
        bot.run(use_reloader=False, loop=asyncio.get_event_loop())
    except Exception as e:
        import json

        emsg = "异常出错：" + repr(e)
        print(emsg)
        with open("./error.txt", "w", encoding="utf8") as f:
            json.dump(emsg, f, ensure_ascii=False)
