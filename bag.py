from client import client


class Bag:
    def __init__(self):
        self.items = Pocket('Items')
        self.pokeballs = Pocket('Pokeballs')
        self.machines = Pocket('TM/HM')
        self.berries = Pocket('Berries')
        self.key = Pocket('Key Items')
        self.pockets = ['items', 'pokeballs', 'machines', 'berries', 'key']

    def __str__(self):
        return '\n'.join([f'[{len(getattr(self, pocket))}] {getattr(self, pocket).name}' for pocket in self.pockets])

    def __repr__(self):
        return f'<class {self.__class__.__name__}>'

    def add(self, item: object):
        pocket = getattr(self, self.get_pocket(item))
        pocket.add(item)

    def use(self, item: object):
        pocket_name = self.get_pocket(item)
        pocket = getattr(self, pocket_name)
        if pocket_name == 'machines':
            item_from_pocket = pocket.use(item)
            machine = client.get_machine(pocket.use(item).name)
            return client.get_move(machine.move.name)

    def discard(self, item: object, amount: int):
        pocket = getattr(self, self.get_pocket(item))
        pocket.discard(item)

    def remove(self, item: object):
        pocket = getattr(self, self.get_pocket(item))
        pocket.remove(item)

    def category(self, item: object):
        return client.get_item_category(item.category.name)

    def get_pocket(self, item: object):
        pocket = self.category(item).pocket.name
        if hasattr(self, pocket):
            return pocket
        else:
            return 'items'


class Pocket:
    def __init__(self, name: str):
        self.name = name
        self.maxlen = 30
        self.items = []

    def __str__(self):
        return "\n".join([f'[{item.count}] {item.name}' for item in self.items])

    def __repr__(self):
        return f'<class {self.__class__.__name__}>'

    def __len__(self):
        return len(set(self.names))

    def add(self, item: object):
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

    def remove(self, item: object):
        self.items.remove(self.get(item))
        print(f"Removed {item.name}")

    def discard(self, item: object, amount: int):
        item_from_pocket = self.get(item)
        if item_from_pocket.count >= amount:
            item_from_pocket.count -= amount
            if item_from_pocket.count == 0:
                self.remove(item_from_pocket)
            else:
                print(f'Removed {amount} {item_from_pocket.name}.')
        else:
            print(f'Not enough {item_from_pocket.name}. Total: {item_from_pocket.count}')

    def get(self, item: object):
        if item.name in self.names:
            index = self.names.index(item.name)
            return self.items[index]
        else:
            print(f"Item {item.name} is not in pocket")
            return None

    def use(self, item: object, pokemon: object):
        item_from_pocket = self.get(item)
        if item_from_pocket:
            item_from_pocket.count -= 1
            if item_from_pocket.count == 0:
                self.remove(item_from_pocket)
            return item_from_pocket

    @property
    def names(self):
        return [item.name for item in self.items]


if __name__ == '__main__':
    # bag = Bag()
    # bag.add(client.get_item('sun-stone'))
    # bag.add(client.get_item('sun-stone'))
    # print(bag)
    pass
