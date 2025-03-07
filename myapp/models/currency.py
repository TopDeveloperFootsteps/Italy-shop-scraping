from django.db import models
from myapp.models.product import ProductItem

class CurrencyItem(models.Model):
    scraping_date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    product_id = models.ForeignKey(ProductItem, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_id