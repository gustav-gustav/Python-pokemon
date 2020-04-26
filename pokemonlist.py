from collections import deque


class PokemonList:
    def __init__(self, *pokemons):
        self.maxlen = 6
        self.deque = deque(maxlen=self.maxlen)
        for pokemon in pokemons:
            self.add(pokemon)

    def __str__(self):
        return f'<class {self.__class__.__name__}>'

    def __repr__(self):
        return f'<class {self.__class__.__name__}>'

    def __iter__(self):
        return iter(self.deque)

    def __next__(self):
        return next(self.deque)

    def __len__(self):
        return len(self.deque)

    def __getitem__(self, name: str):
        if name in self.names:
            return self.deque[self.names.index(name)]
        else:
            return None

    def add(self, pokemon: object, index: int=-1):
        if len(self.deque) < self.maxlen:
            if index in range(-1, 6):
                self.deque.insert(index, pokemon)
            else:
                print(f'Position out of range: {index}')
        else:
            print(f'{self} is full.')

    def pop(self, name: str):
        pokemon = self[name]
        self.deque.remove(pokemon)
        return pokemon

    def move(self, name: str, position: int):
        self.add(self.pop(name), index=position)

    @property
    def names(self):
        return [pokemon.name for pokemon in self.deque]
