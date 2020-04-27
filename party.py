from collections import deque
from pokemon import Pokemon


class Party:
    '''Trainer's pokemon Party'''
    def __init__(self, *pokemons: Pokemon) -> None:
        '''Adds Pokemons to self.deque'''
        self.maxlen = 6
        self.deque = deque(maxlen=self.maxlen)
        for pokemon in pokemons:
            self.add(pokemon)

    def __str__(self) -> str:
        return f'<class {self.__class__.__name__} {[str(pokemon) for pokemon in self]}>'

    def __repr__(self) -> str:
        return f'<class {self.__class__.__name__}({", ".join([repr(pokemon) for pokemon in self])})>'

    def __iter__(self) -> iter:
        return iter(self.deque)

    def __len__(self) -> int:
        return len(self.deque)

    def __setitem__(self, index: int, pokemon: Pokemon) -> None:
        if type(index) is int:
            if index in range(0, self.maxlen):
                self.deque[index] = pokemon
            elif index == -1:
                self.deque.append(pokemon)
            else:
                raise IndexError(f'index {index!r} out of {range(-1, len(self))}')
        else:
            raise TypeError(f'index must be of type {str!r}')

    def __getitem__(self, identifier) -> object:
        '''Returns item from self.deque if item.name is in self.names'''
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

    def add(self, pokemon: Pokemon, index: int=-1) -> None:
        '''Adds a Pokemon to self.deque if there is space available'''
        if len(self) < self.maxlen:
            self[index] = pokemon
        else:
            print(f'{repr(self)} is full.')

    def pop(self, identifier) -> object:
        '''Removes Pokemon from self.deque and returns it'''
        pokemon = self[identifier]
        self.deque.remove(pokemon)
        return pokemon

    def remove(self, identifier) -> None:
        '''Removes Pokemon from self.deque'''
        pokemon = self[identifier]
        self.deque.remove(pokemon)

    def move(self, identifier1, identifier2) -> None:
        '''Moves a pokemon to a given position in self.deque'''
        poke1 = self[identifier1]
        poke2 = self[identifier2]
        index1 = self.index(identifier1)
        index2 = self.index(identifier2)
        self[index1] = None
        self[index2] = None
        self.add(poke2, index1)
        self.add(poke1, index2)
        print('done')

    def index(self, name:str) -> int:
        '''Returns Pokemon's index given its name'''
        return self.deque.index(self[name])

    @property
    def names(self) -> list:
        '''Returns a list of pokemon names from self.deque'''
        return [pokemon.name for pokemon in self.deque]


if __name__ == '__main__':
    '''debugging'''
    from pokemon import Pokemon
    from math import floor
    from random import randint
    level = 20
    pokemons = Party(*(Pokemon(pokemon, level=randint(floor(level*0.9), floor(level*1.1)))
                             for pokemon in ['bulbasaur', 'charmander', 'squirtle', 'pikachu']))