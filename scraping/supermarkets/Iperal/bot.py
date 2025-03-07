import datetime
import traceback
from logging import INFO, ERROR, WARNING, DEBUG
from selenium.webdriver.common.by import By
from .utils import clean_product_price, clean_result_number, get_unit
# from .utils
from ...main_bot import MainBot

class ScaperBot(MainBot):
    def __init__(self, ecommerce_url, category_url, login_info, session=None):
        super().__init__(__file__, None, False)
        self.email_info = login_info['email']
        self.password_info = login_info['password']
        self.address = login_info['address']
        self.category_link = category_url
        self.ecommerce_link = ecommerce_url
        self.product_data = []

        if self.can_start_scraper(session, None):
            self.start()
            self.close(self.product_data,self.address)
    
    def start(self):
        self.driver.get(self.ecommerce_link)

        self.accept_privacy()
        self.login()
        self.select_address()
        self.select_time()
        self.driver.get(self.category_link)
        self.scroll_page()
        self.scrap_product()
        # self.driver.get(self.category_link)
        # self.scrape_products()
    
    def accept_privacy(self):
        # STEP1: Accept privacy
        self.log(f'Accept privacy')
        try:
            button = self.wait_for_el('accept_privacy')
            button.click()
        except:
            self.log('Accept Privacy button not found', WARNING)
    
    def login(self):
        self.log(f'Login start')
        try:
            button = self.wait_for_el('login_icon')
            button.click()

            field_email = self.wait_for_el('email_field')
            field_email.send_keys(self.email_info)

            field_password = self.wait_for_el('password_field')
            field_password.send_keys(self.password_info)

            login_confirm = self.wait_for_el('login_confirm')
            login_confirm.click()
            self.log("login successful")


        except Exception as e:
            self.log(f'Login failed: {e}')
    
    def select_address(self):
        self.log(f'register address')
        try:
            # field_modal_finish_btn = self.wait_for_el('close_first_modal')
            # field_modal_finish_btn.click()
            # self.log("Close first modal")

            self.log(f'click address select')
            select_address_button = self.wait_for_el('address_select')
            select_address_button.click()

            self.log(f'click correct tab')
            select_tab = self.wait_for_el('select_sub')
            select_tab.click()

            self.log(f"input address")
            input_address = self.wait_for_el('input_address')
            input_address.send_keys(self.address)

            list_address = self.wait_for_el('address_list')
            print(list_address)
            content_divs = list_address.find_elements(By.XPATH, "./div")
            if content_divs:
                content_divs[0].click()
                self.log('clicked correct address')
            else:
                self.log('incorrect address')

        except Exception as e:
            self.log(f'register address: {e}')

    def select_time(self):
        self.log(f'register time')
        try:
            field_time_select = self.wait_for_el('time_select')
            field_time_select.click()

            self.log(f'click day select')
            field_day_list = self.wait_for_el('day_list')
            content_day_divs = field_day_list.find_elements(By.XPATH,'./div')
            if content_day_divs:
                content_day_divs[0].click()
                self.log('clicked correct day')
            else:
                self.log('incorrect day')
           
            self.log(f"click time select")
            field_time_list = self.wait_for_el('time_list')
            inner_container_div = field_time_list.find_element(By.XPATH, ".//div[contains(@class, 'timeslot-button d-flex justify-center empty selected')]")
            if inner_container_div:
                inner_container_div.click()
                self.log('clicked correct time')
            else:
                self.log('incorrect time')
        
        except Exception as e:
            self.log(f'register address: {e}')

    def scrap_product(self):
        self.log(f'scraping product information')
        try:
            items = self.find_el("product_item", multiple=True)

            result_number = self.find_el("result_number").text
            elements_number = 0
            if result_number:
                elements_number = clean_result_number(result_number)

            self.log(f"there are {elements_number} products")
            if elements_number != len(items):
                self.log(f"Mismatching between total elements scraped and the total elements declared in the page", WARNING)
            
        except Exception as e:
            self.log(f'ITEMS NOT FOUND: ', WARNING)
            num_elements = self.find_el("result_number").text
            elements_number = clean_result_number(num_elements)
            if elements_number == 0:
                return None
        
        self.total_items += len(items)

        for i, item in enumerate(items):
            try:
                product_link = self.get_text_from_item("product_link",item=item,attribute='href')
                product_id = product_link.split("/")[-1]
                product_image = self.get_text_from_item("product_img", item=item, attribute="src")
                product_brand = self.get_text_from_item("brand",item=item)
                product_name = self.get_text_from_item("name",item=item)
                product_price = clean_product_price(self.get_text_from_item("price",item=item))
                product_description = self.get_text_from_item('description', item=item)
                product_old_price = clean_product_price(self.get_text_from_item('original_price',item=item))
                self.log(self.get_text_from_item("price",item=item))
                product_unit = get_unit(self.get_text_from_item("price",item=item))

                product_info = {
                    'brand': product_brand,
                    'description': product_description,
                    'miscellaneous': None,
                    'scraping_date': datetime.date.today(),
                    'product_id': product_id,
                    'price': product_price,
                    'offer_type': None,
                    'offer_end_date': None,
                    'discount_percentage': None,
                    'original_price': product_old_price,
                    'url': product_link,
                    'img_url': product_image,
                    'unit': product_unit
                }

                self.product_data.append(product_info)
                self.log(f'PRODUCT DATA: {self.product_data[-1]}')

                self.log(f"PRICE: {price}")
                self.total_prices += price

            except Exception as e:   
                self.log(f'error:{e}')




    
