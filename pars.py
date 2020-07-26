import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests

import time

chrome_options = Options()
chrome_options.add_argument('start-maximized')

from config import config


class Parser:
    links_lesson = []
    links_homework = []

    def __init__(self):

        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        self.driver.get(config['login_url'])
        element_email = self.driver.find_element_by_xpath("//input[@id='user_email']")
        element_pass = self.driver.find_element_by_xpath("//input[@id='user_password']")
        element_email.send_keys(config['login'])
        element_pass.send_keys(config['password'])
        element_pass.send_keys(Keys.ENTER)
        time.sleep(1)

    def parse_links(self):
        self.driver.get(f'https://geekbrains.ru/lessons/{config["id_course"]}')
        links_lesson = self.driver.find_elements_by_xpath('//a[@class="lesson-header lesson-header_ended"]')
        links_homework = self.driver.find_elements_by_xpath('//div[@class="lessons-list"]//ul//a')
        for link in links_lesson:
            self.links_lesson.append(link.get_attribute("href"))
        for link in links_homework:
            self.links_homework.append(link.get_attribute("href"))

        self.open_links()

    def open_links(self):
        i = 0
        for link in self.links_lesson:
            i += 1
            self.go_to_liks(link, i)

        j = 0
        for link in self.links_homework:
            j += 1
            self.go_to_liks(link, j)

    def go_to_liks(self, link, i):
        self.driver.get(link)
        self.parse_page(i)

    def parse_page(self, i):
        links = self.driver.find_elements_by_xpath("//a[@class='lesson-contents__download-row']")

        for link in links:
            path = os.path.abspath(os.curdir)
            href = link.get_attribute("href")
            file_name = href.split('/')[-1]

            if not os.path.exists(f'{path}\\lesson_{i}'):
                os.mkdir(f'{path}\\lesson_{i}')
            time.sleep(1)

            if not '=.exe' in file_name:
                if not os.path.exists(f'{path}\\lesson_{i}\\{file_name}'):
                    f = open(f'{path}\\lesson_{i}\\{file_name}', "wb")
                    ufr = requests.get(href)
                    f.write(ufr.content)
                    f.close()

                    print(link)
                    print(link.text)
                    print(link.get_attribute('href'))

        path = os.path.abspath(os.curdir)
        f = open(f'{path}\\lesson_{i}\\description.txt', "a")

        for link in links:
            href = link.get_attribute("href")
            file_name = href.split('/')[-1]
            f.write(href)
            f.write(file_name)
            f.write(link.text)
            f.write(';\n\r')

        f.close()