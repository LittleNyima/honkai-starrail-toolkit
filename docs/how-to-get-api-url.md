# 抽卡分析链接获取教程

## Windows 平台

**[@Ricardo-Riley](https://github.com/Ricardo-Riley)** 提供的方法：在游戏目录 `Star Rail\Game\StarRail_Data\webCaches\Cache\Cache_Data\data_2` 文本搜索 `https://api-takumi.mihoyo.com/common/gacha_record/api/getGachaLog`，查找最后匹配的链接，可以得到url 地址。

施工中，目前可以参考[这篇图文教程](https://mp.weixin.qq.com/s/CzSTvRDJ3C3SVDQKPcLvVA)的方法。本项目现已实现自动检测 API URL，可以参考项目说明中的方法使用。

## iOS、iPadOS 平台

>  注：iOS 和 iPadOS 平台的获取方式与原神相同，如果文字版的教程感觉比较繁琐，可以参考**星穹铁道工坊的视频版教程**：[视频版教程见此链接](https://mp.weixin.qq.com/s/CzSTvRDJ3C3SVDQKPcLvVA)。

1. 前往 App Store 下载名为 **Stream** 的网络抓包工具（请注意甄别，应当是下图中的这个，不要下载到错误的软件）

   ![stream](https://s1.ax1x.com/2023/05/01/p9G1nRf.md.jpg)

2. 下载后打开软件，点击 **开始抓包** 按钮。

3. 这一步**仅在第一次使用时需要进行**，后续可直接跳过：

   - 添加 VPN 配置：点击开始抓包后会弹出「“Stream”想添加 VPN 配置」的通知，点击 **允许** 按钮，然后会弹出输入锁屏密码的界面，**输入密码** 后会自动返回 Stream 的应用界面。
   - 下载 CA 证书：点击 **去安装证书** 按钮，再点击灰色的 **安装CA证书** 按钮，这时会弹出一个网页尝试下载证书，点击 **允许** 按钮。
   - 安装 CA 证书：证书下载完后进入 **设置** 界面，选择 **通用** 标签，再选择底部的 **VPN与设备管理**，点击刚刚下载的证书（名称应当类似**Stream Generated CA xxx**），点击右上角的 **安装**，再选择安装证书。
   - 信任 CA 证书：返回 **设置** 界面，选择 **通用** 标签，再选择顶部的 **关于本机**，拉到最下边点击 **证书信任设置**，勾选刚刚安装的 **Stream Generated CA xxx**，点击 **继续**，即配置完成。
   - 检查是否配置成功：返回 Stream，如果此时显示“CA 证书已经安装且信任”，则表示配置成功，可以开始抓包。

4. 开始抓包后返回游戏，点击抽卡查询按钮，进入抽卡查询界面（需要看到最近的抽卡记录才行）。

5. 进行一次抽卡查询后返回 Stream 页面，点击 **停止抓包**。

6. 点击 **抓包历史**，然后点击 **最近的一条抓包记录**，找到开头为 `GET https://api-takumi.mihoyo.com/` 的请求，点进去之后选择 **请求** 标签页，长按请求链接，并选择 **复制请求链接**，即可得到请求 API 地址。

## Android 平台

施工中，目前可以参考[**这篇图文教程**](https://game.xiaomi.com/viewpoint/1439459001_1661508721405_100)的方法。
