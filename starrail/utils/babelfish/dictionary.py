from starrail.utils.babelfish.multilingual import MultilingualString as _MS

# Lookup table - used by dictionary

lookup_table = dict(
    STELLAR=_MS(en='Stellar Warp', zhs='群星跃迁'),
    DEPARTURE=_MS(en='Departure Warp', zhs='始发跃迁'),
    CHARACTER=_MS(en='Character Event Warp', zhs='角色跃迁'),
    LIGHT_CONE=_MS(en='Light Cone Event Warp', zhs='光锥跃迁'),
    GitHub_dist=_MS(en='GitHub Distribution', zhs='GitHub下载'),
    netdisk_dist=_MS(en='Net Disk Distribution', zhs='网盘下载'),
)

record_type_mapping = {
    '角色': 'character',
    '光锥': 'lightcone',
}

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
ui_3star_light_cone = _MS(en='Light Cone (3)', zhs='三星光锥')
ui_4star_character = _MS(en='Character (4)', zhs='四星角色')
ui_4star_light_cone = _MS(en='Light Cone (4)', zhs='四星光锥')
ui_5star_character = _MS(en='Character (5)', zhs='五星角色')
ui_5star_light_cone = _MS(en='Light Cone (5)', zhs='五星光锥')
ui_about = _MS(en='About', zhs='关于')
ui_about_this = _MS(en='About This Application', zhs='关于本软件')
ui_arerage_warps_per_5star = _MS(
    en='Average warps per 5 star',
    zhs='五星平均抽数',
)
ui_auto = _MS(en='Auto', zhs='跟随系统设置')
ui_average_warps_per_up = _MS(
    en='Average warps per up',
    zhs='UP 平均抽数',
)
ui_cancel_update = _MS(en='Cancel Update', zhs='暂不更新')
ui_check_update = _MS(en='Check Update', zhs='检查更新')
ui_check_update_at_start = _MS(
    en='Check Update at Application Start',
    zhs='启动时自动检查更新',
)
ui_check_update_at_start_desc = _MS(
    en='It\'s strongly recommended to turn this on to get the latest feature',
    zhs='强烈建议打开检查更新，本app版本快速迭代中，会加入更多功能。',
)
ui_check_update_fail = _MS(
    en='Check update failed. Please check your network connection.',
    zhs='检查更新失败，请检查你的网络连接并重试。（不重试也行，但是你可能没联网）',
)
ui_check_update_success = _MS(
    en='Check update finished',
    zhs='检查更新完成',
)
ui_copyright = _MS(
    en='Copyright © {} LittleNyima.',
    zhs='版权所有 © {} LittleNyima。',
)
ui_curr_fps = _MS(
    en='Current FPS in Game Settings: {}.',
    zhs='当前游戏设定帧率：{}。',
)
ui_current_account = _MS(en='Current', zhs='当前账号')
ui_current_version = _MS(
    en='Current version: {}.',
    zhs='当前版本：{}。',
)
ui_customize_url = _MS(
    en='Customize API URL',
    zhs='自定义 API URL',
)
ui_deduce_uid_fail = _MS(
    en='Fail to deduce uid. There may be no record. Please check.',
    zhs='检测 UID 失败，账号可能没有抽卡记录，请重试。',
)
ui_downloading_gacha = _MS(
    en='Downloading page {page} of type {name}',
    zhs='正在导出{name}的第{page}页',
)
ui_en = _MS(
    en='English',
    zhs='英语',
)
ui_extract_api_fail = _MS(
    en='Extracting API URL failed. Please retry after exiting the game.',
    zhs='提取 API URL 失败，请关闭游戏或重新查询抽卡信息后重试。',
)
ui_extract_api_fail_with_msg = _MS(
    en='Extracting API URL failed. Failed with: {}',
    zhs='提取 API URL 失败，遇到的问题：{}',
)
ui_extracting_api_url = _MS(
    en='Extracting API URL',
    zhs='正在提取 API URL',
)
ui_fine = _MS(en='Fine', zhs='好')
ui_fine1 = _MS(en='Fine', zhs='好的')
ui_fine2 = _MS(en='Fine', zhs='好吧')
ui_fps_is_already = _MS(
    en='FPS is already {}~',
    zhs='帧率已经是{}啦～',
)
ui_fps_is_set_to = _MS(
    en='FPS is successfully set to {}.',
    zhs='帧率已成功设置为{}。',
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
ui_is_latest_version = _MS(
    en='Your application is the latest version.',
    zhs='已经是最新版本啦',
)
ui_load_failure = _MS(en='Record Load Failed', zhs='加载失败')
ui_load_gacha = _MS(en='Import from JSON', zhs='导入数据')
ui_load_success = _MS(en='Record Load Success', zhs='加载成功')
ui_load_success_msg = _MS(
    en='Successfully loaded {cnt} items for uid {uid}.',
    zhs='成功导入了用户{uid}的{cnt}条记录。',
)
ui_locale = _MS(en='Display Language', zhs='显示语言')
ui_locale_setting_desc = _MS(en='Changing the display language', zhs='改变显示语言')
ui_no_data = _MS(en='No Data', zhs='暂无数据')
ui_not_good = _MS(en='No', zhs='不好')
ui_ooops = _MS(en='OOOPS!', zhs='出错了！')
ui_open_docs = _MS(en='Open Documentations', zhs='打开帮助页面')
ui_open_issues = _MS(en='Open Issue Page', zhs='打开反馈页面')
ui_open_repo = _MS(en='Open GitHub Repo', zhs='打开代码仓库')
ui_open_troubleshooting = _MS(en='Open Troubleshooting', zhs='打开常见问题')
ui_operation_zone = _MS(en='Operations', zhs='操作区')
ui_personalization = _MS(en='Personalization', zhs='个性化')
ui_reset_fps = _MS(
    en='Reset FPS',
    zhs='重置帧率',
)
ui_reset_panel = _MS(en='Reset Panel', zhs='重置面板')
ui_save_data = _MS(en='Save As', zhs='保存数据')
ui_save_failure = _MS(en='Data Save Failed', zhs='保存失败')
ui_save_success = _MS(en='Data Save Success', zhs='保存成功')
ui_save_success_msg = _MS(en='Data is saved to {}', zhs='数据已保存到{}')
ui_send_feedback = _MS(en='Send Feedback', zhs='提交反馈')
ui_send_feedback_desc = _MS(
    en='Feedback is welcome if you encounter problems or have suggestions.',
    zhs='如果你遇到问题，或对本项目有更多建议，欢迎提交反馈。',
)
ui_set_fps_fail_with_msg = _MS(
    en='Setting FPS failed. Failed with: {}',
    zhs='设置帧率失败，遇到的问题：{}',
)
ui_setting_failure = _MS(
    en='Error',
    zhs='设置失败',
)
ui_setting_panel = _MS(en='Setting Panel', zhs='设置面板')
ui_setting_restart_content = _MS(
    en='Please restart to apply changes.',
    zhs='请重启以应用新设置。',
)
ui_setting_restart_title = _MS(en='Success', zhs='设置成功')
ui_setting_success = _MS(en='Success', zhs='设置成功')
ui_settings = _MS(en='Settings', zhs='设置')
ui_since_last_guarantee = _MS(
    en='Since Last Guarantee',
    zhs='保底已垫',
)
ui_status_panel = _MS(en='Status Panel', zhs='状态面板')
ui_switch = _MS(en='Switch', zhs='切换')
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
ui_theme_mode = _MS(en='Theme Mode', zhs='应用主题')
ui_theme_mode_dark = _MS(en='Dark', zhs='深色')
ui_theme_mode_light = _MS(en='Light', zhs='浅色')
ui_theme_mode_settings_desc = _MS(
    en='Changing the appearance of application',
    zhs='改变应用外观',
)
ui_title = _MS(en='Honkai: Star Rail Toolkit', zhs='崩坏：星穹铁道工具箱')
ui_total_warp = _MS(en='Total Warp', zhs='总抽数')
ui_traceback = _MS(en='Traceback', zhs='报错信息')
ui_troubleshooting = _MS(en='TroubleShooting', zhs='常见问题')
ui_troubleshooting_desc = _MS(
    en='Click here to view FAQ.',
    zhs='点此查看常见问题解答。',
)
ui_unlock_fps = _MS(
    en='Unlock FPS Settings',
    zhs='解锁帧率',
)
ui_unlock_fps_desc = _MS(
    en=(
        'First set the frame rate in the game at least once, and then use the '
        'functions of this interface.'
    ),
    zhs='首先至少在游戏中设置一次帧率，再使用本页面中的功能。',
)
ui_update_available = _MS(
    en='New Version is Available',
    zhs='检查到新版本',
)
ui_update_desc = _MS(
    en=(
        'New Version of Honkai: Star Rail Toolkit is available. '
        'CHANGELOG: {}\n Please update to the latest version to experience '
        'the latest features. If the connectivity of GitHub is not good, '
        'it is recommended to download from the network disk distribution.'
    ),
    zhs=(
        '崩坏：星穹铁道工具箱有新的可用版本，更新日志：{}\n 请更新到最新版本以使用全新'
        '功能。如果你对GitHub的连接不稳定，请从网盘下载最新版本。'
    ),
)
ui_use_customize_url = _MS(en='Use Customize URL', zhs='使用自定义URL')
ui_users = _MS(en='Users', zhs='用户管理')
ui_users_desc = _MS(en='Multi-user management', zhs='如果有多个账号可以用这个切换')
ui_welcome = _MS(
    en='Welcome to HKSR Toolkit!',
    zhs='欢迎登车！',
)
ui_zhs = _MS(
    en='Simplified Chinese',
    zhs='简体中文',
)

# === END OF PRE-DEFINED VOCABULARIES ===
