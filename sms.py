#!/usr/bin/env python3


from configparser import ConfigParser
from pyvirtualdisplay import Display  # xvfb wrapper
import re
from selenium import webdriver
import sys


CONF_FILE = './conf'
BROWSER_VISIBLE = False


def init_conf():
    conf = [ConfigParser()]
    conf[0].read(CONF_FILE)
    return conf


def get_conf(conf=init_conf()):
    return conf[0]


def print_help():
    print('Sends a sms via your Telenor credentials to another Telenor phone.')
    print('usage: sms phonenumber message')


def hide_browser():
    display = Display(visible=0, size=(800, 600))
    display.start()


def log_in(driver):
    driver.get('https://my.telenor.bg')
    driver.find_element_by_name('phone').send_keys(get_conf()['credentials']['num'])
    driver.find_element_by_id('button-next').click()
    driver.find_element_by_id('pin').send_keys(get_conf()['credentials']['password'])
    driver.find_element_by_id('button-next').click()


def send(driver, num, msg):
    assert(len(msg) <= 100)
    driver.get('https://my.telenor.bg/compose')
    driver.find_element_by_id('closeprivacy').click()
    driver.find_element_by_id('receiverPhoneNum').send_keys(num)
    driver.find_element_by_id('txtareaMessage').send_keys(msg)
    driver.find_element_by_css_selector('.purple-pink-gradient').click()
    print('Sent', msg, 'to +359', num)


# Without this the browser survives program termination.
def clean_up(driver):
    driver.close()


# Remove the leading 0 because +359 is automatically added.
def remove_zero(num):
    if not (re.match('0895\d\d\d\d\d\d', target)
        or re.match('0899\d\d\d\d\d\d', target)):
        raise BaseException('This is not a Telenor phone number.')

    return num[1:]


# target - phone number OR a name from conf/phonebook
def get_target_num(target):
    try:
        return remove_zero(target)
    except:
        pass

    try:
        pb = get_conf()['phonebook']
        if target in pb:
            return pb[target][1:]
    except:
        pass

    raise BaseException('Failed to identify recepient.')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print_help()
        sys.exit()

    if not BROWSER_VISIBLE:
        hide_browser()

    driver = webdriver.Firefox()
    log_in(driver)
    send(driver, get_target_num(sys.argv[1]), sys.argv[2])
    clean_up(driver)
