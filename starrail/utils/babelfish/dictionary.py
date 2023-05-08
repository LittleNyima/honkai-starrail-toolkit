from starrail.utils.babelfish.multilingual import MultilingualString as _MS

# Lookup table - used by dictionary

lookup_table = dict(
    STELLAR=_MS(en='Stellar Warp', zhs='群星跃迁'),
    DEPARTURE=_MS(en='Departure Warp', zhs='始发跃迁'),
    CHARACTER=_MS(en='Character Event Warp', zhs='角色跃迁'),
    LIGHT_CONE=_MS(en='Light Cone Event Warp', zhs='光锥跃迁'),
)

# === BEGIN OF PRE-DEFINED VOCABULARIES ===

average_gacha_per_5_star = _MS(
    en='Average gacha per 5-star',
    zhs='五星平均抽数',
)
gacha_report = _MS(en='Gacha Report', zhs='抽卡分析')
gacha_title = _MS(
    en='Gacha Report for Honkai: Star Rail Player {}',
    zhs='《崩坏：星穹铁道》玩家{}的抽卡分析',
)
history_of_5_stars = _MS(
    en='History of 5-star gacha attempts',
    zhs='五星出货记录',
)
html_thead = _MS(
    en=(
        '<th>Type</th><th>Count</th><th>Basic Prob.</th><th>True Prob.</th>'
        '<th>Since Last</th>'
    ),
    zhs=('<th>星级</th><th>数量</th><th>基础概率</th><th>综合概率</th><th>距上次</th>'),
)
markdown_thead = _MS(
    en=(
        '| Type | Count | Basic Prob. | True Prob. | Since Last |\n'
        '| ---- | ----- | ----------- | ---------- | ---------- |\n'
    ),
    zhs=(
        '| 星级 | 数量 | 基础概率 | 综合概率 | 距上次 |\n'
        '| ---- | ---- | ------ | ------- | ---- |\n'
    ),
)
ui_about = _MS(en='About', zhs='关于')
ui_downloading_gacha = _MS(
    en='Downloading page {page} of type {name}',
    zhs='正在导出{name}的第{page}页',
)
ui_extract_api_fail = _MS(
    en='Extracting API URL failed. Please retry after exiting the game.',
    zhs='提取 API URL 失败，请关闭游戏或重新查询抽卡信息后重试。',
)
ui_extracting_api_url = _MS(
    en='Extracting API URL',
    zhs='正在提取 API URL',
)
ui_gacha_basic_prob = _MS(en='Basic Prob.', zhs='基础概率')
ui_gacha_count = _MS(en='Count', zhs='数量')
ui_gacha_since_last = _MS(en='Since Last', zhs='距上次')
ui_gacha_sync = _MS(en='Sync Gacha Data', zhs='抽卡数据同步')
ui_gacha_sync_desc = _MS(
    en=(
        'First query warp record in the game, then close the game and click '
        'the sync button.'
    ),
    zhs='先在游戏里查询一次抽卡记录，然后退出游戏，点击同步按钮。',
)
ui_gacha_true_prob = _MS(en='True Prob.', zhs='综合概率')
ui_gacha_type = _MS(en='Type', zhs='星级')
ui_get_started = _MS(en='Get Started', zhs='开始使用')
ui_get_started_desc = _MS(
    en='Learning how to use the toolkit.',
    zhs='学习本工具箱的基本使用方法。',
)
ui_github_repo = _MS(en='GitHub Repo', zhs='开源代码')
ui_github_repo_desc = _MS(
    en='This project is open-resource, licenced under GPLv3. View code here.',
    zhs='本项目代码开源，以 GPLv3 分发。点此查看源代码。',
)
ui_no_data = _MS(en='No Data', zhs='暂无数据')
ui_open_docs = _MS(en='Open Documentations', zhs='打开帮助页面')
ui_open_issues = _MS(en='Open Issue Page', zhs='打开反馈页面')
ui_personalization = _MS(en='Personalization', zhs='个性化')
ui_save_data = _MS(en='Save As', zhs='保存数据')
ui_save_success = _MS(en='Data Save Success', zhs='保存成功')
ui_save_success_msg = _MS(en='Data is saved to {}', zhs='数据已保存到{}')
ui_send_feedback = _MS(en='Send Feedback', zhs='提交反馈')
ui_send_feedback_desc = _MS(
    en='Feedback is welcome if you encounter problems or have suggestions.',
    zhs='如果你遇到问题，或对本项目有更多建议，欢迎提交反馈。',
)
ui_settings = _MS(en='Settings', zhs='设置')
ui_sync = _MS(en='Sync Data', zhs='同步数据')
ui_sync_gacha_fail = _MS(
    en='Synchronization Failed',
    zhs='同步失败',
)
ui_sync_gacha_initial = _MS(
    en='Initializing...',
    zhs='正在初始化同步线程',
)
ui_sync_gacha_success = _MS(
    en='Synchronization Success',
    zhs='同步成功',
)
ui_synchronizing_gacha = _MS(
    en='Synchronizing...',
    zhs='正在同步抽卡数据',
)
ui_title = _MS(en='Honkai: Star Rail Toolkit', zhs='崩坏：星穹铁道工具箱')
ui_traceback = _MS(en='Traceback', zhs='报错信息')
ui_troubleshooting = _MS(en='TroubleShooting', zhs='常见问题')
ui_troubleshooting_desc = _MS(
    en='Click here to view FAQ.',
    zhs='点此查看常见问题解答。（目前还没写，所以会跳转到百度）',
)
ui_users = _MS(en='Users', zhs='用户管理')
ui_users_desc = _MS(en='Multi-user management', zhs='如果有多个账号可以用这个切换')
ui_welcome = _MS(
    en='Welcome to HKSR Toolkit!',
    zhs='欢迎登车！',
)

# === END OF PRE-DEFINED VOCABULARIES ===
