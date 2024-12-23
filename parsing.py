import pandas as pd
import requests
import json
import praw
import nltk
import string
from tkinter import *
from tkinter import messagebox
from concurrent.futures import ThreadPoolExecutor
from nltk.corpus import stopwords
from collections import Counter
import re

# Загрузка стоп-слов
nltk.download('stopwords')
stop_words_ru = set(stopwords.words('russian'))  
stop_words_en = set(stopwords.words('english'))  

VK_TOKEN = 'your token (get it when creating the VK app)/// ваш токен (получите при создании приложения VK) '
VK_VERSION = '5.199'

# Константы Reddit API
REDDIT_CLIENT_ID = 'получите при создании приложения Reddit ///check out when creating a reddit app'
REDDIT_CLIENT_SECRET = 'получите при создании приложения Reddit ///check out when creating a reddit app'
REDDIT_USER_AGENT = 'RedditParser by /u/YOUR NAME'

def fetch_vk_posts(token, version, domain, count):
    try:
        response = requests.get(
            'https://api.vk.com/method/wall.get',
            params={
                'access_token': token,
                'v': version,
                'domain': domain,
                'count': count,
                'filter': 'owner'
            }
        )
        response.raise_for_status()
        response_data = response.json()

        if 'response' not in response_data:
            print("Ошибка VK: ", response_data)
            return None

        return response_data
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе VK API: {e}")
        return None

def fetch_reddit_posts(client_id, client_secret, user_agent, subreddit_name, post_count):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    for post in subreddit.hot(limit=post_count):
        if post.selftext.strip():
            posts.append({
                'title': post.title,
                'text': post.selftext,
                'score': post.score,
                'url': post.url,
                'num_comments': post.num_comments
            })
    return posts

def preprocess_text(text, language='ru'):
    #Обрабатывает текст: удаляет стоп-слова, пунктуацию, ссылки и прочее.
    text = text.lower()
    text = re.sub(r'http\S+', '', text)  
    text = re.sub(r'@\w+', '', text)     
    text = ''.join([char for char in text if char not in string.punctuation])  
    stop_words = stop_words_ru if language == 'ru' else stop_words_en  
    words = text.split()
    words = [word for word in words if word not in stop_words and word.isalpha()]  
    return words

def analyze_data(posts, top_n):
    #Анализирует данные: подсчитывает частотность слов и хэштегов.
    all_words = []
    hashtags = []
    for post in posts:
        text = post['text']
        language = detect_language(text)
        words = preprocess_text(text, language)

        all_words.extend(words)
        hashtags.extend([word for word in words if word.startswith('#')])

    word_freq = Counter(all_words).most_common(top_n)
    hashtag_freq = Counter(hashtags).most_common(top_n)

    return word_freq, hashtag_freq

def detect_language(text):
    russian_letters = sum(1 for char in text if 'а' <= char <= 'я' or 'А' <= char <= 'Я')
    english_letters = sum(1 for char in text if 'a' <= char <= 'z' or 'A' <= char <= 'Z')
    return 'ru' if russian_letters > english_letters else 'en'


def save_results(vk_data, reddit_data, analysis_results, save_parsed_data):
    if save_parsed_data:
        with open('all_parsed_data.json', 'w', encoding='utf-8') as file:
            json.dump({'vk': vk_data, 'reddit': reddit_data}, file, ensure_ascii=False, indent=4)

    with open('analysis_results.json', 'w', encoding='utf-8') as file:
        json.dump(analysis_results, file, ensure_ascii=False, indent=4)

def collect_data(vk_groups, reddit_subreddits, count_vk, count_reddit, top_n, save_parsed_data):
    with ThreadPoolExecutor() as executor:
        vk_futures = [executor.submit(fetch_vk_posts, VK_TOKEN, VK_VERSION, group.strip(), count_vk) for group in vk_groups]
        reddit_futures = [executor.submit(fetch_reddit_posts, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, subreddit.strip(), count_reddit) for subreddit in reddit_subreddits]

        vk_data = []
        for future in vk_futures:
            data = future.result()
            if data:
                vk_data.extend([
                    {
                        'text': item.get('text', ''),
                        'id': item.get('id', ''),
                        'likes': item.get('likes', {}).get('count', 0),
                        'comments': item.get('comments', {}).get('count', 0),
                        'reposts': item.get('reposts', {}).get('count', 0),
                        'views': item.get('views', {}).get('count', 0)
                    }
                    for item in data['response']['items']
                ])

        reddit_data = []
        for future in reddit_futures:
            data = future.result()
            if data:
                reddit_data.extend(data)

        word_freq, hashtag_freq = analyze_data(vk_data + reddit_data, top_n)

        save_results(vk_data, reddit_data, {'word_frequency': word_freq, 'hashtag_frequency': hashtag_freq}, save_parsed_data)

        messagebox.showinfo("Завершено", "Парсинг и анализ завершены. Результаты сохранены.")

def start_parsing():
    vk_groups = vk_groups_entry.get().split(',')
    reddit_subreddits = reddit_subreddits_entry.get().split(',')
    count_vk = int(vk_count_entry.get())
    count_reddit = int(reddit_count_entry.get())
    top_n = int(top_n_entry.get())
    save_parsed_data = save_parsed_data_var.get()

    collect_data(vk_groups, reddit_subreddits, count_vk, count_reddit, top_n, save_parsed_data)

root = Tk()
root.title("Парсер социальных сетей")

Label(root, text="Введите короткое имя группы VK (через запятую):").pack(pady=5)
vk_groups_entry = Entry(root, width=50)
vk_groups_entry.pack(pady=5)

Label(root, text="Количество постов VK:").pack(pady=5)
vk_count_entry = Entry(root, width=50)
vk_count_entry.pack(pady=5)

Label(root, text="Введите сабреддиты Reddit (через запятую):").pack(pady=5)
reddit_subreddits_entry = Entry(root, width=50)
reddit_subreddits_entry.pack(pady=5)

Label(root, text="Количество постов Reddit:").pack(pady=5)
reddit_count_entry = Entry(root, width=50)
reddit_count_entry.pack(pady=5)

Label(root, text="Количество популярных слов/хештегов для анализа:").pack(pady=5)
top_n_entry = Entry(root, width=50)
top_n_entry.pack(pady=5)

save_parsed_data_var = BooleanVar()
Checkbutton(root, text="Сохранять данные парсинга в JSON", variable=save_parsed_data_var).pack(pady=5)

Button(root, text="Запустить парсинг", command=start_parsing).pack(pady=20)

root.mainloop()
