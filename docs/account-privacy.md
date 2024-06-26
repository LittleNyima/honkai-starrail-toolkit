# 我的账号数据会被如何使用？

主要的账号数据分为三类：

- 游戏 UID、米游社通行证 ID
- 抽卡查询 URL 含有的 authkey 或 stoken
- 登陆时产生的 cookie

本应用程序使用的数据有：游戏 UID、authkey、cookie，**本应用承诺：除向米哈游官方服务器进行请求外，不会将任何账号数据上传到任何位置**。

## UID 与通行证 ID

这两者理论上来说属于公开数据，只能用来加好友和查看游戏内展示的角色的练度。

## authkey 和 stoken

这两者可以用于查询抽卡记录、访问 H5 活动等，有效期大约 24 小时。

## cookie

可以用于登陆米游社，有效期大约 30 天。

这三种信息中，使用 cookie 可以做到的事情最多，因此泄露后导致的账号安全风险最大。如果使用扫码绑定米游社账号功能，本程序会保存 cookie 到本地，解除绑定后保存的信息将被删除。
