from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

edgedriver_path = r'C:\Users\inger\PycharmProjects\homeworck\edgedriver_win64\msedgedriver.exe'  # Замени на свой путь к msedgedriver.exe
options = Options()
options.add_argument("--start-maximized")
service = Service(edgedriver_path)
driver = webdriver.Edge(service=service, options=options)

url = 'https://www.etsy.com/c/jewelry/handmade-jewelry'
driver.get(url)
time.sleep(5)
def extract_product_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    products = soup.find_all('li', class_='wt-list-unstyled')
    product_list = []

    for product in products:
        name = product.find('h3').text.strip() if product.find('h3') else 'N/A'
        price = product.find('span', class_='currency-value').text.strip() if product.find('span', class_='currency-value') else 'N/A'
        rating = product.find('span', class_='screen-reader-only').text.strip() if product.find('span', class_='screen-reader-only') else 'N/A'
        reviews = product.find('span', class_='text-body-smaller').text.strip() if product.find('span', class_='text-body-smaller') else 'N/A'

        product_list.append({
            'Product Name': name,
            'Price': price,
            'Rating': rating,
            'Number of Reviews': reviews
        })

    return product_list

all_products = []
while True:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'wt-list-unstyled'))
    )
    html = driver.page_source
    all_products.extend(extract_product_data(html))

    try:
        next_button = driver.find_element(By.CLASS_NAME, 'wt-action-group__item')
        if 'disabled' in next_button.get_attribute('class'):
            break
        next_button.click()
        time.sleep(5)
    except:
        break

driver.quit()

df = pd.DataFrame(all_products)
df.to_csv('handmade_jewelry_etsy.csv', index=False)

print("Scraping completed and data saved to 'handmade_jewelry_etsy.csv'")
