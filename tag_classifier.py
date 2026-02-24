# Tag Classifier 模块 - 负责文章标签分类
import re


# 定义标签关键词
TAG_KEYWORDS = {
    "AI": [
        "ai", "artificial intelligence", "machine learning", "ml", "deep learning",
        "neural network", "gpt", "llm", "chatgpt", "openai", "anthropic", "claude",
        "transformer", "model", "training", "inference", "embedding", "vector"
    ],
    "Web": [
        "web", "html", "css", "javascript", "js", "react", "vue", "angular",
        "frontend", "backend", "fullstack", "http", "api", "rest", "graphql",
        "browser", "dom", "node", "deno", "bun"
    ],
    "DevOps": [
        "devops", "docker", "kubernetes", "k8s", "ci/cd", "jenkins", "github actions",
        "deployment", "infrastructure", "terraform", "ansible", "monitoring",
        "prometheus", "grafana", "logging", "cloud", "aws", "azure", "gcp"
    ],
    "Database": [
        "database", "db", "sql", "nosql", "postgres", "mysql", "mongodb",
        "redis", "elasticsearch", "query", "index", "schema", "migration"
    ],
    "Security": [
        "security", "vulnerability", "exploit", "hack", "breach", "encryption",
        "authentication", "authorization", "oauth", "jwt", "ssl", "tls", "https",
        "password", "privacy", "gdpr"
    ],
    "Programming": [
        "python", "java", "c++", "rust", "go", "golang", "typescript", "swift",
        "kotlin", "ruby", "php", "scala", "haskell", "elixir", "clojure",
        "programming", "code", "coding", "algorithm", "data structure"
    ],
    "Mobile": [
        "mobile", "ios", "android", "app", "flutter", "react native",
        "swift", "kotlin", "mobile app"
    ],
    "Startup": [
        "startup", "founder", "entrepreneur", "vc", "venture capital",
        "funding", "investment", "business", "saas", "product launch"
    ],
    "Open Source": [
        "open source", "oss", "github", "gitlab", "contribution", "maintainer",
        "license", "mit", "apache", "gpl"
    ],
    "Performance": [
        "performance", "optimization", "speed", "latency", "throughput",
        "benchmark", "profiling", "caching", "scalability"
    ],
    "Tools": [
        "tool", "cli", "command line", "terminal", "editor", "ide",
        "vscode", "vim", "emacs", "productivity"
    ],
    "Science": [
        "science", "research", "paper", "study", "experiment", "physics",
        "biology", "chemistry", "mathematics", "quantum"
    ]
}


def classify_article(title: str, url: str = "") -> list[str]:
    """
    根据标题和URL对文章进行分类
    
    参数:
        title: 文章标题
        url: 文章URL（可选）
    
    返回:
        标签列表
    """
    tags = []
    text = (title + " " + url).lower()
    
    for tag, keywords in TAG_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                tags.append(tag)
                break  # 找到一个关键词就够了
    
    # 如果没有匹配到任何标签，返回"Other"
    if not tags:
        tags.append("Other")
    
    return tags


def add_tags_to_article(article: dict) -> dict:
    """
    为文章添加标签
    
    参数:
        article: 文章字典，包含 title, url, score, comments
    
    返回:
        添加了 tags 字段的文章字典
    """
    article["tags"] = classify_article(article["title"], article.get("url", ""))
    return article


def group_articles_by_tag(articles: list[dict]) -> dict[str, list[dict]]:
    """
    按标签分组文章
    
    参数:
        articles: 文章列表
    
    返回:
        标签到文章列表的映射
    """
    grouped = {}
    
    for article in articles:
        if "tags" not in article:
            article = add_tags_to_article(article)
        
        for tag in article["tags"]:
            if tag not in grouped:
                grouped[tag] = []
            grouped[tag].append(article)
    
    return grouped


def get_tag_statistics(articles: list[dict]) -> dict[str, int]:
    """
    统计各标签的文章数量
    
    参数:
        articles: 文章列表
    
    返回:
        标签到数量的映射
    """
    tag_counts = {}
    
    for article in articles:
        if "tags" not in article:
            article = add_tags_to_article(article)
        
        for tag in article["tags"]:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    # 按数量降序排序
    return dict(sorted(tag_counts.items(), key=lambda x: x[-1], reverse=True))


def format_tags_for_display(tags: list[str]) -> str:
    """
    格式化标签用于显示
    
    参数:
        tags: 标签列表
    
    返回:
        格式化的标签字符串
    """
    if not tags:
        return ""
    
    # 使用emoji和颜色标记
    tag_emojis = {
        "AI": "🤖",
        "Web": "🌐",
        "DevOps": "⚙️",
        "Database": "💾",
        "Security": "🔒",
        "Programming": "💻",
        "Mobile": "📱",
        "Startup": "🚀",
        "Open Source": "📂",
        "Performance": "⚡",
        "Tools": "🔧",
        "Science": "🔬",
        "Other": "📌"
    }
    
    formatted_tags = []
    for tag in tags:
        emoji = tag_emojis.get(tag, "🏷️")
        formatted_tags.append(f"{emoji} {tag}")
    
    return " | ".join(formatted_tags)


if __name__ == "__main__":
    # 测试示例
    test_articles = [
        {"title": "Show HN: I built an AI chatbot using GPT-4", "url": "https://example.com"},
        {"title": "Optimizing React performance with lazy loading", "url": "https://example.com"},
        {"title": "How we scaled our Kubernetes cluster to 10k pods", "url": "https://example.com"},
        {"title": "PostgreSQL query optimization tips", "url": "https://example.com"},
        {"title": "Security vulnerability in popular npm package", "url": "https://example.com"},
    ]
    
    print("标签分类测试：")
    print("=" * 50)
    for article in test_articles:
        tags = classify_article(article["title"], article["url"])
        print(f"\n标题: {article['title']}")
        print(f"标签: {format_tags_for_display(tags)}")
