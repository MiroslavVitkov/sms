#!/usr/bin/env python3


from pyvirtualdisplay import Display  # xvfb wrapper
from selenium import webdriver


if __name__ == '__main__':
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Firefox()
    driver.get('http://abv.bg')
