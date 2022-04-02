import sys
import os
""" import necessary util functions """
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # add parent directory to path
import battle_utils
import pokebase as pb
from pokebase import cache

import random


""" Calculates the damage of a move on a pokemon given stats and type effectiveness. """
def calculate_damage(attacking_pokemon_obj, defending_pokemon_obj, move_name, attacking_pokemon_stats, defending_pokemon_stats, attacking_pokemon_level = 50):
    """
    Calculates the damage of a move on a pokemon given stats and type effectiveness.
    """
    # get the pokemon's types
    attacking_pokemon_types = battle_utils.get_pokemon_types(attacking_pokemon_obj)
    defending_pokemon_types = battle_utils.get_pokemon_types(defending_pokemon_obj)

    attacking_pokemon_name = attacking_pokemon_obj.name
    defending_pokemon_name = defending_pokemon_obj.name
    # calculate the type effectiveness
    type_effectiveness = battle_utils.calculate_move_effectiveness(move_name, defending_pokemon_name)
    print("Type effectiveness: " + str(type_effectiveness)+"x")

    # get the base damage of the move from pb
    move = pb.move(move_name)
    move_type = move.type.name
    print("Move type: " + str(move_type))
    damage_class = move.damage_class.name
    print("Damage class: " + str(damage_class))
    base_damage = move.power
    print("Base damage: " + str(base_damage))
    print()

    STAB_Bonus = 1.0
    if move_type in attacking_pokemon_types:
        STAB_Bonus = 1.5
    print("STAB Bonus: " + str(STAB_Bonus))
    
    # calculate the damage of the move
    # does not include weather or burn debuff
    if damage_class == 'physical':
        print("{}'s attack: ".format(attacking_pokemon_name) + str(attacking_pokemon_stats['attack']))
        print("{}'s defense: ".format(defending_pokemon_name) + str(defending_pokemon_stats['defense']))
        damage = int((((2*75)/5 + 2)*base_damage*attacking_pokemon_stats['attack']/defending_pokemon_stats['defense']/50)*random.uniform(0.85,1.0)*type_effectiveness*STAB_Bonus)
    elif damage_class == 'special':
        print("{}'s special attack: ".format(attacking_pokemon_name) + str(attacking_pokemon_stats['special-attack']))
        print("{}'s special defense: ".format(defending_pokemon_name) + str(defending_pokemon_stats['special-defense']))
        damage = int((((2*75)/5 + 2)*base_damage*attacking_pokemon_stats['special-attack']/defending_pokemon_stats['special-defense']/50)*random.uniform(0.85,1.0)*type_effectiveness*STAB_Bonus)
    print("Damage: " + str(damage) + " out of {}'s hp:".format(defending_pokemon_name) + str(defending_pokemon_stats['hp']))
    return damage

def main():
    pokemon_names = ['glaceon', 'garchomp']
    pokemon_levels = [75, 75]
    pokemon_objs = [battle_utils.get_pokemon(pokemon_name) for pokemon_name in pokemon_names]
    squirtle_stats = {
        'hp': battle_utils.calculate_stat_at_level(pokemon_objs[0], 'hp', pokemon_levels[0]),
        'attack': battle_utils.calculate_stat_at_level(pokemon_objs[0], 'attack', pokemon_levels[0]),
        'defense': battle_utils.calculate_stat_at_level(pokemon_objs[0], 'defense', pokemon_levels[0]),
        'special-attack': battle_utils.calculate_stat_at_level(pokemon_objs[0], 'special-attack', pokemon_levels[0]),
        'special-defense': battle_utils.calculate_stat_at_level(pokemon_objs[0], 'special-defense', pokemon_levels[0]),
        'speed': battle_utils.calculate_stat_at_level(pokemon_objs[0], 'speed', pokemon_levels[0])
    }

    charizard_stats = {
        'hp': battle_utils.calculate_stat_at_level(pokemon_objs[1], 'hp', pokemon_levels[1]),
        'attack': battle_utils.calculate_stat_at_level(pokemon_objs[1], 'attack', pokemon_levels[1]),
        'defense': battle_utils.calculate_stat_at_level(pokemon_objs[1], 'defense', pokemon_levels[1]),
        'special-attack': battle_utils.calculate_stat_at_level(pokemon_objs[1], 'special-attack', pokemon_levels[1]),
        'special-defense': battle_utils.calculate_stat_at_level(pokemon_objs[1], 'special-defense', pokemon_levels[1]),
        'speed': battle_utils.calculate_stat_at_level(pokemon_objs[1], 'speed', pokemon_levels[1])
    }

    desired_move = "thunderbolt"
    print("Level {} ".format(pokemon_levels[0]) + pokemon_names[0] + " uses: " + desired_move + " against a Level {} ".format(pokemon_levels[1]) + pokemon_names[1])
    print()
    calculate_damage(pokemon_objs[0], pokemon_objs[1], desired_move,squirtle_stats, charizard_stats)

if __name__ == '__main__':
    main()