"""
Created on 21.09.2013
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: Reads data from json files and provides them as a RigData object.
"""
import os
import json
import collections
from utility import path
reload(path)


def module(module):
    """Parses the .json file of the given datatype and module.
    @param module: The name of the module
    @type module: String
    @return: OrderedDict

    """
    json_path = os.path.join(path.get_root_path(), 'data', 'modules',
                             ('%s.json' % module))
    data = json.load(open(json_path), object_pairs_hook=collections.OrderedDict)
    return data
# end def module


def attributedefaults():
    """Returns the dictionary holding defaults for some special, mostly enum,
    attributes.

    """
    json_path = os.path.join(path.get_root_path(), 'data', 'modules',
                             'attributedefaults.json')
    data = json.load(open(json_path), object_pairs_hook=collections.OrderedDict)
    return data
# end def attributedefaults


def moduledefaults():
    """Returns the dictionary holding the defaults for modules."""
    json_path = os.path.join(path.get_root_path(), 'data', 'modules',
                             'moduledefaults.json')
    data = json.load(open(json_path), object_pairs_hook=collections.OrderedDict)
    return data
# end def moduledefaults
