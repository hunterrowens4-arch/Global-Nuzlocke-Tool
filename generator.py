import json

with open('data/pokedex.json') as f:
    pokedex = json.load(f)

caught = [
    'bellsprout',
    'butterfree',
    'ditto',
    'dragonair',
    'ekans',
    'fearow',
    'gastly',
    'graveler',
    'grimer',
    'kadabra',
    'krabby',
    'lickitung',
    'magnemite',
    'marowak',
    'nidoran♂',
    'nidorina',
    'parasect',
    'pidgeotto',
    'sandshrew',
    'seel',
    'shellder',
    'tentacruel',
    'vulpix',
    'wartortle',
    'weedle',
    'zubat'
]

n = 0

roster = []
for species in caught:
    mon = next((p for p in pokedex if p['name']['english'].lower() == species.lower()), None)
    if mon:
        base = mon.get('base', {})
        stats = {
            'hp': base.get('HP', 0),
            'atk': base.get('Attack', 0),
            'def': base.get('Defense', 0),
            'spa': base.get('Sp. Attack', 0),
            'spd': base.get('Sp. Defense', 0),
            'spe': base.get('Speed', 0)
        }

        roster.append({
            'no': mon.get('id', 0),
            'name': mon['name']['english'].capitalize(),
            'nickname': None,
            'types': [t.capitalize() for t in mon.get('type', [])],
            'stats': stats,
            'status': 'alive',
            'legend': False,
            'championships': 0,
            'origin': 1,
            'inheritance_count': 0,
            'inheritance': []
        })
    else:
        n += 1
        print(f'Warning: {species} not found in Pokedex. Error count: {n}')

with open('data/roster.json', 'w') as f:
    json.dump(roster, f, indent=2)

print('roster.json generated successfully')