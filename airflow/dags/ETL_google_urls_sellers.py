from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator, PostgresHook
from airflow.utils.task_group import TaskGroup
from typing import Any
from datetime import datetime, timedelta
import json
from airflow.decorators import dag, task
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
import re
import pandas as pd
from typing import Literal, List, Generator
from itertools import chain
from airflow.operators.python import PythonOperator


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options, executable_path=r"/home/debian/etlhausz/chromedriver/chromedriver")

postgres_conn_id='postgres_default'
@dag(
    start_date=datetime(2022, 10, 10),
    max_active_runs=3,
    schedule_interval=None,
    catchup=False,
  
)

def get_urls_googleshopping() -> Any:
    pg_hook = PostgresHook(postgres_conn_id=postgres_conn_id)
    @task
    def search_products() -> Generator[list, None, None]:
        lista_dicts: list = []
        driver.implicitly_wait(7)
        data = pd.read_excel(r"/home/debian/etlhausz/excelfiles/google.xlsx")
        dicts = data.to_dict('records')
        for dic in dicts:
            time.sleep(3)
            driver.get(r'https://shopping.google.com.br')

            time.sleep(3)
            try:
                search = driver.find_element(By.XPATH,'//*[@id="REsRA"]')
                search.clear()
                search.send_keys(dic['EAN'])
            except:
                print("erro busca ean")
            try:
                busca = driver.find_element(By.XPATH,'//*[@id="kO001e"]/div/div/c-wiz/form/div[2]/div[1]/button/div/span').click()
            except:
                print("erro busca")
            time.sleep(1)
            try:
                google_url = driver.find_elements(By.XPATH,'//*[@id="rso"]/div/div[2]/div/div[1]/div[1]/div[2]/div[3]/div/a')
                urlgoogle = [url.get_dom_attribute('href') for url in google_url]
                if len(urlgoogle) <= 10:
                    google_url = driver.find_elements(By.XPATH, '//*[@id="rso"]/div/div[2]/div/div/div[1]/div[2]/span/a')
                    urlgoogle = [url.get_dom_attribute('href') for url in google_url]
            except:
                print("valor invalido")

            if next(map(lambda k: k if len(k) >=200 else(k if type(k) == str else 'valorinvalido'),urlgoogle),None):

                dict_item: dict = {}
                if urlgoogle !='valorinvalido' or urlgoogle != None:
                    dict_item['URLGOOGLE'] = next(chain(urlgoogle))
                    dict_item['EAN'] = dic['EAN']
                    dict_item['NOMEPRODUTO'] = dic['NomeProduto']
                    dict_item['Marca'] = dic['Marca']
                    dict_item['SKU'] = dic['SKU']
                    dict_item['IDPRODUTO'] = dic['IdProduto']
                    lista_dicts.append(dict_item)
                    print(dict_item)
                
        df = pd.DataFrame(lista_dicts)
        df.to_excel('googleshoppingurls.xlsx')

    search_products()
    
googleurls = get_urls_googleshopping()