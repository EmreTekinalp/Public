"""
@package: utility.node
@brief: Base implementations of the node interfaces
@author: Emre Tekinalp
@contact: e.tekinalp@icloud.com
"""

import os
import json
import logging
import pymel.core as pm
from maya import cmds
from rigging.pandoras_box.utility import abbreviation

reload(abbreviation)
reload(logging)
logging.basicConfig(format='', level=logging.DEBUG)


class Node(object):

    """Dynamically create a maya node by calling the node as a class method.

    The user has access to the node's input parameters on top of all.
    Under resource/node.config the user can find all relevant maya node
    information. If this config file is missing, a fresh new config file
    will be automatically generated inside the resource package when calling
    this class. This class reads the information given in this config file.

    @usage After instantiating the class, access each individual maya node by
           calling its name as a function, which has as parameters the node
           related input attributes.
    @requires from src.python.utility import abbreviation
    @return PyNode class object.
    @example Here are different examples listed below:

    node = PyNode('C')
    # example 1 create a remapValue
    rmv = node.remapValue()

    # example 2 create a multiplyDivide node and set values as default
    mlt = node.multiplyDivide(input1X=1.3, input2=[2, 1, 6], operation=2)

    # example 3 create a condition node and connect by creation time attributes
    cnd = node.condition(firstTerm=mlt.attr('outputX'),
                         secondTerm=rmv.attr('outValue'),
                         colorIfTrueR=rmv.attr('outValue'),
                         colorIfFalseR=0.0)
    print cnd.getAttr('outColorR')

    # example 4 type in help as a first argument to list all input parameters
    adl = node.addDoubleLinear(help)

    # example 5 typing a string as the first argument renames the node
    mdl = node.multDoubleLinear('myNode', input1=1.0)

    @DONE: Check string object compatibility, otherwise extend class
    @DONE: Optimize class, use recursions and helper functions in code
    @DONE: Implement abbreviation algorithm for individual node suffix
    """

    def __init__(self, side='C', suffix=None):
        """Constructor function of the class.
        @param side <str> Specify the prefix abbreviation.
                          Valid values are 'C', 'L', 'R', 'c', 'l', 'r'.
        """
        # args
        self.side = side
        self.suffix = suffix

        # vars
        self._path = self._get_config_path()
        self._nodes = self._get_nodes()
        self._nodename = None
    # end def __init__

    def _get_config_path(self):
        """Return config file path"""
        return os.path.join(self._get_top(__file__), 'config', 'node.config')
    # end def _get_config_path

    def _get_top(self, path):
        """Recursevily retrieve the top group GravityOfExplosion."""
        if os.path.basename(path) == 'GravityOfExplosion':
            return path
        # end if recursion end
        return self._get_top(os.path.abspath(os.path.join(path, os.pardir)))
    # end def _get_top

    def _get_nodes(self):
        """Read and return node_info.json file otherwise create a new one"""
        if os.path.exists(self._path):
            with open(self._path) as json_file:
                json_data = json.load(json_file)
            # end with open json file
            return json_data
        # end if path exists
        return self._setup_data()
    # end def _get_nodes

    def _setup_data(self):
        """Check node classification, filter, save config file and return"""
        classlist = ['utility', 'shader', 'transform', 'drawdb', 'general']
        nodes = [n for n in pm.allNodeTypes() for c in classlist
                 if cmds.getClassification(n, satisfies=c) if n != 'nexManip']
        data = dict()
        self._get_data(nodes, data)
        self._add_abbreviation(data)
        self._save_config_file(data)
        return data
    # end def _setup_data

    def _get_data(self, nodes, data):
        """Recursive function to store data in a dictionary
        @param nodes <list> list of all maya nodes to iterate through
        @param data <dict> dictionary to store all the node and attribute data
        """
        if not nodes:
            return
        # end if recursion
        nd = cmds.createNode(nodes[0])
        attributes = cmds.listAttr(nd, c=True, w=True)
        attr = dict()
        for at in attributes:
            try:
                typ = cmds.getAttr('%s.%s' % (nd, at), type=True)
                attr[at] = typ
            except:
                pass
            # end try except get attribute
        # end for get attribute type
        cmds.delete(nd)
        data[nodes[0]] = attr
        return self._get_data(nodes[1:], data)
    # end def _get_data

    def _add_abbreviation(self, data):
        """Implement the proper abbreviation and mutate the given dictionary
        @param data <dict> A dictionary containing the relevant attribute data
        """
        abb = abbreviation.Abbreviation()
        for key, value in abb.abbreviate(data.keys()).items():
            if key in data:
                data[key]['__ABBREVIATION__'] = value
            # end if key exists in data
        # end for iterate dictionary
    # end def _add_abbreviation

    def _save_config_file(self, data):
        """Save config file
        @param data <dict> A dictionary containing the relevant attribute data
        """
        with open(self._path, 'w') as json_file:
            json.dump(data, json_file, sort_keys=True, indent=2)
        # end with save file
    # end def _save_config_file

    def __getattr__(self, attr):
        """Override getattr function and return node
        @param attr <str> Name of the node which generates a PyNode
        """
        def _node(*args, **kwargs):
            """Function closure to check, setup and return a pyNode"""
            if attr not in self._nodes:
                raise TypeError('Node is invalid: %s' % attr)
            # end if raise type error
            self._nodename = attr
            return self._setup_node(*args, **kwargs)
        # end def _node
        return _node
    # end def __getattr__

    def _setup_node(self, *args, **kwargs):
        """Setup and return the node
        @param args <list> Storing args from config file as list
        @param kwargs <dict> Storing keyword args from config file as dict
        @DONE use logging instead of printing
        """
        node = None
        if args:
            if args[0] == help:
                msg = "\nValid parameters for the %s node:" % self._nodename
                logging.debug(msg)
                for n in self._nodes[self._nodename].items():
                    if not n[0] == '__ABBREVIATION__':
                        logging.debug('-- %s : <%s>' % (n[0], n[1]))
                    # end if exclude abbreviation
                # end for print parameters and types
                return
            # end if help or set name
            if not self.suffix:
                self.suffix = self._nodes[self._nodename]['__ABBREVIATION__']
            # end if not suffix given use abbreviation list
            name = '%s_%s_%s' % (self.side, args[0], self.suffix)
            node = pm.createNode(self._nodename, n=name)
        else:
            node = pm.createNode(self._nodename)
        # end if args exists

        self._setup_attribute(node, **kwargs)
        self.suffix = None
        return node
    # end def _setup_node

    def _setup_attribute(self, node, **kwargs):
        """Set or connect given output into input attributes
        @param node <pyNode> PyNode object to set and get attributes
        @param kwargs <dict> Data storing the keyword argument information
        """
        for key, val in kwargs.items():
            key = pm.attributeName('%s.%s' % (node, key), l=True)
            if key not in self._nodes[self._nodename].keys():
                attrs = [n for n in self._nodes[self._nodename].keys()
                         if n != '__ABBREVIATION__']
                msg = ("Parameter %s does not exist in node_info.json!"
                       " Valid flags are %s" % (key, attrs))
                raise AttributeError(msg)
            # end if raise attribute error
            if pm.objExists(str(val)):
                val.connect(node.attr(key))
            else:
                node.setAttr(key, val)
            # end if connect or set attribute
        # end for set attribute
    # end def _setup_attribute
# end class Node


class DropBox(object):

    """Generic storage, allocation and retrieving class for any kind of data"""

    def __init__(self):
        """Initialize DropBox class object."""
    # end def __init__

    def __setattr__(self, attr, value):
        """Override set attribute to store dynamically created attributes."""
        self.__dict__[attr] = value
    # end def __setattr__

    def __getattr__(self, attr):
        """Override get attribute to store dynamically created attributes."""
        if attr not in self.__dict__.keys():
            raise ValueError('DropBox: please create attribute %s' % attr)
        # end if attr not existt
        return self.__dict__[attr]
    # end def __setattr__
# end class DropBox
