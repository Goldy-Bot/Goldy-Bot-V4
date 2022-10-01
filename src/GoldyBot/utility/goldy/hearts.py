import random

HEARTS = ["🖤", "🤍", "💙", "💚", "💜", "🤎", "🧡", "❤️", "💛"]

class Hearts:
    """🖤 A class of Goldy Bot's lovely hearts. 🤍"""
    BLACK = HEARTS[0]
    WHITE = HEARTS[1]
    BLUE = HEARTS[2]
    GREEN = HEARTS[3]
    PURPLE = HEARTS[4]
    BROWN = HEARTS[5]
    ORANGE = HEARTS[6]
    RED = HEARTS[7]
    YELLOW = HEARTS[8]

    def random() -> str:
        """Returns a random coloured heart. 💛💜💙"""
        return random.choice(HEARTS)