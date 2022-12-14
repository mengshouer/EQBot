import datetime
import typing

from nonebot import MessageSegment

from hoshino import Service

from .search_netease_cloud_music import search as search163
from .search_qq_music import search as searchqq
from .search_migu_music import search as searchmigu

sv = Service(
    "点歌",
    enable_on_default=True,
    visible=True,
    help_="[点歌 好日子] 混合搜索\n"
    "[搜网易云 好日子] 搜索网易云\n"
    "[搜QQ音乐 好日子] 搜索QQ音乐\n"
    "[搜咪咕音乐 好日子] 搜索咪咕音乐",
    bundle="点歌",
)

cool_down = datetime.timedelta(minutes=0.1)  # 冷却时间
expire = datetime.timedelta(minutes=0.5)

temp = {}
last_check = {}


@sv.on_prefix(["选", "选择", "选歌"])
async def choose_song(bot, ev):
    key = f"{ev.group_id}-{ev.user_id}"
    if key not in temp:
        if (
            str(ev.group_id) in last_check
            and datetime.datetime.now() - last_check[str(ev.group_id)] < expire
        ):
            await bot.send(ev, "不可以替他人选歌哦", at_sender=True)
        return
    song_dict = temp[key]
    song_idx = []
    for msg_seg in ev.message:
        if msg_seg.type == "text" and msg_seg.data["text"]:
            song_idx.append(msg_seg.data["text"].strip())
    if not song_idx:
        await bot.send(ev, "你想听什么呀?", at_sender=True)
    else:
        song_idx = "".join(song_idx)
        for idx in song_idx:
            if idx in song_dict:
                song = song_dict[idx]
                if song["type"] == "163":
                    music = MessageSegment.music(song["type"], song["id"])
                elif song["type"] == "custom":
                    music = MessageSegment(type_="music", data=song)
                else:
                    music = MessageSegment(
                        type_="music",
                        data={
                            "id": str(song["id"]),
                            "type": song["type"],
                            "content": song["artists"],
                        },
                    )
                await bot.send(ev, music)
        del temp[key]
        del last_check[str(ev.group_id)]


@sv.on_prefix(("点歌", "我想听"))
async def play_music(bot, ev):
    if str(ev.user_id) in last_check:
        intervals = datetime.datetime.now() - last_check[str(ev.user_id)]
        if intervals < cool_down:
            await bot.send(ev, f"冷却，请{(cool_down - intervals).seconds}秒之后再点歌哦~")
            return
    music_name = []
    for msg_seg in ev.message:
        if msg_seg.type == "text" and msg_seg.data["text"]:
            music_name.append(msg_seg.data["text"].strip())
    if not music_name:
        await bot.send(ev, "歌呢?", at_sender=True)
    else:
        music_name = "".join(music_name)
        song_list = await search163(music_name)
        if song_list:
            key = f"{ev.group_id}-{ev.user_id}"
            temp[key] = {}
            for idx, song in enumerate(song_list):
                temp[key][str(idx)] = song
            song_dict = temp[key]
            song_idx = "0"
            for idx in song_idx:
                if idx in song_dict:
                    song = song_dict[idx]
                    if song["type"] == "163":
                        music = MessageSegment.music(song["type"], song["id"])
                    elif song["type"] == "custom":
                        music = MessageSegment(type_="music", data=song)
                    else:
                        music = MessageSegment(
                            type_="music",
                            data={
                                "id": str(song["id"]),
                                "type": song["type"],
                                "content": song["artists"],
                            },
                        )
                    await bot.send(ev, music)
                    await bot.send(ev, '如果没有搜索到想要结果，可以试着使用"点选"')
            del temp[key]
        else:
            await bot.send(ev, "什么也没有找到")


@sv.on_prefix(("点选", "搜歌曲"))
async def to_apply_for_title(bot, ev):
    if str(ev.user_id) in last_check:
        intervals = datetime.datetime.now() - last_check[str(ev.user_id)]
        if intervals < cool_down:
            await bot.send(ev, f"冷却，请{(cool_down - intervals).seconds}秒之后再点歌哦~")
            return
    music_name = []
    for msg_seg in ev.message:
        if msg_seg.type == "text" and msg_seg.data["text"]:
            music_name.append(msg_seg.data["text"].strip())
    if not music_name:
        await bot.send(ev, "歌呢?", at_sender=True)
    else:
        music_name = "".join(music_name)
        song_list = await search_music(music_name)
        if song_list:
            sv.logger.info("成功获取到歌曲列表")
            key = f"{ev.group_id}-{ev.user_id}"
            temp[key] = {}
            # _music = MessageSegment.music(type_=_type, id_=_id)
            msg = ["我找到了这些~!"]
            flag, flag2 = True, True
            if song_list[0]["type"] == "163":
                msg.append("=== 网易云音乐 ===")
            for idx, song in enumerate(song_list):
                if song["type"] == "qq" and flag:
                    msg.append("=== QQ 音乐 ===")
                    flag = False
                if song["type"] == "custom" and song["subtype"] == "migu" and flag2:
                    msg.append("=== 咪咕音乐 ===")
                    flag2 = False
                msg.append(f'{idx}. {song["name"]} - {song["artists"]}')
                temp[key][str(idx)] = song
            msg.append("=" * 13)
            msg.append("发送[选择]+序号来听歌吧~")
            await bot.send(ev, "\n".join(msg), at_sender=True)
            last_check[str(ev.group_id)] = datetime.datetime.now()
            last_check[str(ev.user_id)] = datetime.datetime.now()
        else:
            await bot.send(ev, "什么也没有找到")


@sv.on_prefix(("搜163", "搜网易云"))
async def search_netease_cloud_music(bot, ev):
    if str(ev.user_id) in last_check:
        intervals = datetime.datetime.now() - last_check[str(ev.user_id)]
        if intervals < cool_down:
            await bot.send(ev, f"冷却，请{(cool_down - intervals).seconds}秒之后再点歌哦~")
            return
    music_name = []
    for msg_seg in ev.message:
        if msg_seg.type == "text" and msg_seg.data["text"]:
            music_name.append(msg_seg.data["text"].strip())
    if not music_name:
        await bot.send(ev, "你想听什么呀?", at_sender=True)
    else:
        music_name = "".join(music_name)
        song_list = await search163(music_name, result_num=5)
        if song_list:
            sv.logger.info("成功获取到歌曲列表")
            key = f"{ev.group_id}-{ev.user_id}"
            temp[key] = {}
            # _music = MessageSegment.music(type_=_type, id_=_id)
            msg = ["我找到了这些~!"]
            for idx, song in enumerate(song_list):
                msg.append(f'{idx}. {song["name"]} - {song["artists"]}')
                temp[key][str(idx)] = song
            msg.append("=" * 13)
            msg.append("发送[选择]+序号来听歌吧~")
            await bot.send(ev, "\n".join(msg), at_sender=True)
            last_check[str(ev.group_id)] = datetime.datetime.now()
            last_check[str(ev.user_id)] = datetime.datetime.now()
        else:
            await bot.send(ev, "什么也没有找到")


@sv.on_prefix(("搜qq音乐", "搜QQ音乐"))
async def search_qq_music(bot, ev):
    if str(ev.user_id) in last_check:
        intervals = datetime.datetime.now() - last_check[str(ev.user_id)]
        if intervals < cool_down:
            await bot.send(ev, f"冷却，请{(cool_down - intervals).seconds}秒之后再点歌哦~")
            return
    music_name = []
    for msg_seg in ev.message:
        if msg_seg.type == "text" and msg_seg.data["text"]:
            music_name.append(msg_seg.data["text"].strip())
    if not music_name:
        await bot.send(ev, "你想听什么呀?", at_sender=True)
    else:
        music_name = "".join(music_name)
        song_list = await searchqq(music_name, result_num=5)
        if song_list:
            sv.logger.info("成功获取到歌曲列表")
            key = f"{ev.group_id}-{ev.user_id}"
            temp[key] = {}
            # _music = MessageSegment.music(type_=_type, id_=_id)
            msg = ["我找到了这些~!"]
            for idx, song in enumerate(song_list):
                msg.append(f'{idx}. {song["name"]} - {song["artists"]}')
                temp[key][str(idx)] = song
            msg.append("=" * 13)
            msg.append("发送[选择]+序号来听歌吧~")
            await bot.send(ev, "\n".join(msg), at_sender=True)
            last_check[str(ev.group_id)] = datetime.datetime.now()
            last_check[str(ev.user_id)] = datetime.datetime.now()
        else:
            await bot.send(ev, "什么也没有找到")


@sv.on_prefix(("搜migu", "搜migu音乐", "搜咪咕音乐"))
async def search_migu_music(bot, ev):
    if str(ev.user_id) in last_check:
        intervals = datetime.datetime.now() - last_check[str(ev.user_id)]
        if intervals < cool_down:
            await bot.send(ev, f"冷却，请{(cool_down - intervals).seconds}秒之后再点歌哦~")
            return
    music_name = []
    for msg_seg in ev.message:
        if msg_seg.type == "text" and msg_seg.data["text"]:
            music_name.append(msg_seg.data["text"].strip())
    if not music_name:
        await bot.send(ev, "你想听什么呀?", at_sender=True)
    else:
        music_name = "".join(music_name)
        song_list = await searchmigu(music_name, result_num=5)
        if song_list:
            sv.logger.info("成功获取到歌曲列表")
            key = f"{ev.group_id}-{ev.user_id}"
            temp[key] = {}
            # _music = MessageSegment.music(type_=_type, id_=_id)
            msg = ["我找到了这些~!"]
            for idx, song in enumerate(song_list):
                msg.append(f'{idx}. {song["title"]} - {song["content"]}')
                temp[key][str(idx)] = song
            msg.append("=" * 13)
            msg.append("发送[选择]+序号来听歌吧~")
            await bot.send(ev, "\n".join(msg), at_sender=True)
            last_check[str(ev.group_id)] = datetime.datetime.now()
            last_check[str(ev.user_id)] = datetime.datetime.now()
        else:
            await bot.send(ev, "什么也没有找到")


async def search_music(music_name: str) -> typing.Union[list, dict]:
    result = []
    song_list = await search163(music_name)
    if song_list:
        result += song_list
    song_list = await searchqq(music_name)
    if song_list:
        result += song_list
    song_list = await searchmigu(music_name)
    if song_list:
        result += song_list
    return result
