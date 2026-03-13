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
Roster  - View and manage your roster
Analyze - Show options for analyzing your roster
Legacy  - Show options for managing your legacy
New     - Start a new leg, or a fresh run
Reset   - Reset your roster
Exit    - Save and quit
Quit    - Exit without saving"""
    print(help_text)

def show_filters(pokedex, roster, current_leg):
    filter_options = """ 
                       Show Roster Options
-----------------------------------------------------------------
Alive         - Show all alive pokemon in your roster
Dead          - Show all dead pokemon in your roster
Type          - Show pokemon in your roster by type
Availabile    - Show pokemon in your roster by availability
Championships - Show pokemon in your roster by championship count !NOT IMPLEMENTED!
BST           - Show pokemon in your roster by base stat total !NOT IMPLEMENTED!
"""
    print(filter_options)


def show_roster(pokedex, roster, current_leg):
    for p in roster:
        print(f'{p['nickname']} - {p['name']}, {p['status']}, championships: {p['championships']}')
    while True:
        print('\nWhat would you like to do with your roster?')
        roster_choice = input('(add / evolve / kill / edit / delete / filter / done)\n>> ').lower().strip()
        if roster_choice in roster_commands:
            roster_commands[roster_choice](pokedex, roster, current_leg)
        elif roster_choice == 'done':
            break
        else:
            print('Invalid choice, please enter a valid selection.')


def show_alive(pokedex, roster, current_leg):
    n = 0
    for p in roster:
        if p['status'] == 'dead':
            continue
        print(f'{p['nickname']} - {p['name']}, championships: {p['championships']}')
        n += 1
    print(f'You have {n} living Pokemon.')


def show_dead(pokedex, roster, current_leg):
    n = 0
    for p in roster:
        if p['status'] == 'alive':
            continue
        print(f'{p['nickname']} - {p['name']}, championships: {p['championships']}')
        n += 1
    print(f'You have {n} dead Pokemon.')


def show_type(pokedex, roster, current_leg):
    n = 0
    target_type = input('\nWhat type would you like to see?\n>> ').capitalize()
    print('')
    for p in roster:
        if target_type not in p['types']:
            continue
        p_type1 = p['types'][0]
        p_type2 = None
        try:
            p_type2 = p['types'][1]
        except:
            pass
        if p_type2:
            print(f'{p['nickname']} - {p['name']}, {p_type1}-{p_type2}, {p['status']}, championships: {p['championships']}')
        else:
            print(f'{p['nickname']} - {p['name']}, {p_type1}, {p['status']}, championships: {p['championships']}')
        n += 1
    if n == 0:
        print('No pokemon were found in the roster by that type.')
    print(f'You have {n} {target_type} type Pokemon.')


def show_bst(pokedex, roster, current_leg):
    stat_list = list()
    while True:
        print('\nWhich stat would you like to see?')
        stat = input('HP | Atk | Def | Spa | Spd | Spe\n>> ').lower().strip()
        if stat in ['hp', 'atk', 'def', 'spa', 'spd', 'spe']:
            for p in roster:
                stat_list.append((p['nickname'], p['name'], p['stats'][stat]))
        else:
            print('Invalid selection, please provide a valid selection.')
        sorted_stat_list = sorted(stat_list, key=lambda x: x[2], reverse=True)
        for mon in sorted_stat_list:
            print(f'{mon[0]} - {mon[1]}, {stat.capitalize()}: {mon[2]}')
        break


def show_available(pokedex, roster, current_leg):
    for p in roster:
        if current_leg not in p['availability']:
            continue
        print(f'{p['nickname']} - {p['name']}, {p['status']}, championships: {p['championships']}')


def add_pokemon_to_roster(pokedex, roster, current_leg):
    mon = None
    while mon == None:
        species = input(
            '\nWhat species of Pokemon did you catch?\n>> ').lower().strip()
        if species == 'exit':
            return
        if any(p['name'].lower() == species for p in roster):
            print('\nThat pokemon is already in your roster.')
            continue
        nickname = input(
            '\nWhat nickname would you like to give it? (Press enter to skip)\n>> ').strip()
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
        f'\nSuccessfully added {mon["name"]["english"].capitalize()} to your roster!')
    print(roster[-1])
    print(f'You now have {len(roster)} pokemon in your roster.')


def evolve_pokemon(pokedex, roster, current_leg):
    target = input(
        '\nWhich Pokemon would you like to evolve? (Enter nickname or species)\n>>').strip().lower()
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
        f'\nAre you sure you want to evolve {mon["nickname"] if mon["nickname"] else mon["name"]} into {evo["name"]["english"]}? (y/n)\n>>').strip().lower()
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
            f'\nSuccessfully evolved into {mon["name"]}!')
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

def edit_nickname(pokedex, roster, current_leg):
    while True:
        target = input(
            '\nWhich Pokemon would you like to rename?\n>>').strip().lower()
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
            f'\nWhat would you like to change {mon["nickname"] if mon["nickname"] else mon["name"]}\'s nickname to? (press Enter to cancel)\n>>').strip()
        if new_nickname:
            mon['nickname'] = new_nickname
            print(
                f'\nSuccessfully changed nickname to {new_nickname}.')
        else:
            print(f'{mon["nickname"]}\'s nickname was not changed.')
        confirmation = False
        while confirmation == False:
            again = input(
                '\nWould you like to rename another Pokemon? (y/n)\n>>').strip().lower()
            if again == 'y':
                confirmation = True
            elif again == 'n':
                return
            else:
                print('Invalid input. Please enter "y" or "n".')


def delete_pokemon(pokedex, roster, current_leg):
    target = input(
        '\nWhich Pokemon would you like to delete from your roster? (Enter nickname or species)\n>> ').strip().lower()
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
    confirmation = input(
        f'\nAre you sure you want to delete {mon["nickname"] if mon["nickname"] else mon["name"]} from your roster? This action cannot be undone, except by the "quit" command. (y/n)\n>> ').strip().lower()
    if confirmation == 'y':
        roster.remove(mon)
        print(
            f'\n{mon["nickname"] if mon["nickname"] else mon["name"]} has been deleted from your roster.')
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
Legacy - show your legends !NOT IMPLEMENTED!
Champion - mark a Pokemon as a champ !NOT IMPLEMENTED!
HOF - save a team to the hall of fame !NOT IMPLEMENTED!
Legend - start a Pokemon's legacy !NOT IMPLEMENTED!
"""
    print(legacy_options)


def new_game(pokedex, roster, current_leg):
    current_leg = input('\nWhat leg are you starting?\n>> ').lower().strip()
    config['current_leg'] = current_leg
    print(f'\nYou are now playing Pokemon {config['current_leg'].title()}')
    if current_leg in ['red', 'blue', 'yellow']:
        config['attempt'] += 1
        print(
            f'This is attempt #{config['attempt']} of Pokemon {current_leg.title()}.\n')
        reset = input(
            'Would you like to reset your roster? (y/n)\n>> ').lower().strip()
        if reset == 'y':
            roster.clear()
            print('Roster has been reset.')
    return current_leg


def reset_roster(pokedex, roster, current_leg):
    confirmation = input(
        '\nAre you sure you want to reset your roster? This action cannot be undone, other than command: "quit". (y/n)\n>> ').lower().strip()
    if confirmation == 'y':
        roster.clear()
        print('Roster has been reset.')
    else:
        print('Roster reset cancelled.')


commands = {
    'available': show_available,
    'bst': show_bst,
    'help': show_help,
    'roster': show_roster,
    'analyze': show_analysis_options,
    'legacy': show_legacy_options,
    'reset': reset_roster,
    'alive': show_alive,
    'dead': show_dead,
    'type': show_type,
    'add': add_pokemon_to_roster,
    'evolve': evolve_pokemon,
    'kill': kill_pokemon,
    'edit': edit_nickname,
    'delete': delete_pokemon
}

roster_commands = {
    'add': add_pokemon_to_roster,
    'alive': show_alive,
    'available': show_available,
    'bst': show_bst,
    'dead': show_dead,
    'delete': delete_pokemon,
    'edit': edit_nickname,
    'evolve': evolve_pokemon,
    'filter': show_filters,
    'kill': kill_pokemon,
    'type': show_type
}


types = ['normal', 'fire', 'water', 'grass', 'electric', 'ice', 'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']


config = load_json('data/config.json')
pokedex = load_json('data/pokedex.json')
roster = load_json('data/roster.json')

current_leg = config['current_leg']

print('\nWelcome to Violet\'s Nuzlocke Companion!\n')
print(
    f'You are currently playing attempt #{config["attempt"]} of Pokemon {current_leg.title()}.')
print(f'You have caught {len(roster)} pokemon in total.')
print(
    f'{sum(1 for p in roster if p["status"] == "dead")} pokemon have died in total.')

a = 0

for p in roster:
    if current_leg in p['availability']:
        a += 1
print(f'You have {a} Pokemon available to you so far in this leg.')

while True:
    action = input(
        '\nWhat would you like to do? (Type "Help" for a list of options)\n>> ').lower().strip()
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
#     team functionality
#     recommend optimal team of 6
#     risk analysis before important battles
#     web based version / GUI / mobile app
#     validate that evolutions are possible based on current leg and pokedex data (ie no gen 2 evos in gen 1, allowing Golbat => Crobat instead of => Oddish, etc)
