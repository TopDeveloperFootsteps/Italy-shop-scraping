from django.db import models
from myapp.models.country import CountryItem
from myapp.models.enums.unit import UnitType

class ProductItem(models.Model):
    brand = models.CharField(max_length=100)
    description = models.TextField()
    miscellaneous = models.CharField(max_length=100, null=True, blank=True)
    scraping_date = models.DateTimeField(auto_now_add=True)
    product_id = models.CharField(max_length=100)
    price = models.FloatField()
    offer_type = models.CharField(max_length=100, null=True, blank=True)
    offer_end_date = models.CharField(max_length=100, null=True, blank=True)
    discount_percentage = models.CharField(max_length=100, null=True, blank=True)
    original_price = models.FloatField(null=True, blank=True)
    url = models.TextField()
    img_url = models.TextField()
    unit = models.CharField(choices = UnitType.choices(), null=True, max_length=100)
    country = models.ForeignKey(CountryItem, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product_id', 'country')

    def __str__(self):
        return self.product_id