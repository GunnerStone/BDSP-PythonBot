import requests
import functools
import operator
from enum import Enum

# A memoizing decorator
memoize = functools.lru_cache(maxsize=None)

# The multiplier types I care about
multiplier_types = {'no_damage_to': 0, 'half_damage_to': 0.5, 'double_damage_to': 2}

# A dict that keeps track of resource types
stored_resource_types = {}


class PokException(Exception):
    """
    A custom exception because apparently just using Exception for everything causes problems
    """
    
    pass


class ResourceType(Enum):
    """
    An enumeration for supported resource types because I prefer that typos cause errors
    """
    
    pokemon = 1
    type = 2
    move = 3


@memoize
def get_raw(url):
    """
    A memoizing wrapper for requests.get, to avoid sending duplicate requests
    """
    
    return requests.get(url)


def get(resource_type, id):
    """
    A wrapper for get_raw that checks the response
    """
    
    if type(id) == str:
        id = id.lower()
    
    request_str = 'https://pokeapi.co/api/v2/{}/{}/'.format(resource_type.name, id)
    result = get_raw(request_str)
    
    if result.ok:
        return result.json()
    else:
        raise PokException('"{}" is not a {}'.format(id, resource_type.name))


def get_pokemon_typenames(pokemon):
    """
    Returns the specified pokemon's type(s) as a set of strings
    """
    
    type_list = get(ResourceType.pokemon, pokemon)['types']
    return {slot['type']['name'] for slot in type_list}


def get_move_typename(move):
    """
    Returns the specified move's type as a string
    """
    
    return get(ResourceType.move, move)['type']['name']


def get_type(type):
    """
    Returns the dict structure associated with the specified pokemon type
    """
    
    return get(ResourceType.type, type)


def is_resource_type(id, resource_type):
    """
    Determines whether the specified item is of the specified type
    """
    
    if id in stored_resource_types.keys():
        return stored_resource_types[id] == resource_type
    else:
        try:
            get(resource_type, id)
            stored_resource_types[id] = resource_type
            return True
        except PokException:
            return False


def is_pokemon(id):
    """
    Determines whether the specified item is a pokemon
    """
    
    return is_resource_type(id, ResourceType.pokemon)


def is_move(id):
    """
    Determines whether the specified item is a move
    """
    
    return is_resource_type(id, ResourceType.move)


def is_type(id):
    """
    Determines whether the specified item is a pokemon type
    """
    
    return is_resource_type(id, ResourceType.type)


def get_attacker_type(id):
    """
    Returns the specified resource's type as a string as long as it is a move or type
    """
    
    if is_type(id):
        return id
    elif is_move(id):
        return get_move_typename(id)
    else:
        raise PokException('"{}" is not a valid move or type.'.format(id))


def get_defender_types(id):
    """
    Returns the specified resource's type as a set of strings as long as it is a pokemon or type
    """
    
    if is_type(id):
        return {id}
    elif is_pokemon(id):
        return get_pokemon_typenames(id)
    else:
        raise PokException('"{}" is not a valid pokemon or type.'.format(id))


def get_damage_relations(type):
    """
    Gets the damage relations from a specified type to other types and returns them as a dict of sets
    """
    
    damage_relations = get_type(type)['damage_relations']
    return {
        multiplier_type: {x['name'] for x in types}
        for multiplier_type, types in damage_relations.items()
        if multiplier_type in multiplier_types
    }


def get_multiplier(attacker_type, defender_type):
    """
    Returns a multiplier for single attacker and defender types
    """
    
    # Get the damage relationships for the attacking type
    damage_relations = get_damage_relations(attacker_type)
    
    for multiplier_type, types in damage_relations.items():
        if defender_type in types:
            return multiplier_types[multiplier_type]
    
    return 1


def get_multipliers(*params):
    """
    Determines the overall multiplier for a pokemon of specified type(s) attacking another pokemon of specified type(s)
    Accepts the types as any one of the following:
        A string with an attacker move/type, followed by '->', followed by a collection containing either a defender pokemon or defender pokemon type(s)
        A string containing a type/move for the attacker and a set of for the defender
        A string containing a type/move for the attacker, with the remaining parameters as types
    Returns the multiplier
    """
    
    # Parse the params
    if len(params) == 1:
        attacker_name, defender_names = map(str.strip, params[0].split('->'))
        defender_names = defender_names.split()
    elif len(params) == 2:
        attacker_names, defender_names = params
        
        # make sure the defenders are a set
        if type(defender_names) == list:
            defender_names = set(defender_names)
        elif type(defender_names) == set:
            pass
        else:
            defender_names = {defender_names}
    elif len(params) > 2:
        attacker_name = params[0]
        defender_names = set(params[1:])
    else:
        raise ValueError("Incorrect number of arguments")
    
    attacker_name = attacker_name.replace(' ', '-')
    
    # Get a hard, cold type for the attacker
    attacker_type = get_attacker_type(attacker_name)
    
    # Get a set of hard, cold types for the defender
    defender_types = set()
    for name in defender_names:
        defender_types.update(get_defender_types(name))
    
    # Enforce restrictions on defender types (the first must be a pokemon or a type and the rest must be types)
    for name in defender_names[1:]:
        if not is_type(name):
            raise PokException('"{}" is not a valid type'.format(name))
    
    # Get a list of all multipliers for all combinations of 
    multipliers = (get_multiplier(attacker_type, defender_type) for defender_type in defender_types)
    
    # Multiply together all the multipliers
    return functools.reduce(operator.mul, multipliers)


"""
Returns multipliers for specified pokemon pairings until an empty line is read
Alternatively, it can also print out the type(s) of moves and pokemon
"""
def calculate_type_effectiveness(attacking_move, defending_pokemon_name):
    """
    Calculates the type effectiveness of a move against a pokemon
    """
    
    # Get the attacking move's type
    attacking_move_type = get_move_typename(attacking_move)
    
    # Get the defending pokemon's types
    defending_pokemon_types = get_pokemon_typenames(defending_pokemon_name)
    
    # Get the multipliers for each combination of types
    multipliers = (get_multiplier(attacking_move_type, defending_pokemon_type) for defending_pokemon_type in defending_pokemon_types)
    
    # Multiply together all the multipliers
    return functools.reduce(operator.mul, multipliers)

