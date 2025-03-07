from enum import Enum

class UnitType(Enum):
    EUR = "€"
    GBP = "£"
    USD = "$"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
    
    @classmethod
    def from_symbol(cls, symbol):
        """Helper method to map a currency symbol to its enum name."""
        for unit in cls:
            if unit.value == symbol:
                return unit.name
        return None  # In case the symbol is not recognized