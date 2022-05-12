#!/usr/bin/python

import csv
from threading import Thread
from typing import List, cast
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .types import Product


class CrawlerParceiroMagalu(object):
    __base_url: str = "https://www.magazinevoce.com.br"
    __store: str
    __query: str
    __price_bigger_then: int
    __price_less_then: int
    __file_name: str
    __browser: bool
    __zip_code: str

    __products: List[Product] = []
    __threads: List[Thread] = []

    def __init__(self, **kwargs):
        self.__store = kwargs.get("store", "")
        self.__query = kwargs.get('query', None)
        self.__price_bigger_then = kwargs.get(
            'price_bigger_then', kwargs.get('pbgt', None))
        self.__price_less_then = kwargs.get(
            'price_less_then',  kwargs.get('plst', None))
        self.__file_name = kwargs.get('file_name', "./products.csv")
        self.__browser = kwargs.get("browser", False)
        self.__zip_code = kwargs.get("zipcode", "")

    def __update_product(self, product: Product):
        for p in self.__products:
            if p.name == product.name:
                self.__products.remove(p)
                self.__products.append(product)

    def __open_product_detail(self, p: Product):

        if self.__zip_code == None or self.__zip_code == "":
            return

        options = webdriver.ChromeOptions()

        if not self.__browser:
            options.add_argument("--headless")  # run background

        driver = webdriver.Chrome(options=options)

        driver.get(p.page_url)

        welcome_modal = driver.find_element(By.ID, "mod-welcome")

        if welcome_modal != None:
            close_btn = welcome_modal.find_element(
                By.CLASS_NAME, "welcome-close")
            if close_btn != None:
                close_btn.click()

        driver.implicitly_wait(0.01)

        input_zipcode: WebElement = driver.find_element(
            By.ID, "zipcode")
        input_zipcode.send_keys(self.__zip_code, Keys.RETURN)

        try:
            element: WebElement = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "shipment-prices"))
            )

            items = element.find_elements(
                By.CLASS_NAME, 'shipment-item')

            if items != None:
                shipping = ', '.join(
                    list(map(lambda item: item.text, items)))

            p.shipping = shipping
            self.__update_product(p)
        except ValueError as err:
            print(err)
        finally:
            pass

        driver.close()

    def __currency_to_float(self, n: str):
        return float(n.replace('R$', '').strip().replace('.', '').replace(',', '.'))

    def __products_to_file(self):
        with open(self.__file_name, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            for product in self.__products:
                writer.writerow([product.name, product.price,
                                product.colors, product.img, product.page_url, product.shipping])

        f.close()

    def __filter_apply(self):
        # TODO: check is possible filter price product inside site
        if self.__price_bigger_then != None:
            self.__products = list(filter(lambda p: p.price >
                                   self.__price_bigger_then, self.__products))

        if self.__price_less_then != None:
            self.__products = list(filter(lambda p: p.price <
                                   self.__price_less_then, self.__products))

    def search(self):
        options = webdriver.ChromeOptions()

        if not self.__browser:
            options.add_argument("--headless")  # run background

        driver = webdriver.Chrome(options=options)

        driver.get(f"{self.__base_url}/{self.__store}")

        print(driver.title)
        print(driver.current_url)

        welcome_modal = driver.find_element(By.ID, "mod-welcome")

        if welcome_modal != None:
            close_btn = welcome_modal.find_element(
                By.CLASS_NAME, "welcome-close")
            if close_btn != None:
                close_btn.click()

        search_bar = driver.find_element(By.NAME, "q")

        search_bar.clear()

        search_bar.send_keys(self.__query, Keys.RETURN)

        products_li = cast(List[WebElement], driver.find_element(
            By.CLASS_NAME, "g-items").find_elements(By.TAG_NAME, "li"))

        self.__products = []
        self.__threads = []

        if products_li != None:
            for product_li in products_li:
                price = self.__currency_to_float(product_li.find_element(
                    By.CSS_SELECTOR, "p > strong").text)

                colors = product_li.find_element(
                    By.CLASS_NAME, "g-variations").text

                img = product_li.find_element(
                    By.CSS_SELECTOR, 'img').get_attribute('data-original')

                page_url_link: WebElement = product_li.find_element(
                    By.CSS_SELECTOR, 'a')

                page_url = page_url_link.get_attribute('href')

                product = Product(
                    name=product_li.text,
                    price=price,
                    colors=colors,
                    img=img,
                    page_url=page_url
                )

                self.__products.append(product)

                if page_url != None:
                    t = Thread(target=self.__open_product_detail,
                               args=(product,))
                    self.__threads.append(t)
                    t.start()

        for t in self.__threads:
            t.join()

        driver.close()

        self.__filter_apply()
        self.__products_to_file()
        print("finished work!")
