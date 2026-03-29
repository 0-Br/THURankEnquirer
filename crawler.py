import time
import random
import pickle
from tqdm import tqdm

import pandas as pd
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

def enquery(id:str):
    ua = UserAgent()
    url = "https://www.wjx.cn/resultquery.aspx?activity=236297801"
    headers = {'User-Agent': ua.random}
    data = {'__VIEWSTATE': '/wEPDwUJMTg2NzQ1MjE2ZGS30+UikLSK+MuwKR5AiIUHwmUF7g==',
            '__VIEWSTATEGENERATOR': 'A51944F2',
            '__EVENTVALIDATION': '/wEdAATr5ZbWZIg0aXUsfbJVftFUfxLSikTZqx6XzQUk71djD7A88eHGsukWIJIFOXmn8igR0tAd5ZA4PMHE5c0EdNu88+EjKC0Ln8GN1BCwtINJsxzSPjo=',
            'hfPostType': '1',
            'hfQuery': '80000|' + id}

    response = requests.post(url, headers=headers, data=data)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.content, 'html.parser')
    div = soup.find("div", id="divContent")

    time_try = 0
    while div is None:
        time_try += 1
        if time_try > 30:
            return None
        time.sleep(5 * random.random())
        headers = {'User-Agent': ua.random}
        response = requests.post(url, headers=headers, data=data)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'html.parser')
        div = soup.find("div", id="divContent")

    data_items = div.find_all("div", class_="data__items")
    data = {}
    for item in data_items:
        title = item.find("div", class_="data__tit_cjd").get_text().strip()
        value = item.find("div", class_="data__key").get_text().strip()
        title = title[:-1]
        data[title] = value

    return data


if __name__ == "__main__":
    df = pd.read_csv('data\\namelist.csv', header=0)

    info = {}
    for index, row in tqdm(df.iterrows(), desc="Crawling...", total=len(df)):
        info[(row['学号'], row['姓名'])] = enquery(row['身份证号'])

    with open("data\\results.pkl", 'wb') as f:
        pickle.dump(info, f)
