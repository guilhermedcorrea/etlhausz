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
import json

options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--start-maximized")
options.add_argument('--disable-infobars')
driver = webdriver.Chrome(options=options, executable_path=r"D:\produtoshausz\chromedriver\chromedriver.exe")

driver.get(r'https://www.deca.com.br/ambientes/banheiro-e-lavabo/acessorios-para-banheiro')

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
            
def get_urls():
    driver.implicitly_wait(7)
    pagina = driver.find_elements(By.XPATH,'/html/body/div[4]/div/div[3]/div/div/div[2]/nav/ul/li[4]/a')[0].text
    pagina = int(pagina)
    for i in range(1,pagina):
        url = 'https://www.deca.com.br/ambientes/banheiro-e-lavabo/acessorios-para-banheiro'+f'?&_page={i}'
      
        driver.get(url)
        try:
            urls = driver.find_elements(By.XPATH,'//*[@id="__next"]/div/div[3]/div/div/div[2]/div/div/div[2]/a')
            for url in urls:
                scroll()
                print(url.get_attribute('href'))
       
                time.sleep(1)
     
            pass
        except:
            pass

def get_produtos():
    driver.implicitly_wait(7)
    driver.get('https://www.deca.com.br/ambientes/banheiro-e-lavabo/assentos-sanitarios/assento-termofixo/Assento-Termofixo-com-Easy-Clean-e-Slow-Close-Flex-Branco-AP-386-17')
    time.sleep(2)

    scroll()
    time.sleep(1)
    json_produtos = driver.find_elements(By.CSS_SELECTOR,'#__NEXT_DATA__')
    for jsons in json_produtos:
        produto = json.loads(jsons.get_attribute('textContent'))
        item = produto.get('props')
        produto_item = item['pageProps']
        print(produto_item['product']['attributes'])
