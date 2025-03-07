import re
from selenium.webdriver.common.by import By


def clean_product_price(string):
    if string:
        match = re.search(r'\d{1,2}([.,])\d{2}', string)
        if match:
            price_str = match.group().replace(",", ".")
            return float(price_str)
        else:
            return None
        regex = re.compile(r'^€ (\d+,\d{2})')
        match = regex.search(string)
        price = match.group(1)
        return float(price.replace(",", ".").strip())
    return None


def clean_result_number(result_number):
    try:
        match = re.search(r'\d+', result_number)
        return int(match.group())
    except:
        return None

def get_unit(text):
    try:
        match = re.search(r"([^\d\s.,]+)$", text)  # Match non-numeric characters at the end of the string
        if match:
            currency_symbol = match.group(1)
            return currency_symbol
        else:
            return None
    except:
        return None

# def get_product_price(product):
#     try:
#         price_element = item.find_element(By.XPATH,'')