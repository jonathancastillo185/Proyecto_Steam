from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time



def fecha_lanzamiento(x):
    
    url = f'https://steamdb.info/app/{x}/info/'
    
    driver = webdriver.Chrome()
    
    driver.get(url)

    time.sleep(4)
    
    td_tags_with_span3 = driver.find_elements(By.XPATH, '//td[@class="span3"]')
    
    for td in td_tags_with_span3:
        if td.text == "Store Release Date":
            next_td = td.find_element(By.XPATH, 'following-sibling::td')
            if next_td:
                fecha = next_td.text
                driver.quit()
                fecha = fecha.split(' (')[0]
                return fecha



def limpiar_fecha(x):
    
    fecha_objeto = datetime.strptime(x, '%d %B %Y')

    fecha_formateada = fecha_objeto.strftime('%Y-%m-%d')

    return fecha_formateada



def extract(x): # ---> para desanidar los generos de games
    tags = []
    for x in x:
        tags.append(x)
    filtro = []
    for x in tags:
        for y in x.split(','):
            y = y.strip(" '[]'")
            filtro.append(y)
    return list(set(filtro))


def generos(x):
    url = x
    generos = []
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)

    a_tags_with_label_class = driver.find_elements(By.XPATH, '//a[contains(@class, "label-link label-color-0")]')

    for a_tag in a_tags_with_label_class:
        text = a_tag.text
        generos.append(text)
    driver.quit()
    
    return generos
    
    

def dumies_games(x): # ---> aca van los tags
    dicc = {}

    for x in list(x):
        dicc[x] = ''
        for y in df['tags']:
            if x in y:
                dicc[x] += '1'
            else:
                dicc[x] += '0'
    dicc1 = {}
    for x,e in dicc.items():
        dicc1[x] = [x for x in e]
        
    return pd.DataFrame(dicc1)
    