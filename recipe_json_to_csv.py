import pandas as pd
import numpy as np
import json
from collections import defaultdict

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


with open("recipe.json") as inh:
    d = json.load(inh)
    final_d = {}

    # iterate once to find all possible items
    all_items = set()
    for k, v in d.items():
        all_items.add(k)
        ingreds = v["ingredients"]
        for item in ingreds:
            all_items.add(item["name"])

    item_reqs_dict = defaultdict(dict) # dict of dicts: item -> required item -> amount
    for k, v in d.items():
        ingreds = v["ingredients"]
        for item in ingreds:
            item_reqs_dict[k][item["name"]] = item["amount"]

    all_reqs = dict()
    for k in d.keys():
        all_reqs[k] = get_all_reqs(k, item_reqs_dict, all_items)
    df = pd.DataFrame(all_reqs).transpose()

    df.to_csv("recipe.csv")
