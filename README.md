# python.ebay-scraper
eBay Seller Products Scraper

# eBay Seller Products Scraper

Этот скрипт представляет собой парсер, который собирает информацию о товарах продавца на eBay и сохраняет эту информацию в Excel-таблицу.

## Как работает скрипт

1. Сначала скрипт запрашивает у пользователя ввод базового URL продавца на eBay. Он будет использовать этот URL для поиска товаров продавца.

2. Скрипт начинает обходить страницы продавца, начиная с первой страницы. Он использует параметр `_pgn` в URL для перехода к следующим страницам.

3. Для каждой страницы продавца, скрипт делает HTTP-запрос, используя случайный User-Agent, чтобы избежать блокировки.

4. С помощью библиотеки BeautifulSoup, HTML-код страницы анализируется для поиска товаров (статей) на странице.

5. Для каждого товара, скрипт:
   - Получает атрибут `data-testid` элемента, чтобы определить уникальный идентификатор товара.
   - Составляет URL товара, используя этот уникальный идентификатор.
   - Получает HTML-код страницы товара и анализирует его снова с помощью BeautifulSoup.
   - Извлекает название и описание товара.
   - Находит кнопки с фотографиями товара, извлекает ссылки на фотографии и сохраняет их.
   - Создает объект `Product` и заполняет его данными.
   - Добавляет объект `Product` в список `products`.

6. Скрипт ищет ссылку на следующую страницу и повторяет процесс для следующей страницы, пока ссылки на следующие страницы существуют.

7. Все собранные данные о товарах сохраняются в Excel-таблицу. Для каждого товара, в таблице создается строка с названием товара, описанием и ссылками на фотографии.

## Как использовать скрипт

1. Убедитесь, что у вас установлены все необходимые библиотеки. Вы можете установить их, выполнив команду:

   ```
   pip install requests beautifulsoup4 fake-useragent openpyxl
   ```

2. Скачайте скрипт и сохраните его на вашем компьютере.

3. Запустите скрипт с помощью команды:

   ```
   python script_name.py
   ```

   Где `script_name.py` - это имя файла скрипта.

4. Введите базовый URL продавца на eBay, откуда вы хотите начать парсинг.

5. Скрипт начнет собирать информацию о товарах, обходя страницы продавца. В конце, он сохранит данные в Excel-таблицу.

6. Вы найдете результаты в файле `products.xlsx` в той же директории, где находится скрипт.

## Примечание

- При парсинге важно соблюдать политику сайта и не злоупотреблять частотой запросов, чтобы избежать блокировки.

- Для более сложных веб-сайтов, структуры HTML и CSS могут меняться, и скрипт может потребовать обновлений.

- Этот скрипт может служить примером базового веб-парсера. Вы можете модифицировать его и добавить дополнительные функции в соответствии с вашими потребностями.


---

Обратите внимание, что вы должны заменить `script_name.py` на фактическое имя файла скрипта. Это общее описание для файла README, и вы можете дополнить его в соответствии с вашими потребностями и особенностями проекта.