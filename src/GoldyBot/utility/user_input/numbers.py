from __future__ import annotations

class Numbers():
    """Class that holds all user input methods for dealing with numbers."""
    def __init__(self):
        pass

    @staticmethod
    def get_number(number:str) -> float|int:
        try:
            return int(number)
        except ValueError: # It is a bloody float!!!!
            return float(number)
