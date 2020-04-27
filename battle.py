from trainer import Trainer

class Battle:
    def __init__(self, trainer1, trainer2):
        self.trainer1 = trainer1
        self.trainer2 = trainer2
        self.trainer1.in_battle = True
        self.trainer2.in_battle = True
        self.winner = None
        self.main()

    def main(self):
        self.trainer1.active_pokemon = self.trainer1.party[0]
        self.trainer2.active_pokemon = self.trainer1.party[0]
        # while not self.winner:
        #     print(f"{self.trainer1} turn")
        #     eval(input('What will you do?\n'))
        #     print(f"{self.trainer2} turn")
        #     eval(input('What will you do?\n'))

    def turn(self):
        print(f"{self.trainer1} turn")
        eval(input('What will you do?\n'))

if __name__ == '__main__':
    Battle(Trainer('ash', 'charmander', level=5),
           Trainer('gary', 'bulbasaur', level=5))
