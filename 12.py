import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
cookies = {
    'BasketUID': 'bbafdac817134550879803140f90f53e',
    '__wba_s': '1',
    '___wbu': '4c35dbee-d5c2-461f-9480-9111c9763572.1710691725',
    '___wbs': 'ac29aa35-bd6c-49ee-8bcb-39fc003ffbd2.1710691725',
    '_wbauid': '4766783781710691728',
}

headers = {
    'authority': 'www.wildberries.ru',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': 'BasketUID=bbafdac817134550879803140f90f53e; __wba_s=1; ___wbu=4c35dbee-d5c2-461f-9480-9111c9763572.1710691725; ___wbs=ac29aa35-bd6c-49ee-8bcb-39fc003ffbd2.1710691725; _wbauid=4766783781710691728',
    'referer': 'https://www.google.com/',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}
url = f'https://www.wildberries.ru/catalog/167961444/detail.aspx'
options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument('headless')
mwd = webdriver.Chrome(options=options_chrome)
mwd.get(url)
time.sleep(0.7)
soup = bs(mwd.page_source, 'html.parser')
ff = soup.find('span', class_='product-review__count-review j-wba-card-item-show j-wba-card-item-observe')
print(ff)