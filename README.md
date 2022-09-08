## 简介

**EQBot:** [HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)->[nonebot1](https://docs.nonebot.dev/) 的一个分支。

## 关于分支

- 支持频道
- 支持第一个超级用户的私聊
- 只保留了基础的功能

## 获取插件

- [HoshinoBot-plugins-index](https://github.com/pcrbot/HoshinoBot-plugins-index)
- [HoshinoBot-Plugins](https://github.com/mengshouer/HoshinoBot-Plugins)
- [Github 搜索等](https://github.com/search?q=hoshino)

## 使用方法

1. 安装 Python3.8+，推荐安装[Miniconda](https://docs.conda.io/en/latest/miniconda.html)进行环境管理。
2. 克隆本仓库并安装依赖
   ```bash
    git clone https://github.com/mengshouer/EQBot.git
    cd EQBot
    python -m pip install -r requirements.txt
   ```
3. 进入`hoshino`文件夹，将`config_example`文件夹复制一份，重命名为`config`，然后编辑其中的`__bot__.py`，按照其中的注释说明进行编辑。
   > 如果您不清楚某项设置的作用，请保持默认。
4. 回到命令行运行`python run.py`

   > 使用 MiniConda 管理环境的请先激活环境，然后运行`python run.py`。

   > 若能看到日志 INFO: Running on 127.0.0.1:8080，说明启动成功。您可以忽略启动时的 WARNING 信息。如果出现 ERROR，说明部分功能可能加载失败。
