import pokebase as pb
import math
""" Calculates the stat for a given pokemon at level X for a given Pokemon. """
def calculate_stat_at_level(pokemon_name, stat_name, level=50,EV=0,IV=0,nature="neutral"):
    pokemon_name = pokemon_name.lower()
    # replace any spaces with dashes '-'
    pokemon_name = pokemon_name.replace(' ', '-')
    pokemon = pb.pokemon(pokemon_name)
    stats = pokemon.stats
    # loop through each stat and find the desired stat and pull the base values
    for stat in stats:
        if stat.stat.name == stat_name:
            base_stat = stat.base_stat
    print(base_stat)
    # calculate the stat
    # HP = floor(0.01 x (2 x Base + IV + floor(0.25 x EV)) x Level) + Level + 10.
    # Other Stats = (floor(0.01 x (2 x Base + IV + floor(0.25 x EV)) x Level) + 5) x Nature.
    if stat_name == 'hp':
        return int(math.floor(0.01 * (2 * base_stat + IV + math.floor(0.25 * EV)) * level) + level + 10)
    else:
        stat_at_level = int(math.floor(0.01 * (2 * base_stat + IV + math.floor(0.25 * EV)) * level) + 5)
    
    # calculate the nature multiplier
    if nature in ['lonely','brave','adamant','naughty'] and stat_name == 'attack':
        return int(stat_at_level * 1.1)
    elif nature in ['bold','relaxed','impish','lax'] and stat_name == 'defense':
        return int(stat_at_level * 1.1)
    elif nature in ['timid','hasty','jolly','naive'] and stat_name == 'speed':
        return int(stat_at_level * 1.1)
    elif nature in ['modest','mild','quiet','rash'] and stat_name == 'special-attack':
        return int(stat_at_level * 1.1)
    elif nature in ['gentle','sassy','careful','calm'] and stat_name == 'special-defense':
        return int(stat_at_level * 1.1)
    elif nature in ['bold','timid','modest','calm'] and stat_name == 'attack':
        return int(stat_at_level * 0.9)
    elif nature in ['lonely','mild','hasty','gentle'] and stat_name == 'defense':
        return int(stat_at_level * 0.9)
    elif nature in ['brave','relaxed','quiet','sassy'] and stat_name == 'speed':
        return int(stat_at_level * 0.9)
    elif nature in ['adamant','impish','jolly','careful'] and stat_name == 'special-attack':
        return int(stat_at_level * 0.9)
    elif nature in ['naughty','rash','lax','naive'] and stat_name == 'special-defense':
        return int(stat_at_level * 0.9)
    else:
        return stat_at_level
