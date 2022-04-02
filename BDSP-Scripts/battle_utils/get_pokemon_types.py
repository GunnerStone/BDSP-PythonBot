import pokebase as pb

def get_pokemon_types(pokemon_obj):
    """
    Returns a list of the pokemon's types
    """
    types = pokemon_obj.types
    return [type.type.name for type in types]
