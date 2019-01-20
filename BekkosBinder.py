import json
import requests

MKM_URL = 'https://api.cardmarket.com/ws/v2.0/priceguide'
SCRYFALL_URL = 'https://api.scryfall.com'

sets_of_interest = ['xln', 'rix', 'dom', 'gs1', 'm19', 'grn', 'rna', 'war', 'm20']

def dict_creator():
    binder = {}

    for element in sets_of_interest:
        binder[element] = {}

    pages = requests.get(SCRYFALL_URL + '/cards').json()
    i = -1

    while pages['has_more']:
        for card in pages['data']:
            if card.get('set', 'none') in sets_of_interest:
                binder[card['set']][card['name']] = {'owners': 'copies'}

        while not pages['next_page'][i-1] == '=':
            i = i-1
        print('I am done with page ' + pages['next_page'][i:] + ' out of ' + str(round(pages['total_cards']/175)+1))

        pages = requests.get(pages['next_page']).json()

    for card in pages['data']:
            if card.get('set', 'none') in sets_of_interest:
                binder[card['set']][card['name']] = {'owners': 'copies'}

    with open('standart_lib', 'w') as fo:
        json.dump(binder, fo)

    return binder


try:
    binder = json.load(open('binder'))
except FileNotFoundError:
    print('Downloading Card Information:')
    binder = dict_creator()
