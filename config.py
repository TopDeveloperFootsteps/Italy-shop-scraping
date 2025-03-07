# config.py

# Define the percentage range for price changes (in %)
PRICE_CHANGE_RANGE = {
    'min_change': -5,  # Minimum percentage change
    'max_change': 5,   # Maximum percentage change
}

# Define stable days before a price change occurs
STABLE_DAYS = 3  # Number of days a price stays stable

# Define probability of a price spike or drop
SPIKE_PROBABILITY = 0.1  # Probability of a sudden price spike/drop (0.1 = 10%)

# Define different periods for price change frequency
PERIODS = {
    'daily': 1,    # 1 change per day
    'weekly': 7,   # 1 change per week
    'monthly': 30  # 1 change per month
}