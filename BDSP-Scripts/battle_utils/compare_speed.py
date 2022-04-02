import pokebase as pb
""" Compare base speed of two Pokemon. """
def is_pokemon_faster(user_pokemon_name, opponent_pokemon_name):
    user_pokemon_name = user_pokemon_name.lower()
    opponent_pokemon_name = opponent_pokemon_name.lower()
    # replace any spaces with dashes '-'
    user_pokemon_name = user_pokemon_name.replace(' ', '-')
    opponent_pokemon_name = opponent_pokemon_name.replace(' ', '-')

    user_pokemon = pb.pokemon(user_pokemon_name)
    opponent_pokemon = pb.pokemon(opponent_pokemon_name)
    user_stats = user_pokemon.stats
    opponent_stats = opponent_pokemon.stats

    # loop through each stat and find the speed stat and pull the base values
    for stat in user_stats:
        if stat.stat.name == 'speed':
            user_speed = stat.base_stat
    for stat in opponent_stats:
        if stat.stat.name == 'speed':
            opponent_speed = stat.base_stat
    # compare stats
    if user_speed > opponent_speed:
        return True
    else:
        return False

print(is_pokemon_faster("Jolteon", "charizard"))