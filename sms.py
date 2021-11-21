#!/usr/bin/env python3


from configparser import ConfigParser
from pyvirtualdisplay import Display  # xvfb wrapper
from selenium import webdriver
import sys


CONF_FILE = './conf'
BROWSER_VISIBLE = False


def print_help():
    print('This program sends a sms via your Telenor credentials.')
    print('usage: sms phonenumber message')


def hide_browser():
    display = Display(visible=0, size=(800, 600))
    display.start()


def log_in(driver):
    conf = ConfigParser()
    conf.read(CONF_FILE)
    conf = conf['credentials']

    driver.get('https://my.telenor.bg')
    driver.find_element_by_name('phone').send_keys(conf['num'])
    driver.find_element_by_id('button-next').click()
    driver.find_element_by_id('pin').send_keys(conf['password'])
    driver.find_element_by_id('button-next').click()


def send(driver, num, msg):
    driver.get('https://my.telenor.bg/compose')
    driver.find_element_by_id('receiverPhoneNum').send_keys(num)
    driver.find_element_by_id('txtareaMessage').send_keys(msg)
    driver.find_element_by_css_selector('.purple-pink-gradient').click()


# Without this the browser survives program termination.
def clean_up(driver):
    driver.close()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print_help()
        sys.exit()

    if not BROWSER_VISIBLE:
        hide_browser()

    driver = webdriver.Firefox()
    log_in(driver)
    send(driver, sys.argv[1], sys.argv[2])
    clean_up(driver)
