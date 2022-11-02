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

def scroll() -> None:
    driver.implicitly_wait(7)
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True

    
postgres_conn_id='postgres_default'
@dag(
    start_date=datetime(2022, 10, 10),
    max_active_runs=3,
    schedule_interval=None,
    catchup=False,
  
)

def get_produtos_leroy() -> Any:
    pg_hook = PostgresHook(postgres_conn_id=postgres_conn_id)

    lista_urls = []
    @task
    def paginacao():
        driver.implicitly_wait(7)
        for i in range(1,4):
            url = f'https://www.leroymerlin.com.br/search?term=tarkett&searchTerm=tarkett&searchType=default&page={i}'

            driver.get(url)
            time.sleep(3)
            scroll()
            try:
                urls_produtos = driver.find_elements(By.XPATH,'/html/body/div[6]/div[4]/div[1]/div[2]/div[3]/div/div/div/div[1]/a')
                for urls in urls_produtos:
                    lista_urls.append(urls.get_attribute('href'))
            except:
                print("error")

    @task
    def produtos_leroy():
        driver.implicitly_wait(7)
        for listas in lista_urls:
            try:
                driver.get(listas)
            
                dict_produtos = {}
                time.sleep(1)

                try:
                    nome_produto = driver.find_elements(By.XPATH,'/html/body/div[9]/div/div[1]/div[2]/div[1]/div[1]/h1')[0].text
                    dict_produtos['nomeproduto'] = nome_produto
                except:
                    print('erro')

                imagens = driver.find_elements(By.XPATH, '/html/body/div[9]/div/div[1]/div[1]/div[1]/div/div/div[2]/div[1]/div[2]/div/div/img')
                cont = 0
                for imagem in imagens:
                    dict_produtos['imagem'+str(cont)] = imagem.get_attribute('src')
                    cont +=1
                try:
                    categorias = driver.find_elements(By.XPATH, '/html/body/div[6]/div/ul[1]/li/a')
                    cont = 0
                    for categoria in categorias:
                        dict_produtos['categoria'+str(cont)] = categoria.get_attribute('title')
                        cont+=1

                except:
                    print("erro")

                try:
                    url_categoria = driver.find_elements(By.XPATH, '/html/body/div[6]/div/ul[1]/li/a')
                    cont=0
                    for urlsc in url_categoria:
                        dict_produtos['urlcategoria'+str(cont)] = urlsc.get_attribute('href')
                        cont+=1
                except:
                    print("erro")

                try:
                    descricao = driver.find_elements(By.XPATH,'/html/body/div[9]/div/div[1]/div[2]/div[2]/div/div[2]/div/div')
                    for descri in descricao:
                        dict_produtos['descricao'] = descri.text
                except:
                    print("erro")

                ref_key = driver.find_elements(By.XPATH,'/html/body/div[9]/div/div[4]/div[2]/table/tbody/tr/th')
                valor_esp = driver.find_elements(By.XPATH,'/html/body/div[9]/div/div[4]/div[2]/table/tbody/tr/td')
                cont = 0
                for val in ref_key:
                    dict_produtos[val.text] = valor_esp[cont].text
                    cont+=1

                referencias = driver.find_elements(By.XPATH,'/html/body/div[9]/div/div[1]/div[2]/div[1]/span')
                for ref in referencias:
                    if ref.get_attribute('itemprop') == 'mpn':
                        dict_produtos['MPN'] = ref.get_attribute('content')
                    
                    else:
                        pass

                print(dict_produtos)
            
                
                
            except:
                pass
    

    paginacao(produtos_leroy())

leroy = get_produtos_leroy()