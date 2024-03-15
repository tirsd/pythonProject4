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
married = True
def charms (i):
    name = str(result.iloc[i]['name'])
    if "крест" in name or "христиан" in name or "икона" in name or "мусульман" in name or "спаси" in name or "сохрани" in name or "месяц" in name or "аллах" in name or "пророк" in name or "будда" in name or "отче" in name or "молитва" in name or "икона" in name or "лунниц" in name or "ангел" in name or "эрцгамм" in name or "чудо" in name or "фатим" in name or "иисус" in name or "б.м" in name or "давид" in name or "матрон" in name or "госп" in name or "хамс" in name:
        return "КУЛЬТ"
    else:
        return "ДЕКОР"
def bracs (link):
    url = f'https://www.wildberries.ru/catalog/{link}/detail.aspx'
    options_chrome = webdriver.ChromeOptions()
    options_chrome.add_argument('headless')
    browser = webdriver.Chrome(options=options_chrome)
    browser.get(url)
    time.sleep(1)
    soup = bs(browser.page_source, "html.parser")
    try:
        r = soup.find("span", attrs={'class':'sizes-list__size-ru'}).text
        if r.rfind("-") > -1:
            wei = r[r.rfind("-")+1:].strip().lower().replace(",",".").replace("гр.","").replace("гр","")
        elif r.rfind("~") > -1:
            wei = r[r.rfind("~")+1:].strip().lower().replace(",", ".").replace("гр.","").replace("гр","")
        elif r.rfind(" ") > -1:
            wei = r[r.rfind(" ")+1:].strip().lower().replace(",", ".").replace("гр.","").replace("гр","")
        wei = float(wei)
        if wei > 0 and wei < 15:
            return wei
    except:
        return np.nan
warnings.filterwarnings('ignore')
links=list()
spis = [143, 287, 431, 719, 1007, 1061, 1115, 1169, 1313, 1601, 1655, 1919, 2045, 2189,2405]
p=1
arts = list()
prices = list()
po = list()
date = list()
discount = list()
print("Введите ссылку:")
url = str(input())
url1 = url[:url.find("page=")+5]
url2 = url[url.find("&",url.find("page=")):]
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
        if str(art).find('price__lower-price wallet-price')>0:
            prl = art.findNext('ins',attrs={'class':'price__lower-price wallet-price'}).text.strip()[:-2]
            if prl.find('\xa0')>0:
                prl = prl.replace('\xa0','')
            prices.append(prl)
            po.append(math.ceil(int(prl)/0.95))
            discount.append(0.95)
        else:
            prl = art.findNext('ins',attrs={'class':'price__lower-price'}).text.strip()[:-2]
            if prl.find('\xa0')>0:
                prl = prl.replace('\xa0','')
            prices.append(prl)
            po.append(prl)
            discount.append(1)
    if p == 1:
        page_counts = int(soup.find(attrs={'data-link':'html{spaceFormatted:pagerModel.totalItems}'}).text.replace(' ',''))//100+1
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
    "oldprice":po
})
artsdf.to_csv("arts.csv")
artsdf = pd.read_csv("arts.csv")
arts = artsdf["link"]
prices = artsdf["price"]
po = artsdf["oldprice"]
for link in tqdm(arts):
    group = np.nan
    name = np.nan
    weight = np.nan
    lock_type = np.nan
    metal = np.nan
    insert = np.nan
    competitor = np.nan
    i = 0
    if int(link)//100000>spis[-1]:
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
        match basket['subj_name']:
            case "Ювелирные браслеты": group = "ЦБ БРАСЛЕТЫ"
            case "Ювелирные цепочки": group = "ЦБ ЦЕПИ"
            case "Ювелирные кольца": group = "КОЛЬЦА"
            case "Ювелирные подвески": group = "ПОДВЕС"
            case "Ювелирные серьги": group = "СЕРЬГИ"
    except:
        pass
    try:
        for option in basket['options']:
            if option['name'] == 'Минимальный вес (г)':
                weight = float(option['value'].replace('г',''))
            elif option['name'] == 'Вставка':
                insert = option['value']
            elif option['name'] == 'Вид замка':
                lock_type = option['value']
            elif option['name'] == 'Состав ювелирного изделия':
                metal = option['value']
    except:
        pass
    try:
        for option in basket['grouped_options'][0]['options']:
            if option['name'] == 'Минимальный вес (г)':
                weight = float(option['value'].replace('г',''))
            elif option['name'] == 'Вставка':
                insert = option['value']
            elif option['name'] == 'Вид замка':
                lock_type = option['value']
            elif option['name'] == 'Состав ювелирного изделия':
                metal = option['value'].lower()
    except:
        pass
    try:
        if np.isnan(weight) and group in ["ЦБ БРАСЛЕТЫ","ЦБ ЦЕПИ"]:
            weight = float(bracs(link))
    except:
        pass
    date.append(datetime.date.today())
    weights.append(weight)
    inserts.append(insert)
    metals.append(metal)
    locks.append(lock_type)
    competitors.append(competitor)
    names.append(name)
    groups.append(group)
if group == "КОЛЬЦА":
    print('Вас интересуют обручальные кольца?')
    mar = str(input())
    if len(mar.lower()) > 0 and mar not in ['да','yes','д','y']:
        married = False
result = pd.DataFrame({'data': date,
                       'competitor': competitors,
                       'name': names,
                       'group': groups,
                       'weight': weights,
                       'price': prices,
                       'price_old': po,
                       'discount': discount,
                       'insert': inserts,
                       'metal': metals,
                       'lock': locks,
                       'article': arts})
result.to_csv("result.csv",index=False)
result = pd.read_csv("result.csv")
groupdf = list()
ii = list()
avprice = list()
insertgroup = list()
charmgr = list()
result = result.drop(result["каучук" in result['insert'] or "жемчуг" in result['insert'] or "серебро" in result['metal'] or "каучук" in result['metal'] or "жемчуг" in result['metal'] or np.isnan(result['weight'])].index)
avgpr = result['price']/result['weight']
result.insert(loc=len(result.columns),column='Price per gramm',value=avgpr)
result = result.drop(result[result['Price per gramm']<3000].index)
result = result.drop(result[result['Price per gramm']>15000].index)
cat = np.where(result['Price per gramm']<=5500, "до 5500",
        np.where(
        (result['Price per gramm'] <= 6000), '5 500 руб. - 6 000 руб.',
        np.where(
        (result['Price per gramm'] <= 6500), '6 000 руб. - 6 500 руб.',
        np.where(
        (result['Price per gramm'] <= 7000), '6 500 руб. - 7 000 руб.',
        np.where(
        (result['Price per gramm'] <= 8000), '7 000 руб. - 8 000 руб.',
        np.where(
        (result['Price per gramm'] <= 9000), '8 000 руб. - 9 000 руб.',
        np.where(
        (result['Price per gramm'] <= 5500), '9 000 руб. -10 000 руб.',  'свыше 10 000 руб.'
        )))))))
result.insert(loc=len(result.columns),column='group_price',value=cat)
for i in tqdm(range(0,len(result))):
    insertgroup.append("")
    inss = str(result.iloc[i]['insert']).split(';')
    for ins in inss:
        ins = str(ins).strip().lower()
        if ins == "бриллиант" or ins == "сапфир" or ins =="рубин" or ins == "изумруд" or ins == "бриллиант натуральный" or ins == "сапфир натуральный" or ins == "рубин натуральный" or ins == "изумруд натуральный" or ins =="бриллианты" or ins == "":
            insertgroup[-1] = "ДК"
            charmgr.append('ДК')
            break
        elif ins == "фианит" or ins == "бриллиант искусственный" or ins == "бриллиант выращенный" or ins =="бриллианит" or ins == "бриллиант синтетический" or "фианит" in str(result.iloc[i]['insert']).lower():
            insertgroup[-1] = "ИФ"
            charmgr.append('ПДК')
        elif "нет" in ins or "без" in ins or  str(result.iloc[i]['insert']).lower().strip() == "золото" or str(result.iloc[i]['insert']).lower() == "эмаль" or ins == "nan":
            insertgroup[-1] = "БК"
            charmgr.append('БК')
            break
        elif "бр" in ins and "искусственный" not in str(result.iloc[i]['insert']).lower() and "выращенный" not in str(result.iloc[i]['insert']).lower() and "синтетический" not in str(result.iloc[i]['insert']).lower():
            insertgroup[-1] = "ДК"
            charmgr.append('ДК')
        elif insertgroup[-1] != "ИФ":
            insertgroup[-1] = "ПДК"
            charmgr.append('ПДК')
    if result.iloc[i]['group'] == "ПОДВЕС" and insertgroup[-1] in ['БК','ИФ']:
        insertgroup[-1] = insertgroup[-1] + " " + result.iloc[i]['group'] + " " + charms(i)
    elif result.iloc[i]['group'] == "ПОДВЕС":
        insertgroup[-1] = insertgroup[-1] + " " + result.iloc[i]['group']
    elif result.iloc[i]['group'] == "СЕРЬГИ":
        insertgroup[-1] = insertgroup[-1] + " " + result.iloc[i]['group']
    elif result.iloc[i]['group'] in ['ЦБ ЦЕПИ', 'ЦБ БРАСЛЕТЫ']:
        insertgroup[-1] = result.iloc[i]['group']
        charmgr[-1] = "ЦБ"
    elif result.iloc[i]['group'] == "КОЛЬЦА" and married:
        insertgroup[-1] = insertgroup[-1] + " " + result.iloc[i]['group'] + " " + "ОБРУЧ"
    elif result.iloc[i]['group'] == "КОЛЬЦА":
        insertgroup[-1] = insertgroup[-1] + " " + result.iloc[i]['group']
    else:
        ii.append(i)
if len(ii)>0:
    result= result.drop(labels=ii,axis=0)
result.insert(loc=len(result.columns),column='product_group(ТГ)',value=insertgroup)
result.insert(loc=len(result.columns),column='product_direction(ТН)',value=charmgr)
oldres = pd.read_excel(r'C:\Users\Petrov.Ilya\Downloads\wb.xlsx')
oldres = pd.concat([oldres,result],ignore_index=True)
oldres.to_excel(r'C:\Users\Petrov.Ilya\Downloads\wb.xlsx', index=False)