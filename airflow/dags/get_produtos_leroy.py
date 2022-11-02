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
from typing import Literal, List

options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--start-maximized")
options.add_argument('--disable-infobars')
driver = webdriver.Chrome(options=options, executable_path=r"D:\produtoshausz\chromedriver\chromedriver.exe")

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
            
lista_urls = []
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
