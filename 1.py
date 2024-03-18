from selenium import webdriver
import time
import datetime
import math
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
import requests
import numpy as np
import openpyxl
import pandas as pd
import warnings
options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument('headless')
mwd2 = webdriver.Chrome(options=options_chrome)
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
warnings.filterwarnings('ignore')
links=list()
spis = [143, 287, 431, 719, 1007, 1061, 1115, 1169, 1313, 1601, 1655, 1919, 2045, 2189,2405]
p=1
arts = list()
prices = list()
po = list()
date = list()
discount = list()
otzs = list()
print("Введите ссылку:")
url = str(input())
url1 = url[:url.find("page=")+5]
url2 = url[url.find("&", url.find("page=")):]
mwd = webdriver.Chrome()
mwd.maximize_window()
while True:
    url = url1 + str(p) + url2
    mwd.get(url)
    time.sleep(1.5)
    step = 1900
    while True:
        step0=step-1900
        lh = mwd.execute_script("return document.body.scrollHeight")
        mwd.execute_script(f"window.scrollTo({step0}, {step});")
        time.sleep(1)
        nh = mwd.execute_script("return document.body.scrollHeight")
        step+=1900
        if nh==lh:
            break
    soup = bs(mwd.page_source, "html.parser")
    artss =  soup.find_all('article',id=True)
    for art in artss:
        arts.append(art['data-nm-id'])
    for art in artss:
        otz = np.nan
        try:
            ff = art.findNext('span',attrs={'class':'product-card__count'}).text
        except:
            pass
        try:
            if (ff.rfind(" "))>3:
                otz = ff[:ff.rfind(" ")].replace("\xa0", "")
            else:
                otz = int(ff[:ff.rfind(" ")])
        except:
            pass
        otzs.append(otz)
        if str(art).find('price__lower-price wallet-price')>0:
            prl = art.findNext('ins',attrs={'class':'price__lower-price wallet-price'}).text.strip()[:-2]
            if prl.find('\xa0')>0:
                prl = prl.replace('\xa0','')
            prices.append(prl)
            po.append(math.ceil(int(prl)/0.95))
            discount.append(0.95)
        else:
            prl = art.findNext('ins',attrs={'class': 'price__lower-price'}).text.strip()[:-2]
            if prl.find('\xa0')>0:
                prl = prl.replace('\xa0','')
            prices.append(prl)
            po.append(prl)
            discount.append(1)
    if p == 1:
        page_counts = int(soup.find(attrs={'data-link': 'html{spaceFormatted:pagerModel.totalItems}'}).text.replace(' ',''))//100+1
    if p == page_counts:
        break
    p+=1
mwd.close()
weights = list()
inserts = list()
metals = list()
locks = list()
competitors = list()
names = list()
groups =list()
artsdf = pd.DataFrame({
    "link":arts,
    "price":prices,
    "oldprice":po,
    "otzyv":otzs
})
artsdf.to_csv("arts.csv")
artsdf = pd.read_csv("arts.csv")
arts = artsdf["link"]
prices = artsdf["price"]
po = artsdf["oldprice"]
otzyvy = artsdf["otzyv"]
for link in tqdm(arts):
    group = np.nan
    name = np.nan
    weight = np.nan
    lock_type = np.nan
    metal = np.nan
    insert = np.nan
    competitor = np.nan
    i = 0
    if int(link)//100000 > spis[-1]:
        i = len(spis)
    else:
        while int(link)//100000 > spis[i]:
            i += 1
    i += 1
    if i < 10:
        i = "0"+str(i)
    current_link = f'https://basket-{i}.wbbasket.ru/vol{int(link)//100000}/part{int(link)//1000}/{link}/info/ru/card.json'
    try:
        basket = requests.get(current_link, verify=False, timeout=30).json()
    except:
        print(link)
        time.sleep(60)
        basket = requests.get(current_link, verify=False, timeout=30).json()
    try:
        competitor = basket['selling']['brand_name']
    except:
        pass
    try:
        name = basket['imt_name'].lower()
    except:
        pass
    try:
        for option in basket['options']:
            if option['name'] == 'Вес товара без упаковки (г)':
                weight = float(option['value'].replace('г',''))
            elif option['name'] == 'Тип меда':
                insert = option['value']
            elif option['name'] == 'Вкус':
                lock_type = option['value']
    except:
        pass
    try:
        if option['name'] == 'Вес товара без упаковки (г)':
            weight = float(option['value'].replace('г', ''))
        elif option['name'] == 'Тип меда':
            insert = option['value']
        elif option['name'] == 'Вкус':
            lock_type = option['value']

    except:
        pass
    date.append(datetime.date.today())
    weights.append(weight)
    inserts.append(insert)
    locks.append(lock_type)
    competitors.append(competitor)
    names.append(name)
    groups.append(group)
result = pd.DataFrame({'data': date,
                       'competitor': competitors,
                       'name': names,
                       'group': groups,
                       'weight': weights,
                       'price': prices,
                       'price_old': po,
                       'discount': discount,
                       'insert': inserts,
                       'otzyvy': otzyvy,
                       'lock': locks,
                       'article': arts})
result.to_csv("result.csv",index=False)
# adres = r'\\gold585.int\uk\Общее хранилище файлов\Служба аналитики\МЮР\tg_tn'.encode().decode('UTF-8')+r'\wildberries_' + str(datetime.date.today().day) + "_" + str(datetime.date.today().month) + "_" + str(datetime.date.today().year)+".xlsx"
# try:
#     oldres = pd.read_excel(adres)
# except:
#     oldres = pd.DataFrame()
# oldres = pd.concat([oldres,result],ignore_index=True)
# oldres.to_excel(adres, index=False)
adresm = "wildberries_"+ str(datetime.date.today().day) + "_" + str(datetime.date.today().month) + "_" + str(datetime.date.today().year)+" "+".xlsx"
try:
    oldresm = pd.read_excel(adresm)
except:
    oldresm = pd.DataFrame()
oldresm = pd.concat([oldresm,result],ignore_index=True)
oldresm.to_excel(adresm, index=False)