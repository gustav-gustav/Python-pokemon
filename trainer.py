from pokemonlist import PokemonList
from pokemon import Pokemon
from bag import Bag
import random

class Trainer:
    '''
    Trainer
    --------
    '''
    def __init__(self, name: str, *pokemons: tuple):
        self.name = name.capitalize()
        self.bag = Bag()
        self.pokemons = PokemonList(*(Pokemon(pokemon, level=5) for pokemon in pokemons) if pokemons else Pokemon(random.choice(['bulbasaur', 'charmander', 'squirtle', 'pikachu']), level=5))
        self.in_battle = False

    def __str__(self):
        return f'<{self.__class__.__name__} {self.name} - {[pokemon for pokemon in self.pokemons]}>'

    def __repr__(self):
        return f'<class {self.__class__.__name__}({self.name!r}, {", ".join([repr(name) for name in self.pokemons.names])})>'

    def battle(self, other):
        def catch(self, pokemon):
            pass

        def throw_pokeball(self, pokeball):
            pass

    def teach(self, machine: object, pokemon_name: str):
        pokemon = self.pokemons[pokemon_name]
        pokemon.learn(self.bag.use(machine))

    def give(self, item: object, pokemon_name: str):
        pokemon = self.pokemons[pokemon_name]
        pokemon.held_item = self.bag.use(item)

    def use_item(self, item: object,  pokemon_name: str):
        pokemon = self.pokemons[pokemon_name]
        pokemon.use(self.bag.use(item))

    def pickup(self, item):
        self.bag.add(item)


if __name__ == '__main__':
    # from client import client
    # ash = Trainer('Ash', 'charmander', 'squirtle', 'bulbasaur', 'pikachu')
    pass