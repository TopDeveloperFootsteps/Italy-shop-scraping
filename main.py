import sys
from scraping.supermarkets.carrefour.bot import ScraperBot as CarrefourBot
from scraping.supermarkets.Iperal.bot import ScaperBot as IperalBot

def run_scraper(supermarket_name, location):
    scrapers = {
        "carrefour": lambda: CarrefourBot(
            ecommerce_url="https://www.carrefour.it/spesa-online/",
            category_url="https://www.carrefour.it/spesa-online/dolci-e-prima-colazione/creme-spalmabili/",
            login_info={
                # "zip_code": "25049",
                "zip_code": location
            },
        ),
        "iperal": lambda: IperalBot(
            ecommerce_url="https://www.iperalspesaonline.it/",
            category_url="https://www.iperalspesaonline.it/category/creme-spalmabili",
            login_info={
                'email':"tjdevko@gmail.com",
                'password': 'ilkjokojjj',
                "address": location
                # 'address': 'Via Giovanni Verga'
            }
        )
    }

    if supermarket_name in scrapers:
        scrapers[supermarket_name]()  # Run the scraper with the correct parameters
    else:
        print("Invalid supermarket name. Please choose 'Iperal' or 'carrefour'.")
        sys.exit(1)

# scrapers['Iperal']()

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 3:
        print("Usage: python main.py <supermarket_name> <location>")
        sys.exit(1)

    supermarket_name = sys.argv[1].lower()
    print(supermarket_name)
    location = sys.argv[2]
    print(location)

    run_scraper(supermarket_name, location)
