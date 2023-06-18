# base api urls
hk4e_sdk_api = 'https://hk4e-sdk.mihoyo.com'
passport_api = 'https://passport-api.mihoyo.com'
public_data_api = 'https://public-data-api.mihoyo.com'
takumi_api = 'https://api-takumi.mihoyo.com'
takumi_record_api = 'https://api-takumi-record.mihoyo.com'

# hkrpg static api
announcements = (
    'https://hkrpg-api-static.mihoyo.com/common/hkrpg_cn/announcement/api/get'
    'AnnContent?game=hkrpg&game_biz=hkrpg_cn&lang=zh-cn&bundle_id=hkrpg_cn&pl'
    'atform=pc&region=prod_gf_cn&level=70&channel_id=1'
)

# public data
device_fingerprint = f'{public_data_api}/device-fp/api/getFp'

# hoyolab universal
game_record = f'{takumi_record_api}/game_record/card/wapi/getGameRecordCard'

# auth
auth_api = f'{takumi_api}/auth/api'
get_token_by_login_tikcet = f'{auth_api}/getMultiTokenByLoginTicket'
get_cookie_by_stoken = f'{auth_api}/getCookieAccountInfoBySToken'
get_cookie_by_game_token = f'{auth_api}/getCookieAccountInfoByGameToken'
get_stoken_by_game_token = (
    f'{passport_api}/account/ma-cn-session/app/getTokenByGameToken'
)

# qrcode
qrcode_api = f'{hk4e_sdk_api}/hk4e_cn/combo/panda/qrcode'
qrcode_fetch = f'{qrcode_api}/fetch'
qrcode_query = f'{qrcode_api}/query'

# honkai: star rail api
hksr_record_api = f'{takumi_record_api}/game_record/app/hkrpg/api'
hksr_basic_info = f'{hksr_record_api}/role/basicInfo'       # 角色基础信息
hksr_index = f'{hksr_record_api}/index'                     # 角色橱窗信息
hksr_avatar_info = f'{hksr_record_api}/avatar/info'         # 角色详细信息
hksr_note = f'{hksr_record_api}/note'                       # 实时便笺
hksr_month_info = f'{takumi_api}/event/srledger/month_info'  # 开拓月历
