"""这是一份实例配置文件

将其修改为你需要的配置，并将文件夹config_example重命名为config
"""
# 插件配置
analysis_blacklist = []  # 不解析里面填写的QQ号发的bilibili链接 List[int]
analysis_display_image = False  # 是否显示解析b站插件的图片 true/false
allow_group = []  # 默认同意好友的群配置，如果申请的人在下列群里，默认同意好友请求 List[int]

# hoshino监听的端口与ip
PORT = 8080
HOST = "127.0.0.1"  # 本地部署使用此条配置（QQ客户端和bot端运行在同一台计算机）
# HOST = '0.0.0.0'          # 开放公网访问使用此条配置（不安全）
ACCESS_TOKEN = ""  # 访问密钥，强烈推荐在公网的服务器设置

DEBUG = False  # 调试模式

BLACK_LIST = []  # 黑名单，权限为 BLACK = -999
WHITE_LIST = []  # 白名单，权限为 WHITE = 51
SUPERUSERS = [10000]  # 填写超级用户的QQ号，可填多个用半角逗号","隔开，权限为 SUPERUSER = 999
NICKNAME = ""  # 机器人的昵称。呼叫昵称等同于@bot，可用元组配置多个昵称

COMMAND_START = {""}  # 命令前缀（空字符串匹配任何消息）
COMMAND_SEP = set()  # 命令分隔符（hoshino不需要该特性，保持为set()即可）

# 发送图片的协议
# 可选 http, file, base64
# 当QQ客户端与bot端不在同一台计算机时，可用http协议
RES_PROTOCOL = "file"
# 资源库文件夹，需可读可写，windows下注意反斜杠转义
RES_DIR = r"./res/"
# 使用http协议时需填写，原则上该url应指向RES_DIR目录
RES_URL = "http://127.0.0.1:5000/static/"


# 启用的模块
# 初次尝试部署时请先保持默认
# 如欲启用新模块，请认真阅读部署说明，逐个启用逐个配置
# 切忌一次性开启多个
MODULES_ON = {
    "botmanage",
    "normal",
    "groupmaster",
    "music"
}
