"""
DailyMind 配置模板
=================
使用前请复制此文件为 config.py，然后填写你的信息。
"""

# ==================== 邮箱配置 ====================
# 使用 QQ邮箱 / 163 / Gmail 等 SMTP 服务
# QQ邮箱需要开启 SMTP 服务并使用授权码（不是登录密码）
# 开启方式：QQ邮箱 -> 设置 -> 账户 -> POP3/IMAP/SMTP -> 开启 -> 生成授权码

SMTP_CONFIG = {
    "host": "smtp.qq.com",          # SMTP 服务器
    "port": 465,                    # SSL 端口（QQ邮箱/163用465，Gmail用587）
    "user": "your_email@qq.com",    # 你的邮箱
    "password": "your_auth_code",   # SMTP 授权码
}

TO_EMAIL = "your_email@qq.com"      # 接收邮件的地址


# ==================== AI 摘要配置 (可选) ====================
# 启用后摘要质量更好。DeepSeek: https://platform.deepseek.com/
# 不启用则用基于规则的摘要

AI_CONFIG = {
    "enabled": False,                # True 启用 AI 摘要
    "provider": "deepseek",
    "api_key": "",                  # DeepSeek API Key
    "api_base": "https://api.deepseek.com",
    "model": "deepseek-chat",
}


# ==================== 运行配置 ====================
# 每天从10个领域中随机选 N 个领域推送（建议5-6个）
RANDOM_DOMAINS_COUNT = 5

# 每个领域最多选几篇文章（建议1-2篇）
ARTICLES_PER_DOMAIN = 2

# 只抓取最近 N 天内的文章（新鲜度控制）
MAX_DAYS = 3