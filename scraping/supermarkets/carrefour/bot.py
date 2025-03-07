import datetime
import traceback
from logging import INFO, ERROR, WARNING, DEBUG

from .utils import clean_product_price, clean_result_number, get_unit
from ...main_bot import MainBot


class ScraperBot(MainBot):
    def __init__(self, ecommerce_url, category_url, login_info, session=None):
        super().__init__(__file__, None, False)
        self.zip_code = login_info['zip_code']
        self.category_link = category_url
        self.ecommerce_link = ecommerce_url
        self.product_data = []

        if self.can_start_scraper(session, None):
            self.start()
            self.close(self.product_data, self.zip_code)

    def start(self):
        self.driver.get(self.category_link)

        self.accept_privacy()
        self.set_zip_code()

        self.driver.get(self.category_link)
        self.scroll_page()
        self.scrape_products()

    def accept_privacy(self):
        # STEP1: Accept privacy
        self.log(f'Accept privacy')
        try:
            button = self.wait_for_el('accept_privacy')
            button.click()
        except:
            self.log('Accept Privacy button not found', WARNING)

    def set_zip_code(self):
        # STEP2: Set CAP
        self.log(f'Set zip code')
        button = self.wait_for_el('button_zip_code')
        button.click()

        field_zip_code = self.wait_for_el('field_zip_code')
        field_zip_code.send_keys(self.zip_code)

        # STEP3: Confirm CAP
        button = self.wait_for_el('confirm_zip_code')
        button.click()

        card_pickup = self.wait_for_el('delivery_service_pickup')
        self.scroll_to_element(card_pickup)
        button = self.wait_for_el('delivery_service', item=card_pickup)
        self.scroll_to_element(button)
        button.click()

        try:
            stores_list = self.wait_for_el('stores_list')
            store_button = self.wait_for_el('choose_first_store', item=stores_list)
            store_button.click()

            button = self.wait_for_el('chose_delivery_later', item=store_button)
            self.scroll_to_element(button)
            button.click()
            self.sleep(self.NORMAL_SLEEP)

        except Exception as e:
            tb = traceback.format_exc()
            self.log(f"Exception occurred: {e}\nTraceback: {tb}", WARNING)
            pass


    def scrape_products(self):
        self.log("SCRAPE PRODUCTS | {0} ".format(self.category_link), DEBUG)
        try:
            items = self.find_el("product_item", multiple=True)

            result_number = self.find_el("result_number").text
            elements_number = 0
            if result_number:
                elements_number = clean_result_number(result_number)

            self.log(f"there are {elements_number} products and {len(items)} items")
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
                if i % 4 == 0:
                    self.scroll_to_element(item)

                brand = self.get_text_from_item("brand", item=item)
                description = self.get_text_from_item("tile_description", item=item)
                product_url = self.get_text_from_item("product_link", item=item, attribute='href')
                img_url = self.get_text_from_item("img_url", item=item, attribute='src')
                product_id = self.get_text_from_item("product_tile", item=item, attribute='data-pid')

                # tries to understand if it's a discounted product since the price has a different source in such a case
                sales_discounted = self.find_el("sales_discounted", item=item, multiple=True)  # only discounted products have this CSS selector
                if len(sales_discounted) > 0:
                    product_price = self.get_text_from_item("value_discounted", item=item)
                    original_price = self.get_text_from_item("original_price", item=item)
                else:
                    product_price = self.get_text_from_item("value", item=item)
                    original_price = None

                price = clean_product_price(product_price)
                unit = get_unit(product_price)

                product_info = {
                    'brand': brand,
                    'description': description,
                    'miscellaneous': None,
                    'scraping_date': datetime.date.today(),
                    'product_id': product_id,
                    'price': price,
                    'offer_type': None,
                    'offer_end_date': None,
                    'discount_percentage': None,
                    'original_price': clean_product_price(original_price),
                    'url': product_url,
                    'img_url': img_url,
                    'unit': unit
                }

                self.product_data.append(product_info)

                self.log(f'PRODUCT DATA: {self.product_data[-1]}')

                self.log(f"PRICE: {price}")
                self.total_prices += price

            except Exception as e:
                tb = traceback.format_exc()
                self.log(f"Exception occurred: {e}\nTraceback: {tb}", ERROR)

