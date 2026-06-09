# 🧠 DailyMind — 每日跨领域思维食粮

> 不追踪 · 不算法 · 只为思考

每天晚 8 点，从**天文、地理、心理/社会、人文/社科、自然/哲学、科技**六个领域中**随机选取四个**，各选几篇文章，生成 AI 摘要和思考问题，推送到你的邮箱。

**中英双语信源：** 36氪、爱范儿、Solidot 等中文源 + ScienceDaily、New Scientist、Aeon 等英文源，每次推送都有中文内容。

---

## 快速开始

### 1. 下载

```bash
git clone https://github.com/你的用户名/DailyMind.git
cd DailyMind
```

或者直接下载 ZIP 解压。

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置邮箱

复制配置模板并编辑：

```bash
cp config.example.py config.py
```

编辑 `config.py`，填写你的邮箱信息：

```python
SMTP_CONFIG = {
    "host": "smtp.qq.com",           # QQ邮箱 / 163 / Gmail
    "user": "your_email@qq.com",     # 你的邮箱
    "password": "your_auth_code",    # SMTP 授权码（不是登录密码）
}
```

> **获取 QQ邮箱授权码：** 设置 → 账户 → POP3/IMAP/SMTP 服务 → 开启 → 生成授权码

### 4. 测试运行

```bash
python main.py
```

如果能收到邮件，说明配置成功！

### 5. 设置每晚 8 点自动运行

**方法一：Windows 任务计划程序（推荐）**

1. 按 `Win+R`，输入 `taskschd.msc`，回车
2. 右侧点「创建基本任务」
3. 名称：`DailyMind`，触发器：每天，时间：`20:00`
4. 操作：启动程序
   - 程序或脚本：`python`
   - 添加参数：`main.py`
   - 起始于：你的 DailyMind 文件夹路径
5. 完成

**方法二：一键脚本（需管理员权限）**

```powershell
.\install_task.ps1
```

---

## 升级使用 AI 摘要（推荐）

默认使用基于规则的摘要。配置 AI API 后，摘要质量会明显提升。

1. 在 [DeepSeek](https://platform.deepseek.com/) 注册 → 获取 API Key
2. 修改 `config.py`：
   ```python
   AI_CONFIG = {
       "enabled": True,
       "api_key": "sk-你的key",
   }
   ```
3. 成本：约 **0.001 元/次**，一年不到 5 毛钱

---

## 项目结构

```
DailyMind/
├── main.py                 # 主入口
├── config.example.py       # 配置模板（复制为 config.py 使用）
├── config.py               # 你的配置（已 gitignore，不上传）
├── digest.py               # AI / 规则摘要生成
├── mail_sender.py          # HTML 邮件发送
├── db.py                   # SQLite 去重
├── .gitignore
├── requirements.txt
├── install_task.ps1        # Windows 定时任务脚本
├── crawlers/
│   ├── base.py             # 爬虫基类 + RSS 解析器
│   ├── registry.py         # 随机选择机制
│   ├── astronomy.py        # 🌌 天文
│   ├── geography.py        # 🌍 地理
│   ├── psychology.py       # 🧠 心理/社会
│   ├── humanities.py       # 🎭 人文/社科
│   ├── nature_phil.py      # 🌿 自然/哲学
│   └── tech.py             # 🤖 科技
└── data/                   # 数据库和日志（自动生成，已 gitignore）
```

## 反茧房设计

- ✅ 每日随机选 4/6 个领域，不会只看同一个方向
- ✅ 每个领域多个信源，随机切换
- ✅ 不追踪用户偏好，无个性化算法
- ✅ 每篇文章配思考问题，引导主动思考
- ✅ 已推送文章自动去重，不再重复出现
- ✅ 中英双语信源混合，打破语言和信息茧房

## 自定义

想增减领域、信源或调整推送时间？编辑对应文件即可：

- **信源** → `crawlers/` 目录下各领域文件
- **推送时间** → 任务计划程序的触发器
- **推送数量** → `config.py` 里的 `RANDOM_DOMAINS_COUNT` 和 `ARTICLES_PER_DOMAIN`

## License

MIT