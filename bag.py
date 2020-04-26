from client import client
import re


class Bag:
    '''Trainer's Bag'''
    def __init__(self):
        '''Creates all pockets in the bag and adds them to self.pockets'''
        self.items = Pocket('Items')
        self.pokeballs = Pocket('Pokeballs')
        self.machines = Pocket('TM/HM')
        self.berries = Pocket('Berries')
        self.key = Pocket('Key Items')
        self.pockets = list(self.__dict__.keys())

    def __str__(self) -> str:
        return '\n'.join([f'[{len(getattr(self, pocket))}] {getattr(self, pocket).name}' for pocket in self.pockets])

    def __repr__(self) -> str:
        return f'<class {self.__class__.__name__}>'

    def add(self, item: object) -> None:
        '''Adds item to adequate pocket'''
        pocket = getattr(self, self.get_pocket(item))
        pocket.add(item)

    def use(self, item: object) -> object:
        '''Depending on functionality of item, returns different results'''
        pocket_name = self.get_pocket(item)
        pocket = getattr(self, pocket_name)
        if pocket_name == 'machines':
            item_from_pocket = pocket.use(item)
            if item_from_pocket:
                effect = item_from_pocket.effect_entries[0].effect
                move = re.search(r'(?<=Teaches )(.*)(?= to a compatible Pokémon\.)', effect)[0].lower().replace(' ', '-')
                return client.get_move(move)
        else:
            return pocket.use(item)

    def discard(self, item: object, amount: int) -> None:
        '''Discards an amount of a given item'''
        pocket = getattr(self, self.get_pocket(item))
        pocket.discard(item)

    def remove(self, item: object) -> None:
        '''Removes item from bag'''
        pocket = getattr(self, self.get_pocket(item))
        pocket.remove(item)

    def category(self, item: object) -> object:
        '''Returns item category object'''
        return client.get_item_category(item.category.name)

    def get_pocket(self, item: object) -> str:
        '''Returns pocket name for given item'''
        pocket_name = self.category(item).pocket.name
        if hasattr(self, pocket_name):
            return pocket_name
        else:
            return 'items'


class Pocket:
    '''Pocket from Trainer's Bag'''
    def __init__(self, name: str):
        '''Sets Pocket's name, max length and items'''
        self.name = name
        self.maxlen = 30
        self.items = []

    def __str__(self):
        return "\n".join([f'[{item.count}] {item.name}' for item in self.items])

    def __repr__(self):
        return f'<class {self.__class__.__name__}>'

    def __len__(self):
        return len(set(self.names))

    def add(self, item: object) -> None:
        '''Adds an item to self.items'''
        if len(self.items) < self.maxlen:
            if item.name in set(self.names):
                item_from_pocket = self.get(item)
                if item_from_pocket.count < 999:
                    item_from_pocket.count += 1
                else:
                    print(f"Couldn't add {item_from_pocket.name}. Max number of {item_from_pocket.name} reached.")
            else:
                item.count = 1
                self.items.append(item)
        else:
            print(f"Couldn't add {item.name}. Pocket {self.name} is full.")

    def remove(self, item: object) -> None:
        '''Removes an item from self.items if item.count reaches 0'''
        self.items.remove(self.get(item))
        print(f"Removed {item.name}")

    def discard(self, item: object, amount: int) -> None:
        '''Discards an amount of a given item'''
        item_from_pocket = self.get(item)
        if item_from_pocket.count >= amount:
            item_from_pocket.count -= amount
            if item_from_pocket.count == 0:
                self.remove(item_from_pocket)
            else:
                print(f'Removed {amount} {item_from_pocket.name}.')
        else:
            print(f'Not enough {item_from_pocket.name}. Total: {item_from_pocket.count}')

    def get(self, item: object) -> object:
        '''Gets an item from self.items based on its name'''
        if item.name in self.names:
            index = self.names.index(item.name)
            return self.items[index]
        else:
            print(f"Item {item.name} is not in pocket")
            return None

    def use(self, item: object) -> object:
        '''Decreases item.count and returns it'''
        item_from_pocket = self.get(item)
        if item_from_pocket:
            item_from_pocket.count -= 1
            if item_from_pocket.count == 0:
                self.remove(item_from_pocket)
            return item_from_pocket

    @property
    def names(self):
        '''Returns a list of names from self.items'''
        return [item.name for item in self.items]


if __name__ == '__main__':
    bag = Bag()
    bag.add(client.get_item('sun-stone'))
    bag.add(client.get_item('sun-stone'))
    print(bag)
    # pass