from decorators import ResponseTimer
from bs4 import BeautifulSoup
import requests
import json
import os


def type_defense(name, debug=False):
    filepath = os.path.join(os.getcwd(), 'cache', 'type_defense.json')
    # checks if file exists
    if os.path.isfile(filepath):
        with open(filepath, 'r') as js:
            all_types = json.load(js)
    else:
        # if file doesn't exist, creates it with empty dict
        with open(filepath, 'w') as js:
            all_types = {}
            json.dump(all_types, js, indent=2)

    if name not in all_types.keys():
        # if pokemon is not cached requests that information
        if debug:
            requests.get = ResponseTimer(requests.get)
        url = f'https://pokemondb.net/pokedex/{name}'
        with requests.get(url) as response:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            type_tables = soup.findAll('table', attrs={'class': "type-table type-table-pokedex"})
            effects = {}
            for table in type_tables:
                tds = table.findAll('td')
                for td in tds:
                    title = td['title'].split(' ')[0].lower()
                    if (value := td.text):
                        if value == '½':
                            value = 0.5
                        elif value == '¼':
                            value = 0.25
                        elif value == '2':
                            value = 2
                    else:
                        value = 1
                    effect = td['title'].split('=')[-1][1:].replace(' ', '-')
                    effects[title] = {'multiplier': value, 'effect': effect}

            with open(filepath, 'w') as js:
                all_types[name] = effects
                json.dump(all_types, js, indent=2)
    else:
        # if pokemon has already been cached returns its effects
        effects = all_types[name]
    return effects

'''
    def stats(self):
        if not self.local:
            tables = self.soup.findAll('table', attrs={'class': "vitals-table"})
            stat_table = tables[3]
            stats_tr = stat_table.findAll('tr')

            stats = {}
            for tr in stats_tr:
                try:
                    base_value, min_value, max_value = [int(value.text) for value in tr.findAll('td', attrs={'class': 'cell-num'})]
                    value_dict = {'base': base_value, 'min': min_value, 'max': max_value}
                    stats[tr.th.text] = value_dict
                except ValueError:
                    stats[tr.th.text.replace('. ', '_')] = int(tr.find('td', attrs={'class': "cell-total"}).text)
            with open(self.filepath, 'w') as js:
                json.dump(stats, js)
        else:
            with open(self.filepath, 'r') as js:
                stats = json.load(js)
        return stats

    def type_defense(self):
        if not self.local:
            type_tables = self.soup.findAll('table', attrs={'class': "type-table type-table-pokedex"})
            effects = {}
            for table in type_tables:
                tds = table.findAll('td')
                for td in tds:
                    title = td['title'].split(' ')[0].lower()
                    if (value := td.text):
                        if value == '½':
                            value = 0.5
                        elif value == '¼':
                            value = 0.25
                        elif value == '2':
                            value = 2
                    else:
                        value = 1
                    effect = td['title'].split('=')[-1][1:].replace(' ', '-')
                    effects[title] = {'multiplier': value, 'effect': effect}
            with open(self.filepath, 'w') as js:
                json.dump(effects, js)
        else:
            with open(self.filpath, 'r') as js:
                effects = json.load(js)
        return effects
'''
