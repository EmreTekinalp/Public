"""
Created on 02.09.2013
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: Holds all the namingconventions for pandora's box
"""

import os
import json


class NamingConvention():
    """Imports naming conventions from the respective .json file and puts them
    into class variables.
    """
    def __init__(self):
        namingconventions = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                 'data', 'strings', 'namingconvention.json')
        namingconventions = json.load(open(namingconventions))
        for key, value in namingconventions.items():
            setattr(NamingConvention, key, value)
        # end for constant in constants
    # end def __init__
# end class NamingConvention
