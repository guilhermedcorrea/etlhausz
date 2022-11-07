from airflow.decorators import dag, task
from datetime import datetime

import requests
import json
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
import re
import pandas as pd
from typing import Literal, List

options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument("--start-maximized")
options.add_argument('--disable-infobars')
driver = webdriver.Chrome(options=options, executable_path=r"/home/debian/etlhausz/chromedriver/chromedriver")

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

import requests
import json

url = 'https://www.deca.com.br/ambientes/banheiro-e-lavabo/acessorios-para-banheiro'


def get_testing_increase(ti):
    lista_dicts = []
    driver.get(r'https://www.deca.com.br/ambientes/banheiro-e-lavabo/acessorios-para-banheiro')
    urls = driver.find_elements(By.XPATH,'//*[@id="__next"]/div/div[3]/div/div/div[2]/div/div/div[2]/a')
    for url in urls:
               
        lista_dicts.append(url.get_attribute('href'))

    ti.xcom_push(key='testing_increase', value=lista_dicts)
    return lista_dicts

def analyze_testing_increases(ti):
   
    testing_increases=ti.xcom_pull(key='testing_increase', task_ids='get_testing_increase')
    for t in testing_increases:
        driver.get(t)
        print(t)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG('xcom_dag',
         start_date=datetime(2022, 10, 1),
         max_active_runs=2,
         schedule_interval=timedelta(minutes=30),
         default_args=default_args,
         catchup=False
         ) as dag:

    opr_get_covid_data = PythonOperator(
        task_id = 'get_testing_increase_data',
        python_callable=get_testing_increase,
        
    )

    opr_analyze_testing_data = PythonOperator(
        task_id = 'analyze_data',
        python_callable=analyze_testing_increases,
                
    )

    opr_get_covid_data >> opr_analyze_testing_data



