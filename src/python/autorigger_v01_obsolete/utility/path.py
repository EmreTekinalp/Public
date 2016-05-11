"""
Created on 21.09.2013
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: Returns paths to various folders

"""

import os


def get_root_path():
    return os.path.dirname(os.path.dirname(__file__))
# end def get_root_path

def ui():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)),
                        'ui')
# end def ui

def resource():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)),
                        'ui', 'resource')
# end def resource
