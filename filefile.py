import json
import requests

BASE_URL = 'https://api.scryfall.com'


def downloader():
    cards = {}

    data = requests.get(BASE_URL + '/cards').json()

    # Grabs data of most cards and saves them in a dict
    while data['has_more']:
        for element in data['data']:
            cards[element['name']] = element
        data = requests.get(data['next_page']).json()
        print('I am on page ' + data['next_page'][-3:])

    # Grabs the last page
    for element in data['data']:
        cards[element['name']] = element
    print('I am done')

    # Save the cards in a json file
    with open('cardict', 'w') as fo:
        json.dump(cards, fo)


def cardfinder():
    while True:
        cardname = input('Card pls:')
        if cardname in cardict.keys():
            print(cardict[cardname]['image_uris']['png'])
            break
        print('Did you mean any of these:')
        print(autocomplete(cardname))

def autocomplete(cardname):
    candidates = []
    for element in cardict.keys():
        if element[:len(cardname)] == cardname:
            candidates = candidates + element



try:
    cardict = json.load(open('cardict'))
except FileNotFoundError:
    downloader()
    cardict = json.load(open('cardict'))

cardfinder()