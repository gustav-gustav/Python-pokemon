from parsedb import type_defense
from client import client
from moves import Moves
from math import floor
import functools
import random
import time
import os


class Pokemon:
    '''
    Pokemon baseclass
    ----------------------------------------------------------
    stats: [hp, atk, def, sp_atk, sp_def, speed]    ok      \n
    increase stats ased on level                    ok      \n
    levels and exp needed                           ok      \n
    attack_poke                                     ok      \n
    moveset                                         ok      \n
    heal                                            ok      \n
    exp given                                       ok      \n
    exp earned                                      ok      \n
    levelup                                         ok      \n
    nature                                          ok      \n
    gender                                          ok      \n
    evolution chain                                 ok      \n
    evolution requirements                          ok      \n
    evolution                                       ok      \n
    evolution trigger                               ok      \n
    affection                                       not ok  \n
    attacks that apply stats                        not ok  \n
    moveset based on machine                        not ok  \n
    item held                                       ok      \n
    moveset based on level                          ok      \n
    learn new move                                  ok      \n

    battle mechanic:
    ----------
    pokemon order of attack                         not ok  \n

    bulbapedia
    -----------
    https://bulbapedia.bulbagarden.net/wiki/Statistic
    https://bulbapedia.bulbagarden.net/wiki/Nature
    https://bulbapedia.bulbagarden.net/wiki/Effort_values
    https://bulbapedia.bulbagarden.net/wiki/Individual_values
    https://bulbapedia.bulbagarden.net/wiki/Evolution

    if evolves_from:
        moveset         ok
        IVs             ok
        exp             ok
        effort values   not ok

    '''
    def __init__(self, name: str, level: int=1, moveset: list=[], evolves_from: object=None):
        self.pokemon = client.get_pokemon(name)
        self.name = self.pokemon.name.capitalize()
        self.evolves_from = evolves_from
        self.species = client.get_pokemon_species(self.pokemon.id)
        self.level = level if not evolves_from else evolves_from.level
        self.held_item = None if not evolves_from else evolves_from.held_item
        self.used_item = None
        # experience needed per level
        self.growth = client.get_growth_rate(self.species.growth_rate.name).levels
        # sets levels by increasing order
        self.growth.reverse()
        # sets inner exp
        self._exp = self.growth[self.level - 1].experience if not self.evolves_from else self.evolves_from._exp
        self.state = 'Awake' if not evolves_from else evolves_from.state
        self.nature = client.get_nature(random.choice(range(1, 26))) if not evolves_from else evolves_from.nature
        self.evolution_chain = client.get_evolution_chain(self.species.evolution_chain.url.split('/')[-2]).chain if not evolves_from else evolves_from.evolution_chain
        # chain of evolution with requirements based on item, level or condition
        self.evolves_to = self.get_evolution(self.evolution_chain)
        # adds moves to the moveset
        self.moveset = Moves(self, moveset if not evolves_from else evolves_from.moveset.list)
        # gets type effectiveness against self
        self.type_defense = type_defense(name=self.pokemon.name, debug=False)
        for stat in self.pokemon.stats:
            # gets the name of each stat
            param = eval('stat.stat.name')
            # if is evolution, iv is the same as pre-evolution randomly chooses an IV
            iv = getattr(self.evolves_from, param)['iv'] if self.evolves_from else random.randint(0, 16)
            # checks nature modifiers
            nature_mod = (1.1 if param == self.nature.increased_stat.name else 1) if hasattr(self.nature.increased_stat, name) else 1
            nature_mod = (0.9 if param == self.nature.increased_stat.name else 1) if hasattr(self.nature.increased_stat, name) else 1
            # creates a dictionary with all parameters
            obj = eval("dict([('base', stat.base_stat), ('effort', stat.effort), ('iv', iv), ('nature', nature_mod), ('current', stat.base_stat), ('max', stat.base_stat)])")
            # sets dict for every attribute
            setattr(self, param, obj)
            # sets the current stat for very attribte based on level
            self.map_by_level(param)

        # if self.species.has_gender_differences:
        #misc attributes

        self.gender = ('Male' if self.attack['iv'] > self.species.gender_rate else 'Female') if not self.evolves_from else evolves_from.gender
        self.color = self.species.color.name
        self.base_happiness = self.species.base_happiness
        self.capture_rate = self.species.capture_rate
        self.shape = self.species.shape.name
        self.is_baby = self.species.is_baby
        self.height = self.pokemon.height
        self.weight = self.pokemon.weight
        self.attack_order = self.pokemon.order
        self.abilities = self.pokemon.abilities

    def __str__(self):
        return f"<{self.__class__.__name__} {self.name} - {self.moveset.names}>"

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}>'

    def map_by_level(self, name: str):
        '''Called when pokemon is created or when level-up'''
        stat = getattr(self, name)
        if name == 'hp':
            value = ((((2*stat['base']) + stat['iv'] + (stat['effort']//4)) * self.level) / 100) + self.level + 10
        else:
            value = (((((2*stat['base']) + stat['iv'] + (stat['effort']//4)) * self.level) / 100) + 5) * stat['nature']
        exec(f"stat['max'] = floor(value)")  # stat['base'] +
        exec(f"stat['current'] = stat['max']")

    def heal(self, amount: int):
        '''Heal pokemon by an amount'''
        if (diff := self.hp['max'] - self.hp['current']) > 0:
            if diff < amount:
                amount = diff
            self.hp['current'] += amount
            print(f"{self.name} healed by {amount}. total hp: {self.hp['current']}")
            assert(self.hp['current'] >= 0 and self.hp['current'] <= base_hp)
        else:
            print('already at max hp')

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, value):
        next_level = self.growth[self.level]
        print(f"{self.name} earned {value - self._exp} exp.")
        self._exp = round(value)
        if self._exp > next_level.experience:
            self.levelup()

    def stats(self):
        '''Print stats: name - power - pp'''
        print('\n'.join([f"{name}: {getattr(self, name)['current']}" for name in (stat.stat.name for stat in self.pokemon.stats)]))

    def levelup(self):
        '''Called when exp reaches the threshold for the next level'''
        print(f'{self.name} leveled up!')
        self.level += 1
        for attr in [stat.stat.name for stat in self.pokemon.stats]:
            self.map_by_level(attr)
        self.evolve(trigger='level-up')

    def use(self, item):
        if item.category.name == 'evolution':
            self.used_item = item.name
            self.evolve(trigger='item')

    def learn(self, move):
        '''Adds move to self.moveset'''
        self.moveset.add(move)

    def evolve(self, trigger):
        '''triggers evolutions if all requirements are statisfied'''
        if self.evolves_to:
            for evolution in self.evolves_to:
                conditions = []
                requirements = self.evolves_to[evolution]
                if requirements['trigger'] == trigger:
                    for condition in requirements:
                        print(condition)
                        if condition == 'min_level':
                            if self.level >= requirements['min_level']:
                                conditions.append(True)
                            else:
                                conditions.append(False)
                        elif condition == 'item':
                            if self.used_item == requirements['item']:
                                conditions.append(True)
                            else:
                                conditions.append(False)
                        elif condition == 'held_item':
                            if self.held_item == requirements['held_item']:
                                conditions.append(True)
                            else:
                                conditions.append(False)
                        elif condition == 'trigger':
                            pass
                        else:
                            print('unhandled: ', condition, requirements[condition])

                if all(conditions):
                    print(f"{self.name} is evolving")
                    for _ in range(3):
                        print('.  ', end='\r')
                        time.sleep(0.25)
                        print('.. ', end='\r')
                        time.sleep(0.25)
                        print('...', end='\r')
                        time.sleep(0.25)
                    self.__init__(name=evolution, evolves_from=self)
                    print(f"{self.name} evolved into {evolution.capitalize()}")
                    break

    def get_evolution(self, chain):
        if hasattr(chain, 'evolves_to'):
            if chain.species.name == self.pokemon.species.name:
                evolutions = {}
                for evolution in chain.evolves_to:
                    obj = {}
                    for attr_name in evolution.evolution_details[0].Meta.attributes:
                        attr = getattr(evolution.evolution_details[0], attr_name)
                        if attr:
                            obj[attr_name] = attr
                    for attr_name in self.evolution_chain.evolves_to[0].evolves_to[0].evolution_details[0]._subresource_map.keys():
                        attr = getattr(evolution.evolution_details[0], attr_name)
                        if attr:
                            obj[attr_name] = attr.name
                    evolutions[evolution.species.name] = obj
            else:
                for subchain in chain.evolves_to:
                    evolutions = self.get_evolution(subchain)
        else:
            evolutions = None
        return evolutions

    def attack_poke(self, attack, other):
        if (self.state != 'fainted' or self.state != 'asleep') and other.state != 'fainted':
            attack = self.moveset.use(attack)
            if attack:
                if attack.accuracy > random.randrange(start=0, stop=100, step=1):
                    TARGETS = 0.75 if attack.target == "all-other-pokemon" else 1
                    STAB = 1.5 if attack.type.name in [t.type.name for t in self.pokemon.types] else 1
                    TYPE = other.type_defense[attack.type.name]['multiplier']
                    CRIT = ((2*self.level)+5)/(self.level+5) if random.uniform(0, self.speed['current']) > self.speed['current']/(self.speed['current'] * 2) else 1
                    OTHER = 1
                    RANDOM = random.uniform(0.85, 1)
                    LEVEL = self.level
                    ATK = getattr(self, 'special-attack')['current'] if attack.damage_class.name == 'special' else self.attack['current']
                    DEF = getattr(other, 'special-defense')['current'] if attack.damage_class.name == 'special' else other.defense['current']
                    BASE = self.pokemon.base_experience
                    MOD = STAB * TYPE * CRIT * OTHER * RANDOM * TARGETS
                    damage = floor(((((((2*LEVEL) / 5) + 2) * attack.power * (ATK/DEF)) / 50) + 2) * MOD)

                    damage = other.hp['current'] if damage > other.hp['current'] else damage
                    print(f'{self.name} strikes {other.name} with {damage} {attack.damage_class.name} damage.\n')
                    if other.hp['current'] > damage:
                        other.hp['current'] -= damage
                    else:
                        other.hp['current'] = 0
                        other.fainted = True
                        self.earn_exp(other)
                else:
                    time.sleep(0.25)
                    print(f"{self.name}'s {attack.name} missed.")

    def earn_exp(self, other):
        # https://bulbapedia.bulbagarden.net/wiki/Experience#Gain_formula
        a = 1                       #other pokemon
        b = other.pokemon.base_experience   #other pokemon
        t = 1                       #self
        e = 1                       #self
        L = other.level             #other
        p = 1                       #None
        f = 1.2                     #self.affection
        v = 1                       #self
        s = 1                       #exp-share and pokemon in battle that havent fainted
        v = 1                       #self over level of evolution
        formula = (a*t*b*e*L*p*f*v) / 7*s
        self.exp += round(formula)


if __name__ == '__main__':
    # poke1 = Pokemon('poliwhirl', level=20)
    # poke1.held_item = 'kings-rock'
    # poke1.evolve(trigger='trade')
    # poke1.levelup()
    # poke1.use(client.get_item(84))
    pass
