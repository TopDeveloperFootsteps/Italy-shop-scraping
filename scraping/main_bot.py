import random
import time

from selenium.common import WebDriverException, NoSuchElementException

from selenium import webdriver


import os
import json
from logging import getLogger, INFO, WARNING, ERROR

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datamining.settings')
django.setup()
from myapp.models.product import ProductItem
from myapp.models.country import CountryItem
from myapp.models.currency import CurrencyItem
from myapp.models.unit import UnitItem
from myapp.models.enums.unit import UnitType

logger = getLogger('db')


class MainBot:
    def __init__(self, file_paths, scraping_trigger, use_rotating_proxy=False):
        self.debug = False
        self.PRODUCTION = False

        self.proxy = None
        self.SCROLL_INTERVAL = 2.5
        self.NORMAL_SLEEP = 3
        self.DRIVER_WAIT = 20
        self.CATEGORY = ""
        self.SUBCATEGORY1 = ""
        self.SUBCATEGORY2 = ""
        self.SUBCATEGORY3 = ""
        self.NO_VALUE = ""
        self.total_items = 0
        self.total_prices = 0
        self.sum_unit_prices = 0
        self.total_scraped_items = 0
        self.paths = self.get_paths(file_paths)
        self.scraping_trigger = scraping_trigger
        self.logger = logger
        self.use_rotating_proxy = use_rotating_proxy
        self.destroy = False
        self.proxy_used = ''
        self.driver = self.set_proxy_from_dispatcher_with_auth()
        self.success = False
        self.screenshot_saved = False
        self.session = None

    def can_start_scraper(self, session, url_object):
        self.session = session

        return False if session else True

    def save_country(self, country):
        country_item, created = CountryItem.objects.get_or_create(
            name= country
        )
        if created:
            print(f"Created new Store: {country_item}")
        else:
            print(f'Store already exists: {country_item}')
        
        return country_item

    def save_products(self, products, country):

        for product_info in products:
            # Save or get the product using get_or_create
            product_item, created = ProductItem.objects.get_or_create(
                product_id = product_info['product_id'],
                country = country,
                defaults={  # Fields to create or update
                    'product_id': product_info['product_id'],
                    'brand': product_info['brand'],
                    'description': product_info['description'],
                    'miscellaneous': product_info.get('miscellaneous', None),
                    'scraping_date': product_info['scraping_date'],
                    'price': product_info.get('price', None),
                    'offer_type': product_info.get('offer_type', None),
                    'offer_end_date': product_info.get('offer_end_date', None),
                    'discount_percentage': product_info.get('discount_percentage', None),
                    'original_price': product_info.get('original_price', None),
                    'url': product_info['url'],
                    'img_url': product_info['img_url'],
                    'unit': UnitType.from_symbol(product_info['unit'])
                }
            )
            if created:
                print(f"Created new product: {product_item.product_id}")
            else:
                print(f"Product already exists: {product_item.product_id}")

            unit_item, created = UnitItem.objects.get_or_create(
                unit = product_info['unit']
            )
            
            currency_item = CurrencyItem.objects.create(
                price = product_info.get('price'),
                product_id = product_item
            )

    def close(self, products, address):
        print(products)
        try:
            country = self.save_country(address)
            self.save_products(products, country)
            self.driver.quit()
        except WebDriverException as e:
            self.logger.error(f'An error occurred while quitting the driver: {e}')

    def extract_el(self, e):
        return self.paths[e]['t'], self.paths[e]['v']

    def wait_for_el(self, el, time_to_wait=15, multiple=False, item=None, can_fail=False):
        self.sleep(1)
        wait = WebDriverWait(self.driver, time_to_wait)
        if item:
            wait = WebDriverWait(item, time_to_wait)
        if multiple:
            return wait.until(ec.visibility_of_all_elements_located((self.extract_el(el))))
        return wait.until(ec.visibility_of_element_located((self.extract_el(el))))

    def find_el(self, el, item=None, multiple=False):
        method, value = self.extract_el(el)
        driver = item if item else self.driver
        if multiple:
            return driver.find_elements(method, value)
        return driver.find_element(method, value)

    def get_text_from_item(self, el, item=None, attribute=None):
        try:
            if element := self.find_el(el, item, multiple=True):
                if attribute:
                    return element[0].get_attribute(attribute)
                else:
                    return element[0].text
        except NoSuchElementException:
            return ''

    @staticmethod
    def sleep(seconds, variation_percentage=30):
        variation = seconds * (variation_percentage / 100)
        sleep_time = random.uniform(seconds - variation, seconds + variation)
        time.sleep(sleep_time)

    @staticmethod
    def get_paths(file_paths):
        # get the path of the paths.json file relative to the current file
        current_directory = os.path.dirname(os.path.abspath(file_paths))
        json_file_path = os.path.join(current_directory, 'paths.json')
        with open(json_file_path) as f:
            return json.load(f)


    def log(self, text, log_level=INFO):
        print(text)
        # log = self.logger.info
        # if log_level == WARNING:
        #     log = self.logger.warning
        # elif log_level == ERROR:
        #     log = self.logger.error
        #
        # log(text)

    def scroll_page(self):
        self.log(f'Scroll page')

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.sleep(self.NORMAL_SLEEP)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        self.sleep(self.NORMAL_SLEEP)

    def scroll_to_element(self, element):
        self.log(f'scroll to element')
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.sleep(1)

    def set_proxy_from_dispatcher_with_auth(self, increment_session=True):

        chrome_options = Options()

        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.geolocation": 1,
            "profile.default_content_settings.geolocation": 1
        })
        
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        
        chrome_driver_path = "E:/Angular/chart/backend/chromedriver.exe"
        service = Service(chrome_driver_path)  # Create a Service object
        # Let Selenium Manager handle driver installation
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
