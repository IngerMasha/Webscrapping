from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

edgedriver_path = r'C:\Users\inger\PycharmProjects\homeworck\edgedriver_win64\msedgedriver.exe'  # Замени на свой путь к msedgedriver.exe

options = Options()
options.add_argument("--start-maximized")  # Открыть браузер в полноэкранном режиме

service = Service(edgedriver_path)
driver = webdriver.Edge(service=service, options=options)

url = 'https://www.rottentomatoes.com/browse/tv_series_browse/sort:popular'
driver.get(url)

time.sleep(5)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

html = driver.page_source
driver.quit()

# Парсинг HTML с BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Найдем контейнеры с фильмами
movies = soup.find_all('a', class_='js-tile-link')

# Извлекаем данные о фильмах
movie_data = []

for movie in movies:
    title = movie.find('span', class_='p--small').text if movie.find('span', class_='p--small') else 'N/A'
    score = movie.find('span', class_='tMeterScore').text if movie.find('span', class_='tMeterScore') else 'N/A'
    release_date = movie.find('span', class_='p--xxs').text if movie.find('span', class_='p--xxs') else 'N/A'

    movie_data.append({
        'Title': title,
        'Score': score,
        'Release Date': release_date
    })

# Отображение данных в виде таблицы
df_movies = pd.DataFrame(movie_data)
print(df_movies)

# Сохраним данные в CSV-файл
df_movies.to_csv('rottentomatoes_movies_edge.csv', index=False)
