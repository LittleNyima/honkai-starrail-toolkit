# 工具箱命令行使用指南

## 基本用法

命令行的基本用法如下所示，基本格式为：`hksr 全局参数 命令类型 命令参数`

```
usage: hksr [-h] [--locale {en,zhs}] [--log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}] {gacha,unlock} ...

Honkai: Star Rail Toolkit

positional arguments:
  {gacha,unlock}

optional arguments:
  -h, --help            show this help message and exit
  --locale {en,zhs}     Language of gacha report. Abbreviations: `en` for English, `zhs` for simplified Chinese
  --log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}
                        Controlling the level of logging output.
```

## 用法示例

- 显示全局帮助信息：`hksr -h` 或 `hksr --help`
- 显示 `gacha` 命令帮助信息：`hksr gacha -h` 或 `hksr gacha --help`
- 用英语格式导出全部抽卡信息：`hksr --locale en gacha --export all`

## 全局参数

全局参数如下所示：

- `--locale`：（可选）控制输出语言。默认为输出简体中文，可选值为 `en`（英语）、`chs`（简体中文）。
- `--log-level`：（可选）日志等级。控制日志的输出等级，默认为 `DEBUG`。若感觉输出的日志过多影响观感，建议将日志等级更改为 `INFO`，例如：`--log-level INFO`。（注意：若设置的日志等级过高，可能导致基本的信息无法显示，例如导出进度、导出位置、命令行版抽卡报告等）从高到低的可选值为 `CRITICAL`、`ERROR`、`WARNING`、`INFO`、`DEBUG`。

## 命令参数

### gacha 命令

共有以下几个参数：

- `--api`：（Windows 平台可选）API URL 地址。若为 Windows 平台，可以不填这个参数，而使用自动检测功能。
- `--export`：（可选）导出格式选项。默认为导出全部格式，若仅需导出部分格式，可以替换对应参数。目前支持的格式有 `csv`、`html`、`json`、`md`、`xlsx`。例如，若只需要 json 与 xlsx 格式数据，可以替换为 `--export json xlsx`。
- `--load`：（可选）导入抽卡信息，应当传入符合 [SRGF 标准](https://uigf.org/zh/standards/SRGF.html)的 json 文件，若不填则默认跳过导入步骤。
- `--request-interval`：（可选）请求间隔。两次请求之间的最小间隔，默认为 `0.1`。若某些情况下因请求过于频繁导致 IP 被 ban，可以适度把这个值调大一点。

### unlock 命令

共有以下几个参数：

- `--fps`：（可选）要解锁到的帧率。
- `--reset`：（可选）重置帧率到 60 帧。
