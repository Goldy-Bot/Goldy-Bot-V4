import GoldyBot
from ...objects.currency import Currency

class Money():
    """Subclass for managing money in member database class."""
    def __init__(self, member) -> None:
        self.actual_member:GoldyBot.Member = member

    async def get_money(self, currency_class:Currency) -> int:
        """Returns the amount of money this member has of that currency."""
        currency = currency_class

        try: 
            member_data = await self.actual_member.get_member_data()
            return member_data[self.actual_member.member_id][currency.code_name]
        except KeyError:
            return currency.default_bal

    async def give_money(self, currency_class:Currency, amount:int) -> bool:
        """Gives the member the specified amount of money on that specified currency."""
        currency = currency_class

        # Add to previous bal in database.
        result = await self.actual_member.database.edit("global", {"_id":int(self.actual_member.member_id)}, {
            self.actual_member.member_id: {
                currency.code_name:  (await self.get_money(currency) + amount)
            }
        })

        return result

    async def take_money(self, currency_class:Currency, amount:int) -> bool:
        """Takes from the member a specified amount of money on that specified currency."""
        currency = currency_class

        # Take from previous bal in database.
        result = await self.actual_member.database.edit("global", {"_id":int(self.actual_member.member_id)}, {
            self.actual_member.member_id: {
                currency.code_name:  (await self.get_money(currency) - amount)
            }
        })

        return result