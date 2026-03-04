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
Analyze - Show options for analyzing your roster !NOT IMPLEMENTED!
Legacy  - Show options for managing your legacy !NOT IMPLEMENTED!
Stats   - Show your current stats !NOT IMPLEMENTED!
New     - Start a new leg, or a fresh run !NOT IMPLEMENTED!
Exit    - Save and quit
"""
    print(help_text)


def show_roster_options(pokedex, roster, current_leg):
    roster_options = """
              Roster Options
------------------------------------------
Show   - Show your current roster
Add    - Add a pokemon to your roster
Evolve - Evolve a pokemon in your roster !NOT IMPLEMENTED!
Kill   - Mark a pokemon as dead
Edit   - Edit a pokemon in your roster
Delete - Delete a pokemon from your roster !NOT IMPLEMENTED!
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
            else:
                print(f'Warning: {species} not found in Pokedex.')
                continue

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
Inheritance Count - Edit a pokemon's inheritance count
Inherited Moves   - Edit a pokemon's inherited moves
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


commands = {
    'help': show_help,
    'roster': show_roster_options,
    'show': show_filters,
    'add': add_pokemon_to_roster,
    'kill': kill_pokemon,
    'edit': show_edit_options,
    'nickname': edit_nickname
}

config = load_json('data/config.json')
pokedex = load_json('data/pokedex.json')
roster = load_json('data/roster.json')

current_leg = config['current_leg']

print('Welcome to Violet\'s Nuzlocke Companion!')
print(
    f'You are currently playing attempt #{config["attempt"]} of Pokemon {current_leg.title()}.')
print(f'You currently have {len(roster)} pokemon available in this leg.')
print(
    f'{sum(1 for p in roster if p["status"] == "dead")} pokemon have died in total.')

while True:
    action = input(
        'What would you like to do? (Type "Help" for a list of options)\n>>').lower().strip()
    if action in commands:
        commands[action](pokedex, roster, current_leg)
    elif action == 'exit':
        print('Saving and exiting...')
        shutil.copy('data/roster.json',
                    f'data/roster_backup_{current_leg}.json')
        with open('data/roster.json', 'w', encoding='utf-8') as f:
            json.dump(roster, f, indent=2)
        break
    elif action == 'debug':
        print(f'pokedex[:10] = {pokedex[:10]}')
        print(f'roster[-10:] = {roster[-10:]}')
    else:
        print('Invalid action. Type "Help" for a list of options.')

# actions to add:
#     roster - show options for managing your roster
#         show - show your current roster
#             all
#             alive
#             dead
#             legends
#             type filter
#             origin filter
#             by championship count
#             bst
#         add - add a pokemon to your roster (can later auto-assign origin, will also need to change origin to str instead of int, have it redirect to edit if pokemon is aready in roster)
#         evolve - evolve a pokemon in your roster
#         kill - mark a pokemon as dead
#         edit - edit a pokemon in your roster, can implement sub-options to edit certain attributes
#             nickname
#             inherited move count
#             inherited moves
#         delete - delete a pokemon from your roster
#     analysis - show options for analyzing your roster
#         coverage - show your type coverage + recommend pokemon to add to your team based on coverage
#         weaknesses - show your type weaknesses + recommend pokemon to add to your team based on weaknesses
#         bst - show your team's base stat total + recommend pokemon to add to your team based on bst
#     legacy - show options for managing your legacy
#         champion - mark a pokemon as a champion
#         hof - save a team to the hall of fame
#         legend - start a pokemon's legacy
#     stats - show your current stats
#         hof - show your hall of fame teams
#         deaths - show your total number of deaths by leg
#             all (include %)
#             by type
#             by bst
#     new game - start a new leg, or a fresh run
#     exit - save and quit

# way later ideas:
#     recommend optimal team of 6
#     risk analysis before important battles
#     web based version / GUI / mobile app
