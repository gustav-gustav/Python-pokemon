from collections import deque


class PokemonList:
    def __init__(self, *pokemons: tuple) -> None:
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

    def __next__(self) -> next:
        return next(self.deque)

    def __len__(self) -> int:
        return len(self.deque)

    def __getitem__(self, identifier) -> list:
        '''Returns item from self.deque if item.name is in self.names'''
        if type(identifier) is int:
            if identifier in range(-len(self), len(self)-1) or identifier == 0:
                return self.deque[identifier]
            else:
                raise IndexError(f'identifier {identifier!r} out of range of len({len(self)})')
        else:
            if identifier in self.names:
                return self.deque[self.names.index(identifier)]
            else:
                raise ValueError(f'identifier {identifier!r} not in {self!r}')

    def add(self, pokemon: object, index: int=-1) -> None:
        '''Adds a Pokemon to self.deque if there is space available'''
        if len(self.deque) < self.maxlen:
            if index in range(0, len(self)):
                self.deque.insert(index, pokemon)
            elif index == -1:
                self.deque.append(pokemon)
            else:
                print(f'Position out of range: {index}')
        else:
            print(f'{self} is full.')

    def pop(self, name: str) -> object:
        '''Removes Pokemon from self.deque and returns it'''
        pokemon = self[name]
        self.deque.remove(pokemon)
        return pokemon

    def move(self, name: str, position: int) -> None:
        '''Moves a pokemon to a given position in self.deque'''
        self.add(self.pop(name), index=position)

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
    pokemons = PokemonList(*(Pokemon(pokemon, level=randint(floor(level*0.9), floor(level*1.1)))
                             for pokemon in ['bulbasaur', 'charmander', 'squirtle', 'pikachu']))
    print(repr(pokemons))
    pokemons.move(0, -1)
    print(repr(pokemons))
    pokemons.move(0, -1)
    print(repr(pokemons))