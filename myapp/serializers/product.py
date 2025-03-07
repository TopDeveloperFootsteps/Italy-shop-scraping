from rest_framework import serializers
from .country import CountrySerializer
from myapp.models import ProductItem
from django.utils import timezone  # Import timezone
import random
from datetime import timedelta  # Only import timedelta, no need for the entire datetime module
import config  # Import the config file

# Price Simulator Class
class PriceSimulator:
    def __init__(self):
        # Use the values from config.py
        self.min_change = config.PRICE_CHANGE_RANGE['min_change']
        self.max_change = config.PRICE_CHANGE_RANGE['max_change']
        self.stable_days = config.STABLE_DAYS
        self.spike_prob = config.SPIKE_PROBABILITY

    def simulate_price(self, initial_price, days=30, period='daily'):
        prices = []
        current_price = initial_price
        date = timezone.now() - timedelta(days=days)

        # Adjust simulation period based on configuration
        period_days = config.PERIODS.get(period, 1)  # Default to 'daily' if period is invalid

        for _ in range(days):
            if random.randint(1, self.stable_days) == 1:  # Price changes every 'stable_days' days
                # Simulate price change
                price_change = random.uniform(self.min_change, self.max_change)
                if random.random() < self.spike_prob:  # Apply spike
                    price_change *= random.uniform(2, 4)  # Sudden spike/drop

                # Calculate new price and ensure it doesn't go below 0.01
                new_price = round(current_price * (1 + price_change / 100), 2)
                current_price = max(new_price, 0.01)

            # Only add price change to history on specified period
            if _ % period_days == 0:
                prices.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "price": current_price
                })

            date += timedelta(days=1)

        return prices

# Product Serializer Class
class ProductSerializer(serializers.ModelSerializer):
    price_history = serializers.SerializerMethodField()
    country = CountrySerializer()  # Use the CountrySerializer here to include detailed information
    class Meta:
        model = ProductItem
        fields = ['id', 'description', 'brand', 'price', 'img_url', 'country', 'price_history']  # Add price_history here

    def get_price_history(self, obj):
        # Generate simulated price history for the product
        simulator = PriceSimulator()
        price_history = simulator.simulate_price(obj.price, days=365)  # Simulate price for 30 days
        return price_history
