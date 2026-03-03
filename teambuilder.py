import json

with open('pokedex.json') as f:
  pokedex = json.load(f)

print(len(pokedex))
print(pokedex[0])
