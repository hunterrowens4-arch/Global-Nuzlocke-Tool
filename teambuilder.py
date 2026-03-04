import json

def load_json(path):
  with open(path) as f:
    return json.load(f)

pokedex = load_json('data/pokedex.json')
roster = load_json('data/roster.json')

print('Welcome to Violet\'s Nuzlocke Companion!')
action = input('What would you like to do? (type "help" for a list of options)\n>>')