from pokemonlist import PokemonList
from pokemon import Pokemon
from bag import Bag
import random

class Trainer:
    def __init__(self, name):
        self.name = name.capitalize()
        self.bag = Bag()
        self.pokemons = PokemonList(Pokemon(random.choice(['bulbasaur', 'charmander', 'squirtle', 'pikachu']), level=5))

    def __str__(self):
        return f'<{self.__class__.__name__} {self.name} - {[repr(pokemon) for pokemon in self.pokemons]}>'

    def __repr__(self):
        return f'<class {self.__class__.__name__} {self.name}>'

    def battle(self, other):
        def catch(self, pokemon):
            pass

        def throw_pokeball(self, pokeball):
            pass

    def teach(self, machine, pokemon):
        pokemon.learn(machine)

    def give(self, item, pokemon):
        pokemon.held_item = self.bag.use(item)

    def use_item(self, item,  pokemon):
        pokemon.use(self.bag.use(item))

    def pickup(self, item):
        self.bag.add(item)


if __name__ == '__main__':
    ash = Trainer('Ash')
    print(ash)