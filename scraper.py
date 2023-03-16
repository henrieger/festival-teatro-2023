#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.common.by import By

def main():
    driver = webdriver.Chrome()
    driver.get('https://festivaldecuritiba.com.br/atracao/buscar/todas/')
    items = get_page_items(driver)
    print(items)

def get_page_items(driver: webdriver.Remote) -> list:
    content = driver.find_element(By.ID, 'myTabContent')
    items = content.find_elements(By.TAG_NAME, 'li')
    return items

if __name__ == '__main__':
    main()
