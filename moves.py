from collections import deque
from client import client
import random


class Moves:
    '''Pokemon's moveset'''
    def __init__(self, pokemon, moveset: list=[]):
        '''
        Adds moves to self.deque
        ----
            if moveset is provided tries to add them
            elif moveset is provided and pokemon.evolves_from is not None, adds them as previous moves
            else chooses random moves available based on the Pokemon's level
        '''
        self.pokemon = pokemon
        self.maxlen = 4
        self.deque = deque(maxlen=self.maxlen)
        self.available_moves = [m.move.name for m in self.pokemon.pokemon.moves]
        if moveset:
            if self.pokemon.evolves_from:
                for move in moveset:
                    self.deque.append(move)
            else:
                for move in moveset:
                    self.add(move, printer=False)
        else:
            learned = [move for move in self.pokemon.pokemon.moves if move.version_group_details[0].move_learn_method.name == "level-up"]
            lower_than_level = [move.move.name for move in learned if move.version_group_details[0].level_learned_at <= self.pokemon.level]
            for _ in range(self.maxlen):
                if lower_than_level:
                    random_move = lower_than_level.pop(random.randrange(len(lower_than_level)))
                    self.add(random_move, printer=False)

    def __repr__(self) -> str:
        return f'<class {self.__class__.__name__} {list(self.deque)}>'

    def __len__(self) -> int:
        return len(self.deque)

    def __iter__(self) -> iter:
        return iter(self.deque)

    def __setitem__(self, index: int, move: object) -> None:
        '''Adds item to self.deque if index meets requirements'''
        if type(index) is int:
            if index in range(0, self.maxlen):
                self.deque.insert(index, move)
            elif index == -1:
                self.deque.append(move)
            else:
                raise IndexError(
                    f'index {index!r} out of {range(-1, len(self))}')
        else:
            raise TypeError(f'index must be of type {str!r}')

    def __getitem__(self, identifier) -> object:
        '''Returns move from self.deque if move is in self.deque'''
        if type(identifier) is int:
            if identifier in range(-len(self), len(self)) or identifier == 0:
                return self.deque[identifier]
            else:
                raise IndexError(f'identifier {identifier!r} out of range of len({len(self)})')
        elif type(identifier) is str:
            if identifier in self.names:
                return self.deque[self.names.index(identifier)]
            else:
                raise ValueError(f'identifier {identifier!r} not in {self!r}')
        else:
            raise TypeError(f'identifier must be of type {str!r} or {int!r}')


    def use(self, move: str) -> object:
        '''Returns a move based on its name and decrease its pp'''
        if move in [move.name for move in self]:
            index = self.index(move)
            if self[index].pp > 0:
                self[index].pp -= 1
                print(f'{self.pokemon.name} uses {move}')
                return self[move]
            else:
                print(f'no pp left for {attack.name}')
        else:
            print(f"{self.pokemon.name} doesn't know {move}")
            return None

    def add(self, move: str, index: int=-1, printer: bool=True) -> None:
        '''Adds move to self.deque given its name if move is in pokemon's available moves'''
        # move list for all learnable moves
        if move in self.available_moves:
            # checks if move is already in moveset
            if move not in self.names:
                # index for selected move in learnable list
                move_index = [i for i, mv in enumerate(self.available_moves) if mv == move][0]
                # checks if required level is  satisfied
                if self.pokemon.level >= self.pokemon.pokemon.moves[move_index].version_group_details[0].level_learned_at:
                    if len(self) < self.maxlen:
                        # if space is available, inserts it
                        self[index] = client.get_move(move)
                        if printer:
                            print(f"{self.pokemon.name} learned {move}!")
                    else:
                        # else prompts to delete a move
                        print(f"{self.pokemon.name} is trying to learn {move}")
                        print(f"would you like to remove a move to learn {move}?")
                        movestats = ''.join(
                            [f"[{index}]{mv.name} - power: {mv.power} - pp: {mv.pp}\n" for index, mv in enumerate(self)])
                        ans = input('y/n: ')
                        if ans == 'y':
                            index = int(input(movestats + 'choice: '))
                            self.remove(self[index].name)
                            self.add(move, index=index)
                        else:
                            print(f"{self.pokemon.name} didn't learn {move}")
                else:
                    print(f"{self.pokemon.name}'s level is too low to learn {move}")
            else:
                print(f"{self.pokemon.name} already know's {move}")
        else:
            print(f"{self.pokemon.name} cant't learn {move}")

    def remove(self, move: str) -> None:
        '''Removes a move from self.deque given its name'''
        if move in [m.name for m in self]:
            self.deque.remove(self[move])
            print(f'{self.pokemon.name} forgot {move}...')
        else:
            print(f'no move {move} in moveset')

    def index(self, move: str) -> int:
        '''Returns the index of a move given its name'''
        for m in self:
            if move == m.name:
                return self.deque.index(m)

    @property
    def names(self) -> list:
        '''Returns a list of move names from self.deque'''
        return [m.name for m in self.deque]