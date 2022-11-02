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
#options.add_argument("--headless")
#options.add_argument("--disable-gpu")
#options.add_argument('--disable-dev-shm-usage')
#options.add_argument('--no-sandbox')
options.add_argument("--start-maximized")
options.add_argument('--disable-infobars')
driver = webdriver.Chrome(options=options, executable_path=r"D:\produtoshausz\chromedriver\chromedriver.exe")


driver.get(r'https://www.rocaceramica.com.br/serie/alvor')

def get_descricao():
    descricao = driver.find_elements(By.XPATH,'/html/body/section[2]/div/div/div/p')
    for desc in descricao:
        print(desc.text)

def get_urls():
    lista_urls = []
    urls = driver.find_elements(By.XPATH,'/html/body/section[3]/div/div/a')
    for url in urls:
        lista_urls.append(url.get_attribute('href'))
    return lista_urls

def get_produtos():
    urls = get_urls()
    if isinstance(urls, list):
        for url in urls:
            driver.get(url)

            nome = driver.find_elements(By.XPATH,'/html/body/section[2]/div/div[2]/div[1]/div/h2')[0].text
            print(nome)

            codigo = driver.find_elements(By.XPATH,'/html/body/section[2]/div/div[2]/div[1]/div/div[1]/div[2]')[0].text
            print(codigo)

            tipo = driver.find_elements(By.XPATH,'/html/body/section[2]/div/div[2]/div[1]/div/div[1]/div[1]')[0].text
            print(tipo)
           

get_produtos()