"""
摘要生成模块
==========
使用基于规则的方法生成文章摘要和思考引导问题。
如果配置了 AI API，则使用 AI 生成更优质的摘要。
"""

import random
import re
from config import AI_CONFIG

from crawlers.base import Article


# ==================== 各领域思考问题模板 ====================

THINKING_QUESTIONS = {
    "天文": [
        "如果宇宙有边界，边界之外是什么？",
        "人类在宇宙中是否孤独？这个问题的意义是什么？",
        "仰望星空时，我们看到的究竟是过去还是现在？",
        "如果有一天人类可以星际移民，文明会变成什么样？",
        "宇宙那么大，我们的烦恼还重要吗？",
    ],
    "地理": [
        "人类对地球的改造是进步还是破坏？",
        "如果地理大发现发生在今天，世界会如何不同？",
        "气候变化的背后，是人类文明的何种困境？",
        "一座城市的兴衰，折射出怎样的社会规律？",
        "你记忆中故乡的变化，背后是怎样的地理逻辑？",
    ],
    "心理": [
        "我们看到的「自己」，是真实的还是别人期望的？",
        "为什么人们总在重复同样的错误？",
        "快乐是一种可以追求的东西，还是一个副产品？",
        "人是理性的动物，还是理性的伪装者？",
        "我们活在自己的叙事里，还是别人的叙事里？",
    ],
    "社会": [
        "群体决策为什么往往不如个体理性？",
        "我们生活在信息时代，还是信息茧房？",
        "技术进步让社会更公平了，还是更分裂了？",
        "为什么人们热衷于站队和对立？",
        "一个好的社会，应该追求效率还是公平？",
    ],
    "人文": [
        "如果历史可以重来，文化会完全不同吗？",
        "一本书真的能改变一个人吗？改变的是什么？",
        "艺术的价值在于表达还是在于共鸣？",
        "在快节奏的时代，慢阅读还有意义吗？",
        "人类文明的进步，是线性的还是循环的？",
    ],
    "社科": [
        "文明之间的冲突，本质上是价值观的冲突吗？",
        "数据越多，我们就越了解社会吗？",
        "消费主义是自由的体现，还是新的枷锁？",
        "城市让人的生活更好了，还是更孤独了？",
        "我们今天的生活方式，一百年后的人会怎么看？",
    ],
    "自然": [
        "人类是自然的一部分，还是自然的破坏者？",
        "物种灭绝是自然规律，还是人类的罪过？",
        "如果蜜蜂消失了，人类能活多久？",
        "自然界的秩序是设计出来的还是涌现出来的？",
        "科技能解决环境问题，还是只会让问题更糟？",
    ],
    "哲学": [
        "意识是什么？它能否被还原为物理过程？",
        "人类真的拥有「自由意志」吗？",
        "如果宇宙遵循物理定律，那「偶然」是否存在？",
        "人生的意义是自己赋予的，还是本来就有的？",
        "你相信的「真理」，换一个文化背景还成立吗？",
    ],
    "科技": [
        "技术让生活更好了，还是让生活更复杂了？",
        "人工智能会取代人类的工作，还是取代无聊的工作？",
        "我们是在使用工具，还是工具在使用我们？",
        "科技发展越快，人类就越幸福吗？",
        "如果有一天AI有了意识，它应该拥有权利吗？",
    ],
    "经济": [
        "经济增长是无限的，还是有其自然边界？",
        "钱能买到幸福吗？如果能，买到哪一步？",
        "为什么有人辛勤工作却依然贫穷？",
        "消费主义是经济增长的动力，还是环境的代价？",
        "如果AI取代了大量工作，经济体系会怎么变？",
    ],
}


def _extract_key_sentences(text: str, max_sentences: int = 4) -> str:
    """从文本中提取关键句子作为摘要"""
    # 按句号、问号、感叹号、换行分割
    sentences = re.split(r'[。！？\n]', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

    if not sentences:
        return text[:200]

    if len(sentences) <= max_sentences:
        return "。".join(sentences) + "。"

    # 选前 1-2 句 + 后 1 句 + 中间随机 1 句
    selected = []
    selected.append(sentences[0])
    if len(sentences) > 2:
        selected.append(sentences[1])
    if len(sentences) > 4:
        selected.append(sentences[-2])
    if len(sentences) > 5:
        middle = sentences[len(sentences) // 2]
        if middle not in selected:
            selected.append(middle)

    return "。".join(selected[:max_sentences]) + "。"


def _generate_thinking_question(domain: str, title: str = "") -> str:
    """为某个领域生成一个思考引导问题"""
    questions = THINKING_QUESTIONS.get(domain, [
        "这篇文章给你最大的启发是什么？",
        "你能用一句话向别人介绍这个观点吗？",
        "如果把这个道理用在生活中，会怎样？",
    ])
    return random.choice(questions)


def generate_digest(articles: list[Article]) -> list[Article]:
    """
    为文章列表生成摘要和思考问题。
    目前使用基于规则的方法，配置了 AI 则调用 AI。
    """
    if AI_CONFIG.get("enabled") and AI_CONFIG.get("api_key"):
        return _generate_digest_ai(articles)
    else:
        return _generate_digest_rule(articles)


def _generate_digest_rule(articles: list[Article]) -> list[Article]:
    """基于规则的摘要生成"""
    for article in articles:
        # 如果有原始摘要且足够长，直接用
        if len(article.summary) > 50:
            article.summary = article.summary[:300]
        else:
            # 否则从标题生成
            article.summary = f"今日{article.domain}领域精选文章：{article.title}。"

        # 生成思考问题
        article.thinking_question = _generate_thinking_question(
            article.domain, article.title
        )

    return articles


def _generate_digest_ai(articles: list[Article]) -> list[Article]:
    """使用 AI API 生成摘要"""
    try:
        import httpx

        api_key = AI_CONFIG["api_key"]
        api_base = AI_CONFIG["api_base"]
        model = AI_CONFIG["model"]

        for article in articles:
            prompt = (
                f"你是DailyMind的摘要助手。请为以下文章生成：\n"
                f"1. 一篇200字以内的中文摘要，要求引人思考、有一定深度\n"
                f"2. 一个启发性的思考问题（引导读者深入思考）\n\n"
                f"标题：{article.title}\n"
                f"领域：{article.domain}\n"
                f"链接：{article.url}\n"
                f"原文摘要：{article.summary[:500] if article.summary else '无'}\n\n"
                f"请按以下格式回复：\n"
                f"【摘要】\n"
                f"（摘要内容）\n\n"
                f"【思考】\n"
                f"（思考问题）"
            )

            resp = httpx.post(
                f"{api_base}/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 500,
                },
                timeout=30,
            )
            resp.raise_for_status()
            result = resp.json()
            content = result["choices"][0]["message"]["content"]

            # 解析返回内容
            summary_part = ""
            question_part = ""
            if "【摘要】" in content and "【思考】" in content:
                parts = content.split("【思考】")
                summary_part = parts[0].replace("【摘要】", "").strip()
                question_part = parts[1].strip() if len(parts) > 1 else ""
            else:
                summary_part = content[:300]
                question_part = _generate_thinking_question(article.domain)

            article.summary = summary_part[:400]
            article.thinking_question = question_part

    except Exception as e:
        print(f"[AI 摘要生成失败，降级到规则模式] {e}")
        return _generate_digest_rule(articles)

    return articles