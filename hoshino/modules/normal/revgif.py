import re
from io import BytesIO
from PIL import Image, ImageSequence
from base64 import b64encode
from hoshino import Service, aiorequests
from nonebot import MessageSegment

sv = Service(
    "GIF倒放",
    visible=True,
    enable_on_default=True,
    bundle="GIF倒放",
    help_="""
- [倒放 xx] xx为gif图
""".strip(),
)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-cn",
}


@sv.on_keyword("倒放")
async def revgif(bot, ev):
    message_id = None
    # 情况1，用户对需要倒放的gif进行回复
    match = re.match(r"\[CQ:reply,id=(?P<id>.*)\]\[CQ:", str(ev.message))
    if match is not None:
        message_id = match.group("id")
        pre_message = await bot.get_msg(message_id=message_id)
        pre_raw_message = pre_message["message"]
        await match_revgif(bot, ev, custom=pre_raw_message)
    else:
        await match_revgif(bot, ev)


async def match_revgif(bot, ev, custom=None):
    if custom is not None:
        ev.message = str(custom)
    # 情况2，用户直接发送“倒放+GIF图片”
    match = re.match(r"(.*)\[CQ:image(.*?)url=(?P<url>.*)\]", str(ev.message))
    if match is not None:
        image_url = match.group("url")
        await do_revgif(bot, ev, image_url)
    else:
        await bot.finish(ev, "未找到图片信息，请尝试重新发送图片")


async def do_revgif(bot, ev, image_url):
    print("正在准备图片")
    response = await aiorequests.get(image_url, headers=headers)
    image = Image.open(BytesIO(await response.content))
    print(f"frames:{image.n_frames}, mode:{image.mode}, info:{image.info}")

    if image.n_frames == 1:
        await bot.finish(ev, "非GIF图片")
    if image.n_frames > 200:
        await bot.finish(ev, "GIF帧数太多了，罢工.jpg")

    sequence = []
    for f in ImageSequence.Iterator(image):
        sequence.append(f.copy())
    if len(sequence) > 30:
        await bot.send(ev, "正在翻转图片序列，请稍候")
    sequence.reverse()
    buffer = BytesIO()
    sequence[0].save(buffer, format="GIF", save_all=True, append_images=sequence[1:])
    b64_img = b64encode(buffer.getvalue()).decode()
    await bot.send(ev, MessageSegment.image(f"base64://{b64_img}"))
    buffer.close()
