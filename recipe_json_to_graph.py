import pandas as pd
import numpy as np
import json
from collections import defaultdict
import networkx as nx

REMOVE_ITEMS = True

# modified from https://github.com/ingmar/factorio-trees/blob/master/recipes.lua
ITEMS_TO_REMOVE = set([
    "basic-armor",
    "basic-bullet-magazine",
    "heavy-armor",
    #"iron-axe",
    "iron-chest",
    "shotgun",
    "shotgun-shell",
    "small-electric-pole",
    "wooden-chest",
    "basic-modular-armor",
    "burner-mining-drill",
    "pistol",
    #"steel-furnace",
    #"stone-furnace",
    "submachine-gun",
    "burner-inserter",
    "electric-energy-interface",
    "light-armor",
    "modular-armor",
    "power-armor",
    "power-armor-mk2"
])

# remove items containing the following strings
REMOVE_STRINGS = ["ee-", "textplate", "empty-", "fill-", "armor"]


# helper function to accumulate the vector of required ingredients
# use pd.Series() to add the vectors
# calls itself recursively
def _get_all_reqs(item, item_reqs_dict, accum_vector):
    _accum_vector = accum_vector.copy() # must be immutable method
    for required_item, amount in item_reqs_dict[item].items():
        _accum_vector[required_item] += amount
        if required_item in item_reqs_dict:
            _accum_vector = _get_all_reqs(required_item, item_reqs_dict, _accum_vector)
        else:
            continue
    return _accum_vector
#
def get_all_reqs(item, item_reqs_dict, all_items):
    """
    Given a dictionary of the item requirements for each (item -> item required -> amount), as well as the set of all possible ingredients,
    return a dictionary of all the recursive requirements for a given item.
    """
    accum_vector = {k: 0 for k in all_items} # initialize all ingredients with 0
    accum_vector[item] += 1 # give yourself a value of 1, for things like assembler mk2 to associate it with assembler mk1
    accum_vector = pd.Series(accum_vector) # so we can add them
    return _get_all_reqs(item, item_reqs_dict, accum_vector)


def to_remove(k):
    if not REMOVE_ITEMS:
        return False
    _flag = False
    for s in REMOVE_STRINGS:
        if s in k:
            _flag = True
            break
    if not _flag and k in ITEMS_TO_REMOVE:
        _flag = True
    return _flag

directed_graph = nx.DiGraph()

with open("recipe.json") as inh:
    d = json.load(inh)
    keys = list(d.keys())
    for k in keys:
        if to_remove(k):
            del d[k]
    final_d = {}

    # iterate once to find all possible items
    all_items = set()
    for k, v in d.items():

        # do we remove the item?
        if to_remove(k):
            continue

        all_items.add(k)
        ingreds = v["ingredients"]
        for item in ingreds:
            all_items.add(item["name"])

    item_reqs_dict = defaultdict(dict) # dict of dicts: item -> required item -> amount
    for k, v in d.items():
        if to_remove(k):
            continue
        ingreds = v["ingredients"]
        for item in ingreds:
            # create own dictionary of dict of dicts for total requirements
            item_reqs_dict[k][item["name"]] = item["amount"]
            # also add to directed graph
            directed_graph.add_edges_from([(k, item["name"])])

    all_reqs = dict()
    for k in d.keys():
        all_reqs[k] = get_all_reqs(k, item_reqs_dict, all_items)
    df = pd.DataFrame(all_reqs).transpose()

    if REMOVE_ITEMS:
        title = "recipe_filtered"
    else:
        title = "recipe"

    df.to_csv("{}.csv".format(title))

#nx.drawing.nx_pydot.write_dot(directed_graph, "{}.dot".format(title))
#nx.write_graphml(directed_graph, "{}.graphml".format(title))
nx.write_gexf(directed_graph, "{}.gexf".format(title)), 
#undirected_graph = nx.Graph(directed_graph)
