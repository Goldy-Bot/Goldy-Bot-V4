class Currency():
    """
    Base class for a currency in Goldy Bot. Use this to create you own custom currency.
        
    ---------------
    ### ***``Example:``***

    Hello, want to make your own custom currency? Well anyways you came to the right place.
    Below I show you an example on how to create your very own currency in Goldy Bot using the currency base class.

    ```python
    class GBP(GoldyBot.Currency):
        def __init__(self):
            super().__init__("GBP", "British Pounds", "💷", 600)
    ```
    - This is how a custom currency is implemented. The code name is ``GBP``, the display name is ``British Pounds``, the currency icon/emoji is a ``pound banknote`` (💷) emoji and the default balance for this currency is 600.

    ```python
    class UwUCoin(GoldyBot.Currency):
        def __init__(self):
            super().__init__("uwu_coin", "UwU Coin", "🟡", 0)
    ```
    - Here's another example for fun. 😁
    """

    def __init__(self, code_name:str, display_name:str, display_emoji:str="💷", default_bal:int=600):
        self.code_name_ = code_name
        self.display_name_ = display_name
        self.display_emoji_ = display_emoji
        self.default_bal_ = default_bal

    @property
    def code_name(self):
        """Returns code name of currency."""
        return self.code_name_

    @property
    def display_name(self):
        """Returns display name of currency."""
        return self.display_name_

    @property
    def display_emoji(self):
        """Returns some sort of emoji or icon that is used to identify this currency."""
        return self.display_emoji_

    @property
    def default_bal(self):
        """Returns the default balance for this currency."""
        return self.default_bal_

class GoldyCredits(Currency):
    """The main Goldy Bot currency."""
    def __init__(self):
        super().__init__("goldCoins", "Goldy Credits")