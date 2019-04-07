from enum import Enum


class Bonus:
    class BonusType(Enum):
        MONEY_PER_FRAME = 1
        SUBS = 2
        SPECIAL_EVENT = 3

    def __init__(self, type):
        self.type = type

    def get_bonus(self):
        pass

    def get_presentation(self):
        pass

    def get_price(self):
        pass


class BotNetBonus(Bonus):
    def __init__(self):
        self.level = 0
        super().__init__(self.BonusType.SUBS)

    def get_bonus(self):
        return 10 * self.level

    def get_price(self):
        return 50 + 50 * (2 ** self.level)

    def get_presentation(self):
        return 'BotNet lvl{0}, price: {1}, subs: {2}'.format(self.level,
                                                             self.get_price(),
                                                             self.get_bonus())


class AdvertisingBonus(Bonus):
    def __init__(self):
        self.level = 0
        super().__init__(self.BonusType.MONEY_PER_FRAME)

    def get_bonus(self):
        return 0 if not self.level else 1 * (10 ** (self.level - 20))

    def get_price(self):
        return 50 + 150 * (2 ** self.level)

    def get_presentation(self):
        return 'Advert lvl{0}, price: {1}, money per sub: {2}'.format(
            self.level, self.get_price(), self.get_bonus())
