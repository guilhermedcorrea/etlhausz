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
from typing import Literal, List, Generator
import pandas as pd


options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--start-maximized")
options.add_argument('--disable-infobars')
driver = webdriver.Chrome(options=options, executable_path=r"D:\produtoshausz\chromedriver\chromedriver.exe")

driver.get('https://tarkett.com.br/categoria/piso-vinilico-lvt/linha-square')

time.sleep(1)


def scroll() -> None:
    
    driver.implicitly_wait(7)
        
    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
        
    while(match==False):
        lastCount = lenOfPage

        time.sleep(3)
        lenOfPage = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True


def descricao_linha() -> dict:
    dict_descricao: dict = {}
    try:
        nome_linha = driver.find_elements(By,
        '//*[@id="app"]/main/div[2]/div[1]/article/div[1]/h1')[0].text
        dict_descricao['linha'] = nome_linha
    except:
        pass
    
    try:
        descricao = driver.find_elements(By.XPATH,
        '//*[@id="app"]/main/div[2]/div[1]/article/div[2]')
        for descri in descricao:
            dict_descricao['descricao'] = descri.text
    except:
        pass

    return dict_descricao
  
def get_produtos() -> Generator[list, None, None]:
    lista_dicts: list  = []
    driver.implicitly_wait(7)
    scroll()
    referencias = driver.find_elements(By.XPATH,
    '//*[@id="cores"]/div/div/article/div[1]/div')
    for ref in referencias:
        dict_produtos: dict = {}

        skus = ref.text.split("\n")
        for sku in skus:
            if re.search('\d+',sku, re.IGNORECASE):
                try:
                    dict_produtos['codigoprodutoo'] = sku

                    dict_produtos['ulrbusca'] = 'https://tarkett.com.br/busca/' + sku
                except:

                    dict_produtos['codigoprodutoo'] = 'valor nao encontrado'

            if re.search('x|mm',sku, re.IGNORECASE):
                
                try:
                    dict_produtos['dimensoes'] = sku
                except:

                    dict_produtos['dimensoes'] = 'valor nao encontrado'

        descricao = descricao_linha()
        dict_produtos.update(descricao)

        try:
            download_ref = driver.find_elements(By.XPATH,
                                                '//*[@id="downloads"]/div/div/div/a/div/article')
            link_download = driver.find_elements(By.XPATH,
                                                 '//*[@id="downloads"]/div/div/div/a')
            cont = 0
            for download in download_ref:
                dict_produtos[download.text] = link_download[cont].get_attribute('href')
                cont +=1
        except:
            print("nao tem")

        conteudo_key = driver.find_elements(By.XPATH,'//*[@id="videos"]/div/div/div/p')
        conteudo_val = driver.find_elements(By.XPATH,'//*[@id="videos"]/div/div/div/iframe')
        cont = 0
        for conteudok in conteudo_key:
            dict_produtos[conteudok.text] = conteudo_val[cont].get_attribute('src')
            cont+=1
        lista_dicts.append(dict_produtos)

        referencia_key = driver.find_elements(By.XPATH,'//*[@id="masonry"]/div[1]/div/div[10]/div/p')
        referencia_val = driver.find_elements(By.XPATH,'//*[@id="masonry"]/div[1]/div/div/div/div/a/img')
        cont = 0
        for refk in referencia_key:
            dict_produtos[refk.text] = referencia_val[cont].get_attribute('src')
            cont +=1
         
    data = pd.DataFrame(lista_dicts)
    data.to_excel('descricao_tarkett.xlsx')

    yield lista_dicts
