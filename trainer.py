from random import choice, randint
from math import floor
from party import Party
from pokemon import Pokemon
from bag import Bag
from client import client


class Trainer:
    '''Pokemon Trainer'''
    def __init__(self, name: str, *pokemons: tuple, level: int=5):
        self.name = name.capitalize()
        self.bag = Bag()
        self.party = Party(*(Pokemon(pokemon, level=randint(floor(level*0.9), floor(level*1.1))) for pokemon in pokemons) if pokemons else Pokemon(choice(['bulbasaur', 'charmander', 'squirtle', 'pikachu']), level=5))
        self.in_battle = False

    def __str__(self):
        return f'<{self.__class__.__name__} {self.name}>'

    def __repr__(self):
        return f'<class {self.__class__.__name__}({self.name!r}, {", ".join([repr(name) for name in self.party.names])})>'

    def battle(self, other):
        def catch(self, pokemon):
            pass

        def throw_pokeball(self, pokeball):
            pass

    def teach(self, machine: object, pokemon_name: str) -> None:
        pokemon = self.party[pokemon_name]
        pokemon.learn(self.bag.use(machine))

    def give(self, item: object, pokemon_name: str) -> None:
        pokemon = self.party[pokemon_name]
        pokemon.held_item = self.bag.use(item)

    def use_item(self, item: object,  pokemon_name: str) -> None:
        pokemon = self.party[pokemon_name]
        pokemon.use(self.bag.use(item))

    def pickup(self, item: object) -> None:
        self.bag.add(item)


if __name__ == '__main__':
    from client import client
    ash = Trainer('Ash', 'charmander', 'squirtle', 'bulbasaur', 'pikachu', level=50)