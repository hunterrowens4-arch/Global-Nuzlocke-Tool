import json
import shutil


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def show_help(pokedex, roster, current_leg):
    help_text = """
      Violet's Nuzlocke Companion Commands
------------------------------------------------
Help    - Show this list of options
Roster  - Show options for managing your roster
Analyze - Show options for analyzing your roster
Legacy  - Show options for managing your legacy
New     - Start a new leg, or a fresh run
Reset   - Reset your roster
Exit    - Save and quit
Quit    - Exit without saving
"""
    print(help_text)


def show_roster_options(pokedex, roster, current_leg):
    roster_options = """
              Roster Options
------------------------------------------
Show   - Show your current roster
Add    - Add a pokemon to your roster
Evolve - Evolve a pokemon in your roster
Kill   - Mark a pokemon as dead
Edit   - Edit a pokemon in your roster
Delete - Delete a pokemon from your roster
"""
    print(roster_options)


def show_filters(pokedex, roster, current_leg):
    filter_options = """ 
                       Show Roster Options
-----------------------------------------------------------------
All           - Show all pokemon in your roster !NOT IMPLEMENTED!
Alive         - Show all alive pokemon in your roster !NOT IMPLEMENTED!
Dead          - Show all dead pokemon in your roster !NOT IMPLEMENTED!
Legends       - Show all legendary pokemon in your roster !NOT IMPLEMENTED!
Type          - Show pokemon in your roster by type !NOT IMPLEMENTED!
Availability  - Show pokemon in your roster by availability !NOT IMPLEMENTED!
Championships - Show pokemon in your roster by championship count !NOT IMPLEMENTED!
BST           - Show pokemon in your roster by base stat total !NOT IMPLEMENTED!
"""
    print(filter_options)


def add_pokemon_to_roster(pokedex, roster, current_leg):
    mon = None
    while mon == None:
        species = input(
            'What species of Pokemon did you catch?\n>>').lower().strip()
        if species == 'exit':
            return
        nickname = input(
            'What nickname would you like to give it? (Press enter to skip)\n>>').strip()
        for p in pokedex:
            if p['name']['english'].lower() == species:
                mon = p
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
                break

    roster.append({
        'no': mon.get('id', 0),
        'nickname': nickname if nickname else None,
        'name': mon['name']['english'].capitalize(),
        'types': [t.capitalize() for t in mon.get('type', [])],
        'stats': stats,
        'origin': current_leg,
        'availability': [current_leg],
        'championships': 0,
        'legend': False,
        'inheritance_count': 0,
        'inheritance': [],
        'status': 'alive'
    })

    print(
        f'Successfully added {mon["name"]["english"].capitalize()} to your roster!')
    print(roster[-1])
    print(f'You now have {len(roster)} pokemon in your roster.')


def evolve_pokemon(pokedex, roster, current_leg):
    target = input(
        'Which Pokemon would you like to evolve? (Enter nickname or species)\n>>').strip().lower()
    mon = None
    for p in roster:
        if p['nickname'].lower() == target:
            mon = p
            break
        elif p['name'].lower() == target:
            mon = p
            break
    if not mon:
        print(f'No Pokemon by that name or species was found in the roster.')
        return
    evo_no = mon['no'] + 1
    evo = None
    for p in pokedex:
        if p['id'] == evo_no:
            evo = p
            break
    if not evo:
        print(
            f'{mon["name"]} cannot evolve or its evolution is not in the pokedex.')
        return
    confirmation = input(
        f'Are you sure you want to evolve {mon["nickname"] if mon["nickname"] else mon["name"]} into {evo["name"]["english"]}? (y/n)\n>>').strip().lower()
    if confirmation == 'y':
        mon['no'] = evo['id']
        mon['name'] = evo['name']['english'].capitalize()
        mon['types'] = [t.capitalize() for t in evo.get('type', [])]
        base = evo.get('base', {})
        mon['stats'] = {
            'hp': base.get('HP', 0),
            'atk': base.get('Attack', 0),
            'def': base.get('Defense', 0),
            'spa': base.get('Sp. Attack', 0),
            'spd': base.get('Sp. Defense', 0),
            'spe': base.get('Speed', 0)
        }
        print(
            f'Successfully evolved into {mon["name"]}!')
    else:
        print('Evolution cancelled.')


def kill_pokemon(pokedex, roster, current_leg):
    deceased = input(
        'Which Pokemon fell in combat? (Enter nickname)\n>>').strip().lower()
    mon = None
    for p in roster:
        if p['nickname'] and p['nickname'].lower() == deceased:
            mon = p
            break
        elif p['name'].lower() == deceased:
            mon = p
            break
    if not mon:
        print(f'No Pokemon by that name or species was found in the roster.')
        return
    if mon['status'] == 'dead':
        print(
            f'{mon["nickname"] if mon["nickname"] else mon["name"]} is already dead.')
        return
    mon['status'] = 'dead'
    print(f'{mon["nickname"] if mon["nickname"] else mon["name"]} is now dead.')


def show_edit_options(pokedex, roster, current_leg):
    edit_options = """
                     Edit Options
------------------------------------------------------
Nickname          - Edit a pokemon's nickname
Inheritance Count - Edit a pokemon's inheritance count !NOT IMPLEMENTED!
Inherited Moves   - Edit a pokemon's inherited moves !NOT IMPLEMENTED!
"""
    print(edit_options)


def edit_nickname(pokedex, roster, current_leg):
    while True:
        target = input(
            'Which Pokemon would you like to rename?\n>>').strip().lower()
        if target == 'exit':
            return
        mon = None
        for p in roster:
            if p['nickname'] and p['nickname'].lower() == target:
                mon = p
                break
            elif p['name'].lower() == target:
                mon = p
                break
        if not mon:
            print(f'No Pokemon by that name or species was found in the roster.')
            continue
        new_nickname = input(
            f'What would you like to change {mon["nickname"] if mon["nickname"] else mon["name"]}\'s nickname to? (press Enter to cancel)\n>>').strip()
        if new_nickname:
            mon['nickname'] = new_nickname
            print(
                f'Successfully changed nickname to {new_nickname}.')
        else:
            print(f'{mon["nickname"]}\'s nickname was not changed.')
        confirmation = False
        while confirmation == False:
            again = input(
                'Would you like to rename another Pokemon? (y/n)\n>>').strip().lower()
            if again == 'y':
                confirmation = True
            elif again == 'n':
                return
            else:
                print('Invalid input. Please enter "y" or "n".')


def delete_pokemon(pokedex, roster, current_leg):
    target = input(
        'Which Pokemon would you like to delete from your roster? (Enter nickname or species)\n>>').strip().lower()
    mon = None
    for p in roster:
        if p['nickname'] == target:
            mon = p
            break
        elif p['name'].lower() == target:
            mon = p
            break
    if not mon:
        print(f'No Pokemon by that name or species was found in the roster.')
        return
    confirmation = input(
        f'Are you sure you want to delete {mon["nickname"] if mon["nickname"] else mon["name"]} from your roster? This action cannot be undone, except by the "quit" command. (y/n)\n>>').strip().lower()
    if confirmation == 'y':
        roster.remove(mon)
        print(
            f'{mon["nickname"] if mon["nickname"] else mon["name"]} has been deleted from your roster.')
    else:
        print('Deletion cancelled.')


def show_analysis_options(pokedex, roster, current_leg):
    analysis_options = """
                                       Analysis Options
------------------------------------------------------------------------------------------------
Coverage - show your type coverage + recommend Pokemon to add to your team based on coverage !NOT IMPLEMENTED!
Weakness - show your type weaknesses + recommend Pokemon to add to your team based on weaknesses !NOT IMPLEMENTED!
BST - show your team's base stat total + recommend Pokemon to add to your team based on BST !NOT IMPLEMENTED!
"""
    print(analysis_options)


def show_legacy_options(pokedex, roster, current_leg):
    legacy_options = """
            Legacy Options
--------------------------------------
Champion - mark a Pokemon as a champ !NOT IMPLEMENTED!
HOF - save a team to the hall of fame !NOT IMPLEMENTED!
Legend - start a Pokemon's legacy !NOT IMPLEMENTED!
"""
    print(legacy_options)


def new_game(pokedex, roster, current_leg):
    current_leg = input('What leg are you starting?\n>>').lower().strip()
    config['current_leg'] = current_leg
    print(f'You are now playing Pokemon {config['current_leg'].title()}')
    if current_leg in ['red', 'blue', 'yellow']:
        config['attempt'] += 1
        print(
            f'This is attempt #{config['attempt']} of Pokemon {current_leg.title()}.')
        reset = input(
            'Would you like to reset your roster? (y/n)\n>>').lower().strip()
        if reset == 'y':
            roster.clear()
            print('Roster has been reset.')
    return current_leg


def reset_roster(pokedex, roster, current_leg):
    confirmation = input(
        'Are you sure you want to reset your roster? This action cannot be undone, other than command: "quit". (y/n)\n>>').lower().strip()
    if confirmation == 'y':
        roster.clear()
        print('Roster has been reset.')
    else:
        print('Roster reset cancelled.')


commands = {
    'help': show_help,
    'roster': show_roster_options,
    'analyze': show_analysis_options,
    'legacy': show_legacy_options,
    'reset': reset_roster,
    'show': show_filters,
    'add': add_pokemon_to_roster,
    'evolve': evolve_pokemon,
    'kill': kill_pokemon,
    'edit': show_edit_options,
    'nickname': edit_nickname,
    'delete': delete_pokemon
}

config = load_json('data/config.json')
pokedex = load_json('data/pokedex.json')
roster = load_json('data/roster.json')

current_leg = config['current_leg']

print('\nWelcome to Violet\'s Nuzlocke Companion!\n')
print(
    f'You are currently playing attempt #{config["attempt"]} of Pokemon {current_leg.title()}.')
print(f'You currently have {len(roster)} pokemon available in this leg.')
print(
    f'{sum(1 for p in roster if p["status"] == "dead")} pokemon have died in total.\n')

while True:
    action = input(
        'What would you like to do? (Type "Help" for a list of options)\n>>').lower().strip()
    if action in commands:
        commands[action](pokedex, roster, current_leg)
    elif action == 'new':
        current_leg = new_game(pokedex, roster, current_leg)
    elif action == 'quit':
        print('Exiting without saving...\n')
        break
    elif action == 'exit':
        print('Saving and exiting...')
        shutil.copy('data/roster.json',
                    f'data/roster_backup_{current_leg}.json')
        with open('data/roster.json', 'w', encoding='utf-8') as f:
            json.dump(roster, f, indent=2)
        shutil.copy('data/config.json',
                    f'data/config_backup_{current_leg}.json')
        with open('data/config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        break
    elif action == 'debug':
        print(f'Roster Length: {len(roster)}')
        print(
            f'Last Pokemon in Roster: {roster[-1] if roster else "Roster is empty."}')
        print(f'Evo Target: {roster[3]}')
    else:
        print('Invalid action. Type "Help" for a list of options.')

# way later ideas:
#     recommend optimal team of 6
#     risk analysis before important battles
#     web based version / GUI / mobile app
#     validate that evolutions are possible based on current leg and pokedex data (ie no gen 2 evos in gen 1, allowing Golbat => Crobat instead of => Oddish, etc)
