from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

# Укажи путь к Edge WebDriver (замени на свой путь)
edgedriver_path = r'C:\Users\inger\PycharmProjects\homeworck\edgedriver_win64\msedgedriver.exe'  # Замени на свой путь к msedgedriver.exe

# Настройка параметров для Edge
options = Options()
options.add_argument("--start-maximized")  # Открываем браузер в полноэкранном режиме

# Запуск драйвера Edge
service = Service(edgedriver_path)
driver = webdriver.Edge(service=service, options=options)

# URL новостной страницы (замени на нужный сайт)
url = 'https://www.bbc.com/news'

# Переход на страницу
driver.get(url)
time.sleep(5)  # Ждем загрузки динамического контента

# Прокрутка страницы вниз для загрузки всех новостей (если нужно)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

# Извлекаем HTML-код страницы
html = driver.page_source
driver.quit()

# Парсинг HTML с BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Поиск новостных статей (классы могут отличаться на других сайтах)
articles = soup.find_all('div', class_='gs-c-promo')  # Проверим класс на сайте

# Извлекаем заголовки и даты публикации
news_data = []

for article in articles:
    title_tag = article.find('h3')
    date_tag = article.find('time')

    title = title_tag.text.strip() if title_tag else 'N/A'
    date = date_tag['datetime'] if date_tag and 'datetime' in date_tag.attrs else 'N/A'

    news_data.append({
        'Title': title,
        'Publication Date': date
    })

# Преобразуем данные в DataFrame
df_news = pd.DataFrame(news_data)
print(df_news)

# Функция для извлечения месяца из даты публикации
def get_publication_month(date_str):
    if date_str != 'N/A':
        date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        return date_obj.strftime('%B')  # Преобразуем в название месяца (например, 'January')
    return 'Unknown'

# Применяем функцию для добавления месяца публикации
df_news['Publication Month'] = df_news['Publication Date'].apply(get_publication_month)

# Группируем статьи по месяцам
grouped_articles = df_news.groupby('Publication Month')['Title'].apply(list).to_dict()

# Выводим результат
for month, titles in grouped_articles.items():
    print(f"\n{month}:")
    for title in titles:
        print(f" - {title}")

df_news.to_csv('categorized_news_articles.csv', index=False)
