# 《崩坏：星穹铁道》工具箱

<div align="center">
<img src="https://s1.ax1x.com/2023/04/30/p98Cv26.png" alt="logo" />
</div>

## 开发状态

| 主分支版本 | 开发分支版本 | PyPI 版本 |
| :--------: | :----------: | :-------: |
|   0.3.0    |    0.3.0     |   0.3.0   |

- [x] 支持命令行导出 csv、xlsx、json 格式抽卡记录
- [x] 支持命令行显示抽卡报告
- [x] 支持导出 markdown 格式抽卡报告
- [x] 支持导出网页版抽卡报告
- [x] 支持中英文多语言导出
- [ ] 支持 Windows 平台游戏中自动检测 API URL
- [ ] 实现用户界面并编译到 Windows 与 macOS 平台
- [ ] 支持自动检查更新

## 安装方式

目前仅提供命令行版本，用户交互界面版本正在开发中。

### 命令行安装

Python 用户可以直接使用 pip 安装本工具：

```shell
pip install starrail-toolkit --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 从源码安装

若需要使用尚未推送到 PyPI 版本的功能，可通过源码安装：

```shell
git clone git@github.com:LittleNyima/honkai-starrail-toolkit.git
cd honkai-starrail-toolkit
python setup.py install
```

## 使用指南

### 获取抽卡查询 API URL

请参考[【这个教程】](docs/how-to-get-api-url.md)获取查询链接。

由此可以获得一个形如 `https://api-takumi.mihoyo.com/common/gacha_record/api/getGachaLog?xxxxx` 的 URL，后续步骤使用的就是这个 URL。注意：API URL 会在一定时间后过期，过期后需要重新获取。

### 导出抽卡记录

#### 命令行导出

可以使用如下命令导出：

```shell
hksr --api https://api-takumi.mihoyo.com/xxx
```

**参数说明：**

- `--api`：（必选）API URL 地址。*注：未来将支持自动获取 API URL，届时本参数将变为可选。*
- `--export`：（可选）导出格式选项。默认为导出全部格式，若仅需导出部分格式，可以替换对应参数。目前支持的格式有 `csv`、`html`、`json`、`md`、`xlsx`。例如，若只需要 json 与 xlsx 格式数据，可以替换为 `--export json xlsx`。
- `--locale`：（可选）控制输出语言。默认为输出简体中文，可选值为 `en`（英语）、`chs`（简体中文）。
- `--log-level`：（可选）日志等级。控制日志的输出等级，默认为 `DEBUG`。若感觉输出的日志过多影响观感，建议将日志等级更改为 `INFO`，例如：`--log-level INFO`。从高到低的可选值为 `CRITICAL`、`ERROR`、`WARNING`、`INFO`、`DEBUG`。

## 导出结果示例

- Excel 结果示例（为保护隐私已隐藏部分信息）

  <img src="https://s1.ax1x.com/2023/05/02/p9GJKts.png" alt="xlsx" style="width: 600px;" />

- Markdown 结果示例：

  <img src="https://s1.ax1x.com/2023/05/02/p9GYNKf.png" alt="markdown" style="width: 600px;" />
