# 《崩坏：星穹铁道》工具箱

<img src="https://s1.ax1x.com/2023/04/30/p98Cv26.png" alt="logo" align="left" vertical-align="center" />

```
Starrail Toolkit

- 主分支版本：0.1.0
- 开发分支版本：0.1.0
```

<br clear="left">

## 开发状态

- [x] 支持命令行导出 csv、xlsx、json 格式抽卡记录
- [ ] 支持命令行显示抽卡报告
- [ ] 支持导出网页版抽卡报告
- [ ] 支持 Windows 平台游戏中自动检测 API URL
- [ ] 实现用户界面并编译到 Windows 与 macOS 平台
- [ ] 支持自动检查更新

## 安装方式

目前仅提供命令行版本，用户交互界面版本正在开发中。

### 命令行安装

Python 用户可以直接使用 pip 安装本工具：

```shell
pip install starrail-toolkit --upgrade
```

## 使用指南

### 获取抽卡查询 API URL

由此可以获得一个形如 `https://api-takumi.mihoyo.com/common/gacha_record/api/getGachaLog?xxxxx` 的 URL，后续步骤使用的就是这个 URL。注意：API URL 会在一定时间后过期，过期后需要重新获取。

### 导出抽卡记录

#### 命令行导出

可以使用如下命令导出：

```shell
hksr https://api-takumi.mihoyo.com/xxx --export all
```

参数：`--export` 为导出格式，默认为导出全部格式，若仅需导出部分格式，可将对应参数替换。目前支持的格式有 `csv`、`json`、`xlsx`，替换方式例如 `--export json xlsx`。
