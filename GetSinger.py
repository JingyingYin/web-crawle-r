#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


def get_singer(click_times = 6):
    '''
    get all the singers name from the web
    :return list of singers:
    '''

    driver = None
    # the button 'SEE MORE' has to be clicked continuously to show all the singer tables
    # Thus, I have to use selenium to mimic human clicking that button
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)  # use the path where chromedriver is
        driver.get('https://www.biography.com/people/groups/singer')
        driver.maximize_window()  # maximize the window
        time.sleep(5)  # wait, make sure that the maximizing is done
        for i in range(click_times):
            xpath = "//*[@id='lyra-wrapper']/div/div[3]/section/div[2]/section[2]" \
                    "/section/div/button"
            WebDriverWait(driver,
                          20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            driver.execute_script(
                "document.getElementsByClassName('m-component-footer--loader m-button')[0].click()"
            )
            time.sleep(2)  # wait, make sure that all the content has been shown

        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "lxml")  # get into the original code of website
        contents = soup.select('div[class=="l-grid--item"]')  # reach into the main table where singers are
        singers = []
        for content in contents:
            singer = content.select('a')[0].get('title', None)  # get sinegrs' names
            singers.append(singer)

    finally:
        if driver:
            driver.close()
            return singers
        else:
            return None


def test():
    temp = None
    temp = get_singer(1)
    assert temp is not None

    print("Test pass!")


if __name__ == '__main__':
    test()
