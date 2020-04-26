from collections import deque
from client import client
import random


class Moves:
    def __init__(self, pokemon, moveset: list=[], machine=False):
        self.pokemon = pokemon
        self.maxlen = 4
        self.q = deque(maxlen=self.maxlen)
        if moveset:
            for move in moveset:
                self.add(move, printer=False)
        else:
            learned = [move for move in self.pokemon.pokemon.moves if move.version_group_details[0].move_learn_method.name == "level-up"]
            lower_than_level = [move.move.name for move in learned if move.version_group_details[0].level_learned_at <= self.pokemon.level]
            for _ in range(self.maxlen):
                if lower_than_level:
                    random_move = lower_than_level.pop(random.randrange(len(lower_than_level)))
                    self.add(random_move, printer=False)

    def __repr__(self):
        return f'<class {self.__class__.__name__} {list(self.q)}>'

    def __len__(self):
        return len(self.q)

    def use(self, move):
        if move in [move.name for move in self.list]:
            index = self.index(move)
            if self.q[index].pp > 0:
                self.q[index].pp -= 1
                print(f'{self.pokemon.name} uses {move}')
                return self.get(move)
            else:
                print(f'no pp left for {attack.name}')
        else:
            print(f"{self.pokemon.name} doesn't know {move}")
            return None

    def add(self, move, index=-1, printer=True):
        # move list for all learnable moves
        pkm_mvlist = [m.move.name for m in self.pokemon.pokemon.moves]
        if move in pkm_mvlist:
            # checks if move is already in moveset
            if move not in [move.name for move in self.list]:
                # index for selected move in learnable list
                move_index = [i for i, mv in enumerate(pkm_mvlist) if mv == move][0]
                # checks if required level is  satisfied
                if self.pokemon.level >= self.pokemon.pokemon.moves[move_index].version_group_details[0].level_learned_at:
                    if len(self.q) < self.maxlen:
                        # if space is available, inserts it
                        self.q.insert(index, client.get_move(move))
                        if printer:
                            print(f"{self.pokemon.name} learned {move}!")
                    else:
                        # else prompts to delete a move
                        print(f"{self.pokemon.name} is trying to learn {move}")
                        print(f"would you like to remove a move to learn {move}?")
                        movestats = ''.join(
                            [f"[{index}]{mv.name} - power: {mv.power} - pp: {mv.pp}\n" for index, mv in enumerate(self.list)])
                        ans = input('y/n: ')
                        if ans == 'y':
                            index = int(input(movestats + 'choice: '))
                            self.remove(self.list[index].name)
                            self.add(move, index=index)
                        else:
                            print(f"{self.name} didn't learn {move}")
                else:
                    print(f"{self.pokemon.name}'s level is too low to learn {move}")
            else:
                print(f"{self.pokemon.name} already know's {move}")
        else:
            print(f"{self.pokemon.name} cant't learn {move}")

    def remove(self, move):
        if move in [m.name for m in self.q]:
            self.q.remove(self.get(move))
            print(f'{self.pokemon.name} forgot {move}...')
        else:
            print(f'no move {move} in moveset')

    def index(self, move):
        for m in self.list:
            if move == m.name:
                return self.q.index(m)

    def get(self, move):
        return self.q[self.index(move)]

    @property
    def list(self):
        return list(self.q)

    @property
    def names(self):
        return [m.name for m in self.q]
