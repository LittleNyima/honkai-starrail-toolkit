from starrail.utils.babelfish.multilingual import MultilingualString as _MS

# Lookup table - used by dictionary

lookup_table = dict(
    STELLAR=_MS(en='Stellar Warp', zhs='群星跃迁'),
    DEPARTURE=_MS(en='Departure Warp', zhs='始发跃迁'),
    CHARACTER=_MS(en='Character Event Warp', zhs='角色跃迁'),
    LIGHT_CONE=_MS(en='Light Cone Event Warp', zhs='光锥跃迁'),
)

# Pre-defined vocabularies

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
ui_send_feedback = _MS(en='Send Feedback', zhs='提交反馈')
ui_send_feedback_desc = _MS(
    en='Feedback is welcome if you encounter problems or have suggestions.',
    zhs='如果你遇到问题，或对本项目有更多建议，欢迎提交反馈。',
)
ui_title = _MS(en='Honkai: Star Rail Toolkit', zhs='崩坏：星穹铁道工具箱')
ui_troubleshooting = _MS(en='TroubleShooting', zhs='常见问题')
ui_troubleshooting_desc = _MS(
    en='Click here to view FAQ.',
    zhs='点此查看常见问题解答。（目前还没写，所以会跳转到百度）',
)
ui_welcome = _MS(
    en='Welcome to HKSR Toolkit!',
    zhs='欢迎使用！',
)
