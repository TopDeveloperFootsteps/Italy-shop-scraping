from rest_framework import serializers
from myapp.models import CountryItem

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryItem
        fields = ['id', 'name']  # Choose the fields you want to include from the Country model