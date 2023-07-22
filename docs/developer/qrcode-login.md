# 二维码扫码登陆响应参考

使用二维码进行登陆时，二维码共有四种状态：

- 初始状态（Init）：二维码未被扫描
- 已扫描（Scanned）：二维码已被扫描，但用户尚未确认
- 已确认（Confirmed）：用户已经点击确认
- 已过期（Expired）：二维码过期

## 响应示例

初始状态：

```json
{
    "retcode": 0,
    "message": "OK",
    "data": {
        "stat": "Init",
        "payload": {
            "proto": "Raw",
            "raw": "",
            "ext": ""
        }
    }
}
```

已扫描：

```json
{
    "retcode": 0,
    "message": "OK",
    "data": {
        "stat": "Scanned",
        "payload": {
            "proto": "Raw",
            "raw": "",
            "ext": ""
        }
    }
}
```

已确认：

```json
{
    "retcode": 0,
    "message": "OK",
    "data": {
        "stat": "Confirmed",
        "payload": {
            "proto": "Account",
            "raw": "{\n    \"uid\": \"123456789\",\n    \"token\": \"d0kFcb3crAzYkUTHursdAyHviVo4D50q\"\n}",
            "ext": ""
        }
    }
}
```

已过期：

```json
{
    "data": null,
    "message": "ExpiredCode",
    "retcode":-106
}
```
