import pokebase as pb

""" Gets the pokemon object from the pokemon name """
# for caching reasons & load times, you should be calling this function as little as possible
def get_pokemon(pokemon_name):
    pokemon_name = pokemon_name.lower()
    pokemon_name = pokemon_name.replace(' ', '-')
    return pb.pokemon(pokemon_name)

