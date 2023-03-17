#!/usr/bin/python

import requests
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

def main():
    driver = webdriver.Chrome()
    driver.get('https://festivaldecuritiba.com.br/atracao/buscar/todas/')

    plays = []
    next_btn = get_page_next_btn(driver)

    has_next = True
    while has_next:
        plays.extend(get_page_plays(driver))
        scroll_element_to_center(driver, next_btn)
        driver.execute_script('arguments[0].click();', next_btn)
        next_btn = get_page_next_btn(driver)
        if not next_btn: has_next = False
    plays.extend(get_page_plays(driver))

    driver.close()

    for play in plays:
        print(play.link)
        play.scrape_content()

    df = pd.DataFrame([play.to_dict() for play in plays])
    df.to_excel('festival.xlsx', index=False)

def get_page_plays(driver: webdriver.Remote) -> list:
    content = get_element_by_id(driver, 'myTabContent')
    items = content.find_elements(By.TAG_NAME, 'li')
    links = [get_link(item) for item in items]
    return [Play(link) for link in links]

def get_page_next_btn(driver: webdriver.Remote) -> WebElement:
    icon = get_element_by_class(driver, 'icon-arrow_carrot-right')
    if icon:
        return icon.find_element(By.XPATH, '..')
    return None

def get_element_by_id(driver: webdriver.Remote, id_name: str, wait_time=10) -> WebElement:
    try:
        wait(driver, wait_time).until(EC.presence_of_element_located((By.ID, id_name)))
    except (NoSuchElementException, TimeoutException) as error:
        print(f"Elemento {id_name} não encontrado")
        return None
    return driver.find_element(By.ID, id_name)

def get_element_by_class(driver: webdriver.Remote, class_name: str, wait_time=10) -> WebElement:
    try:
        wait(driver, wait_time).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    except (NoSuchElementException, TimeoutException) as error:
        print(f"Elemento {class_name} não encontrado")
        return None
    return driver.find_element(By.CLASS_NAME, class_name)

def scroll_element_to_center(driver: webdriver.Remote, element: WebElement):
    scrollElementIntoMiddle = "var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);var elementTop = arguments[0].getBoundingClientRect().top;window.scrollBy(0, elementTop-(viewPortHeight/2));"
    driver.execute_script(scrollElementIntoMiddle, element)

def get_link(item: WebElement) -> str:
    return item.find_element(By.CLASS_NAME, 'attraction-link').get_attribute('href')

def make_request(url: str, wait_time=10, max_wait_time=160, panic_counter=0, max_panic_counter=10):
    response = requests.get(url)
    status_code = response.status_code

    if(status_code >= 400):
        print(f"Request para {url} com erro {status_code}.", endl=' ')
        if panic_counter >= max_panic_counter:
            print("PANICO!!! Abortando scraper...")
            quit()
        wt = min(wait_time, max_wait_time)
        print(f"Aguardando {wt} segundos...")
        time.sleep(wt)
        response = make_request(url, wait_time*2)
    return response

# Data, Nome da peça, horário da peça, local da peça, informações (tipo de peça etc.), link
class Play(object):
    def __init__(self, link):
        self.link = link

    def scrape_content(self):
        from bs4 import BeautifulSoup

        response = make_request(self.link)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.title = soup.find('h1').string
        self.date = " ".join(soup.find('label', attrs={'class': 'date-option'}).stripped_strings).upper()
        self.hour = soup.find('label', attrs={'class': 'date-tag'}).string
        self.place = " ".join(soup.find('div', attrs={'class': 'date-block'}).find('h6').stripped_strings)
        
        information = soup.find('div', attrs={'class': 'information'}).find_all('dl')
        self.genre = list(information[0].stripped_strings)[1]
        self.duration = list(information[1].stripped_strings)[1]
        self.event = list(information[2].stripped_strings)[1]
        self.classification = list(information[3].stripped_strings)[1]

    def to_dict(self):
        return {
            'Título': self.title,
            'Data': self.date,
            'Hora': self.hour,
            'Local': self.place,
            'Gênero': self.genre,
            'Duração': self.duration,
            'Evento/Mostra': self.event,
            'Classificação': self.classification,
            'Link': self.link
        }

if __name__ == '__main__':
    main()
