class PiggyBank:
    def __init__(self, deposit_dollars, deposit_cents):
        self.dollars = deposit_dollars
        self.dollars += deposit_cents // 100
        self.cents = deposit_cents % 100

    def add_money(self, deposit_dollars, deposit_cents):
        self.dollars += deposit_dollars
        self.cents += deposit_cents
        self.dollars += self.cents // 100
        self.cents %= 100

    def __str__(self):
        return f"${self.dollars}.{self.cents}"
