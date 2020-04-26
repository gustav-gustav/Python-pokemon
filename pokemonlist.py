from collections import deque


class PokemonList:
    def __init__(self, *pokemons: tuple) -> None:
        self.maxlen = 6
        self.deque = deque(maxlen=self.maxlen)
        for pokemon in pokemons:
            self.add(pokemon)

    def __str__(self) -> str:
        return f'<class {self.__class__.__name__} {[pokemon for pokemon in self]}>'

    def __repr__(self) -> str:
        return f'<class {self.__class__.__name__}>'

    def __iter__(self) -> iter:
        return iter(self.deque)

    def __next__(self) -> next:
        return next(self.deque)

    def __len__(self) -> int:
        return len(self.deque)

    def __getitem__(self, name: str) -> list:
        '''Returns item from self.deque if item.name is in self.names'''
        if name in self.names:
            return self.deque[self.names.index(name)]
        else:
            return None

    def add(self, pokemon: object, index: int=-1) -> None:
        '''Adds a Pokemon to self.deque if there is space available'''
        if len(self.deque) < self.maxlen:
            if index in range(-1, 6):
                self.deque.insert(index, pokemon)
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
