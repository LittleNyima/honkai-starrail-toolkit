# 《崩坏：星穹铁道》工具箱

<div style="min-height: 275px">
<img src="https://s1.ax1x.com/2023/04/30/p98Cv26.png" alt="logo" align="left" vertical-align="center" />

```
Starrail Toolkit

- 主分支版本：0.2.0
- 开发分支版本：0.2.0
- PyPI 版本：0.2.0
```
</div>

<br clear="left">

## 开发状态

- [x] 支持命令行导出 csv、xlsx、json 格式抽卡记录
- [x] 支持命令行显示抽卡报告
- [x] 支持导出 markdown 格式抽卡报告
- [ ] 支持导出网页版抽卡报告
- [ ] 支持 Windows 平台游戏中自动检测 API URL
- [ ] 实现用户界面并编译到 Windows 与 macOS 平台
- [ ] 支持自动检查更新

## 导出结果示例

- Excel 结果示例（为保护隐私已隐藏部分信息）

  ![xlsx](https://s1.ax1x.com/2023/05/02/p9GJKts.md.png)

- Markdown 结果示例：

  ![markdown](https://s1.ax1x.com/2023/05/02/p9GJMhn.md.png)

## 安装方式

目前仅提供命令行版本，用户交互界面版本正在开发中。

### 命令行安装

Python 用户可以直接使用 pip 安装本工具：

```shell
pip install starrail-toolkit --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 使用指南

### 获取抽卡查询 API URL

请参考[【这个教程】](docs/how-to-get-api-url)获取查询链接。

由此可以获得一个形如 `https://api-takumi.mihoyo.com/common/gacha_record/api/getGachaLog?xxxxx` 的 URL，后续步骤使用的就是这个 URL。注意：API URL 会在一定时间后过期，过期后需要重新获取。

### 导出抽卡记录

#### 命令行导出

可以使用如下命令导出：

```shell
hksr --api https://api-takumi.mihoyo.com/xxx --export all
```

参数：`--export` 为导出格式，默认为导出全部格式，若仅需导出部分格式，可将对应参数替换。目前支持的格式有 `csv`、`json`、`md`、`xlsx`，替换方式例如 `--export json xlsx`。
