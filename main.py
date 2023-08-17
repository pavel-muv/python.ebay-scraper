# Импортируем необходимые библиотеки
import requests
import time
import random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import openpyxl

# Определяем класс Product для хранения информации о товаре
class Product:
    def __init__(self):
        self.Name = ""  # Название товара
        self.Description = ""  # Описание товара
        self.PhotoLinks = []  # Список ссылок на фотографии товара

# Определяем функцию для получения данных страницы
def fetch_page_data(url):
    user_agent = UserAgent()
    headers = {
        "User-Agent": user_agent.random
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return None

# Основная функция
def main():
    base_url = input("Введите базовый URL: ")  # Пользователь вводит базовый URL
    page_number = 1  # Начинаем считать со второй страницы
    products = []  # Список для хранения товаров

    while True:
        url = f"{base_url}?_pgn={page_number}"  # Составляем URL страницы
        try:
            html = fetch_page_data(url)  # Получаем HTML-код страницы

            if html is None:
                break

            soup = BeautifulSoup(html, "html.parser")  # Создаем объект BeautifulSoup для парсинга

            print("Страница:", page_number)

            # Выводим количество найденных статей на странице
            print(len(soup.find_all('article')))

            for item in soup.find_all('article'):
                try:
                    # Получаем значение атрибута data-testid
                    data_testid_value = item.get('data-testid')
                    modified_data_testid_value = data_testid_value.replace("ig-", "")

                    # Создаем полный URL товара на eBay
                    url = f"https://www.ebay.com/itm/{modified_data_testid_value}"

                    # Получаем HTML-код страницы товара
                    html_item = fetch_page_data(url)

                    if html_item is None:
                        continue  # Пропускаем текущий товар, если не удалось получить HTML-код

                    # Создаем объект BeautifulSoup для парсинга страницы товара
                    soup_item = BeautifulSoup(html_item, "html.parser")

                    # Создаем объект товара
                    product = Product()

                    # Получаем название товара
                    title = soup_item.select_one(".x-item-title__mainTitle")
                    product.Name = title.get_text(strip=True) if title else ""

                    # Получаем описание и цену товара
                    price = soup_item.select_one(".x-price-primary")
                    product.Description = price.get_text(strip=True) if price else ""

                    # Получаем ссылки на фотографии товара
                    photo_links = []
                    image_items = soup_item.find_all('button')

                    for img_tag in image_items:
                        img = img_tag.find('img')
                        if img:
                            src_value = img.get('src')
                            if src_value:
                                try:
                                    # Заменяем размер изображения в ссылке
                                    new_src_value = src_value.replace("s-l64.jpg", "s-l1600.jpg").replace("l140.jpg",
                                                                                                          "s-l1600.jpg")
                                    photo_links.append(new_src_value)
                                except Exception as img_error:
                                    print("Error processing image:", img_error)

                    # Присваиваем список ссылок на фотографии объекту товара
                    product.PhotoLinks = photo_links

                    # Добавляем объект товара в список товаров
                    products.append(product)

                except Exception as e:
                    print("Error processing product:", e)



            # Поиск ссылки на следующую страницу
            next_page_link = soup.select("a.pagination__next")

            # Если ссылки нет, выходим из цикла
            if not next_page_link:
                break

            # Переходим на следующую страницу
            page_number += 1

            # Задержка между запросами
            delay = random.randint(10, 15)
            print(f"Пауза {delay} секунд перед следующей страницей...")
            time.sleep(delay)

        except requests.exceptions.RequestException as e:
            print("Error during page fetching:", e)
            print("Retrying the same page...")
            continue

    # Создаем новую рабочую книгу Excel
    wb = openpyxl.Workbook()

    # Получаем активный лист
    sheet = wb.active

    # Устанавливаем название листа
    sheet.title = "Products"

    # Добавляем заголовки колонок
    sheet.append(["Name", "Description", "PhotoLinks"])

    # Заполняем таблицу данными о товарах
    for product in products:
        # Преобразуем список ссылок в строку с переносами
        photo_links = "\n".join(product.PhotoLinks)

        # Добавляем данные товара в таблицу
        sheet.append([product.Name, product.Description, photo_links])

    # Сохраняем рабочую книгу в файл Excel
    wb.save("products.xlsx")

    print("Парсинг и экспорт в Excel завершены.")
    print("Получено элементов:", len(products))

    input("Нажмите Enter для завершения: ")

# Вызов функции main() при запуске скрипта
if __name__ == "__main__":
    main()
