#!/usr/bin/python

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

    for play in plays:
        print(play)

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

# Data, Nome da peça, horário da peça, local da peça, informações (tipo de peça etc.), link
class Play(object):
    def __init__(self, link):
        self.link = link

    def __str__(self):
        return self.link

if __name__ == '__main__':
    main()
