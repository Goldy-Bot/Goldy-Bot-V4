class Currency():
    """Base class for currency in Goldy Bot."""

    def __init__(self, code_name:str, display_name:str, display_emoji:str="💷"):
        self.code_name_ = code_name
        self.display_name_ = display_name
        self.display_emoji_ = display_emoji

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