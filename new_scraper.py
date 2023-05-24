from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

# URL dos Exoplanetas da NASA
START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

# Webdriver
browser = webdriver.Chrome("D:/Setup/chromedriver_win32/chromedriver.exe")
browser.get(START_URL)

time.sleep(10)

new_data = []

def scrape_more_data(hyperlink):
    print('hyperlink')
    try:
        page=requests.get(hyperlink)
        soup=BeautifulSoup(page.content,'html.parser')
        temp_list=[]
        for tr_tag in soup.find_all('tr',attrs={'class':'fact_row'}):
            td_tags=tr_tag.find_all('td')
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all('div',attrs={'class':'value'})
                                     [0].contents[0])
                except:
                    temp_list.append('')
        new_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)
# Remova o caractere '\n' dos dados coletados
scraped_data = []

for row in new_data:
    replaced = []
    ## ADICIONE O CÓDIGO AQUI ##
    for el in row:
        el=el.replace('\n','')
        replaced.append(el)
    
    scraped_data.append(replaced)

print(scraped_data)

headers = ['Star_name','Distance','Mass','Radius']

df_1 = pd.DataFrame(scraped_data,columns = headers)

# Converta para CSV
df_1.to_csv('new_scraped_data.csv', index=True, index_label="id")
