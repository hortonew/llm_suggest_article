import os
import pickle
import time

import requests
from bs4 import BeautifulSoup

CACHE_PATH = "articles_cache.pkl"
CACHE_TIMEOUT = 1800  # 30 minutes
PAGE_COUNT = 2 # how many HN pages to pull articles from

def fetch_articles_on_page(page):
    base_url = 'https://news.ycombinator.com/'
    url = f'{base_url}news?p={page}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.find_all('tr', class_='athing')

def extract_article_data(article):
    if title_tag := article.find('a', rel='noreferrer'):
        title = title_tag.text
        article_url = title_tag['href']
        return (title, article_url)
    return None

def get_articles_across_pages() -> list[str]:
    article_data = []
    for page in range(1, PAGE_COUNT+1):
        articles = fetch_articles_on_page(page)
        for article in articles:
            if data := extract_article_data(article):
                article_data.append(data)

    return [f"{title} - {url}" for title, url in article_data]

def write_article_cache(articles: list[str]):
    with open(CACHE_PATH, 'wb') as f:
        pickle.dump(articles, f)

def is_cache_valid():
    if os.path.exists(CACHE_PATH):
        file_mtime = os.path.getmtime(CACHE_PATH)
        current_time = time.time()
        return current_time - file_mtime <= CACHE_TIMEOUT
    return False

def fetch_or_load_articles() -> list[str]:

    if is_cache_valid():
        with open(CACHE_PATH, 'rb') as f:
            print("Loaded articles from cache since it hasn't been 30m")
            articles = pickle.load(f)
    else:
        print("Reached out to HN for articles.")
        articles = get_articles_across_pages()
        write_article_cache(articles=articles)
    
    return articles
