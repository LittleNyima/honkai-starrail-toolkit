# 《崩坏：星穹铁道》工具箱

<div align="center">
<img src="https://s1.ax1x.com/2023/05/06/p9atspD.png" alt="logo" />
</div>

## 开发状态

| 主分支版本 | 开发分支版本 | PyPI 版本 | 发行版版本 |
| :--------: | :----------: | :-------: | :--------: |
|   0.6.9    |    0.6.9     |   0.6.9   |   0.6.9    |

目前第一阶段开发已完成，历史开发计划见[该页面](docs/history-dev-plan.md)。

- [x] 支持更多的可设置选项
- [x] 支持解锁120帧
- [x] 支持以 SRGF 标准导出
- [x] 支持以 SRGF 标准导入
- [x] 支持手动设置 API URL
- [x] 支持夜间模式
- [x] 支持多用户切换
- [x] 美化程序界面

## 常见问题解答

关于程序使用过程中存在的问题，可以参考[本链接](docs/troubleshooting.md)获得解答。若问题无法解决，欢迎[提出反馈](https://github.com/LittleNyima/honkai-starrail-toolkit/issues)。

## 安装方式

### 下载可执行程序

目前提供两种分发途径：[GitHub Release](https://github.com/LittleNyima/honkai-starrail-toolkit/releases) 和 [蓝奏云](https://wwmg.lanzouk.com/iN7870y9o7gb)，两种途径的内容相同，可以自行选择下载方式。

![gui preview gacha](https://s1.ax1x.com/2023/06/01/p9xxdXj.png)

![gui preview unlock](https://s1.ax1x.com/2023/05/23/p9o76gA.png)

### 命令行安装

Python 用户可以直接使用 pip 安装本工具：

```shell
python3 -m pip install starrail-toolkit --force-reinstall --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 从源码安装

若需要使用尚未推送到 PyPI 版本的功能，可通过源码安装：

```shell
git clone git@github.com:LittleNyima/honkai-starrail-toolkit.git
cd honkai-starrail-toolkit
python3 setup.py install
```

注：如果出现关于 `qfluentwidgets` 相关的报错，可能是因为默认 pypi 源的版本较低，可以使用以下命令安装最新版本的依赖：

```
pip install -U PySide6-Fluent-Widgets -i https://pypi.org/simple/
```

##  命令行使用指南

### 获取抽卡查询 API URL

请参考[这个教程](docs/how-to-get-api-url.md)获取查询链接。

由此可以获得一个形如 `https://api-takumi.mihoyo.com/common/gacha_record/api/getGachaLog?xxxxx` 的 URL，后续步骤使用的就是这个 URL。注意：API URL 会在一定时间（大约 24 小时）后过期，过期后需要重新获取。

**注：若为 Windows 平台，可以使用本工具自动检测 API URL。** 首先登陆游戏，进入抽卡查询页面，当显示出一页抽卡查询结果后，退出游戏（由于 Windows 系统文件占用问题，若不退出，可能导致缓存无法读取），运行本工具，即可检测到抽卡查询 URL。如果需要切换账号，建议使用上述教程中的方法获取每个账号的 API URL，以便精确控制导出的账号。

### 导出抽卡记录

#### 命令行导出

可以使用如下命令导出：

```shell
# 非 Windows 平台
hksr gacha --api https://api-takumi.mihoyo.com/xxx
# Windows 平台无需 --api 参数
hksr gacha
```

**参数说明：**

- `--api`：（Windows 平台可选）API URL 地址。若为 Windows 平台，可以不填这个参数，而使用自动检测功能。
- `--export`：（可选）导出格式选项。默认为导出全部格式，若仅需导出部分格式，可以替换对应参数。目前支持的格式有 `csv`、`html`、`json`、`md`、`xlsx`。例如，若只需要 json 与 xlsx 格式数据，可以替换为 `--export json xlsx`。
- `--locale`：（可选）控制输出语言。默认为输出简体中文，可选值为 `en`（英语）、`chs`（简体中文）。
- `--log-level`：（可选）日志等级。控制日志的输出等级，默认为 `DEBUG`。若感觉输出的日志过多影响观感，建议将日志等级更改为 `INFO`，例如：`--log-level INFO`。（注意：若设置的日志等级过高，可能导致基本的信息无法显示，例如导出进度、导出位置、命令行版抽卡报告等）从高到低的可选值为 `CRITICAL`、`ERROR`、`WARNING`、`INFO`、`DEBUG`。
- `--request-interval`：（可选）请求间隔。两次请求之间的最小间隔，默认为 `0.1`。若某些情况下因请求过于频繁导致 IP 被 ban，可以适度把这个值调大一点。

**如果想要进一步了解命令行使用方法，请参考[命令行使用指南](docs/cli-guidance.md)。**

本项目目前正处于快速迭代阶段，使用方式可能会发生改变，请及时更新程序，更新时请留意本部分关于使用方式的说明。

## 导出结果示例

- Excel 结果示例（为保护隐私已隐藏部分信息）

  <img src="https://s1.ax1x.com/2023/05/02/p9GJKts.png" alt="xlsx" style="width: 600px;" />

- Markdown 结果示例：

  <img src="https://s1.ax1x.com/2023/05/02/p9GYNKf.png" alt="markdown" style="width: 600px;" />

## 安全提醒

本仓库代码完全开源，且用户数据全部保存在本地，**本项目不会上传任何用户数据**。本项目仅在该 GitHub 仓库及 PyPI 进行分发，请仔细甄别下载到的程序，防止遭遇恶意程序。

## Credits

本仓库用户界面部分基于 [**zhiyiYo/PyQt-Fluent-Widgets**](https://github.com/zhiyiYo/PyQt-Fluent-Widgets) 实现，缓存解析部分参考了 [**sunfkny/genshin-gacha-export**](https://github.com/sunfkny/genshin-gacha-export)，用户界面设计参考了 [**BoxCatTeam/SRCat**](https://github.com/BoxCatTeam/SRCat)。
