import feedparser
import os
from datetime import datetime
from pathlib import Path

def fetch_news(rss_urls):
    for url in rss_urls:
        feed = feedparser.parse(url)
        source_name = feed.feed.title
        
        # Создаем директорию для текущей даты
        today = datetime.now().strftime('%Y-%m-%d')
        news_dir = Path('news') / today
        news_dir.mkdir(parents=True, exist_ok=True)
        
        # Создаем markdown файл для каждой новости
        for entry in feed.entries[:10]:  # Берем первые 10 новостей
            title = entry.title
            link = entry.link
            try:
                description = entry.description
            except AttributeError:
                description = 'Нет описания'
            
            # Создаем безопасное имя файла
            safe_title = ''.join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title[:50]  # Ограничиваем длину
            
            file_path = news_dir / f'{safe_title}.md'
            
            # Создаем содержимое markdown файла
            content = f"""---
title: {title}
source: {source_name}
date: {today}
link: {link}
---

{description}

[Читать оригинал]({link})"""
            
            # Записываем файл
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == '__main__':
    # Список RSS-фидов для сбора новостей
    rss_urls = [
        'https://lenta.ru/rss',
        'https://www.vedomosti.ru/rss/news',
        'https://tass.ru/rss/v2.xml'
    ]
    
    fetch_news(rss_urls)