"""
@package: utility.node
@brief: Base implementations of the node interfaces
@author: Emre Tekinalp
@contact: e.tekinalp@icloud.com
"""

import os
import sys
import json
import logging
import string
import pymel.core as pm
from maya import cmds
from utility import abbreviation
from tool.pandoras_box.core import base

reload(base)
reload(logging)
logging.basicConfig(format='', level=logging.DEBUG)


class Node(base.Base):

    """Dynamically create a maya node by calling the node as a class method.

    The user has access to the node's input parameters on top of all.
    Under resource/node.config the user can find all relevant maya node
    information. If this config file is missing, a fresh new config file
    will be automatically generated inside the resource package when calling
    this class. This class reads the information given in this config file.

    @return PyNode class object.
    @usage After instantiating the class, access each individual maya node by
           calling its name as a function, which has as parameters the node
           related input attributes.
    @example Here are different examples listed below:

    from utility.node import node

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

    # example 6 change side from default C to L
    node.side = 'L'
    rmv = node.remapValue('test')
    ==> output would be prefixed L instead of C

    @DONE: Check string object compatibility, otherwise extend class
    @DONE: Optimize class, use recursions and helper functions in code
    @DONE: Implement abbreviation algorithm for individual node suffix
    """

    def __init__(self):
        """Class constructor to initialize Node."""
        super(Node, self).__init__()

        # private method
        self._get_config_path()

        # private vars
        self.suffix = None

        self._nodes = self._get_nodes()
        self._abbs = dict()
        self._nodename = None
    # end def __init__

    def _get_config_path(self):
        """Return config file path."""
        self._path = os.path.join(self._get_top_path(__file__),
                                  'etc', 'node', 'node.config')
        self._abbr = os.path.join(self._get_top_path(__file__),
                                  'etc', 'node', 'node_abbreviations.config')
    # end def _get_config_path

    def _get_top_path(self, path):
        """Recursively return the top group path.

        @param path <string> Input path to start recursive search for top group
        """
        if os.path.split(path)[-1] == 'Maya':
            return path
        # end if we reach Maya
        return self._get_top_path(os.path.split(path)[0])
    # end def _get_top_path

    def _get_nodes(self):
        """Read and return node_info.json file otherwise create a new one."""
        if os.path.exists(self._path) and os.path.exists(self._abbr):
            with open(self._path) as json_file:
                json_data = json.load(json_file)
            # end with open json file
            return json_data
        # end if path exists
        return self._setup_data()
    # end def _get_nodes

    def _setup_data(self):
        """Check node classification, filter, save config file and return."""
        classlist = ['utility', 'shader', 'transform', 'drawdb', 'general']
        ignore = ['nexManip', 'xgmPatch']
        nodes = [n for n in pm.allNodeTypes() for c in classlist
                 if cmds.getClassification(n, satisfies=c) and
                 cmds.getClassification(n) if not n in ignore]
        nodes = list(set(nodes + [n for n in pm.allNodeTypes()
                                  if (n.startswith('n_') or
                                      n == 'pointOnCurveInfo' or
                                      n == 'pointOnSurfaceInfo' or
                                      n == 'pointMatrixMult')]))
        data = dict()
        self._get_data(nodes, data)
        self._abbs = self._add_abbreviation(data)
        self._save_config_file(data)
        return data
    # end def _setup_data

    def _get_data(self, nodes, data):
        """Recursive function to store data in a dictionary.

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
        """Implement the proper abbreviation and mutate the given dictionary.

        @param data <dict> A dictionary containing the relevant attribute data
        @note It is important to know that if there is no node.config file than
              we need to use the Abbreviation class which generates one.
        """
        abb = abbreviation.Abbreviation(['_'])
        abbreviations = dict()
        for key, value in abb.abbreviate(data).items():
            if key in data:
                data[key]['__ABBREVIATION__'] = value
                abbreviations[key] = value
            # end if key exists in data
        # end for iterate dictionary
        return abbreviations
    # end def _add_abbreviation

    def _save_config_file(self, data):
        """Save config file.

        @param data <dict> A dictionary containing the relevant attribute data
        """
        with open(self._path, 'w') as json_file:
            json.dump(data, json_file, sort_keys=True, indent=2)
        # end with save file
        with open(self._abbr, 'w') as json_file:
            json.dump(self._abbs, json_file, sort_keys=True, indent=2)
        # end with save file
    # end def _save_config_file

    def __getattr__(self, attr):
        """Override getattr function and return node.

        @param attr <str> Name of the node which generates a PyNode
        """
        def _node(*args, **kwargs):
            """Function closure to check, setup and return a PyNode"""
            if attr not in self._nodes:
                raise TypeError('Node is invalid: %s' % attr)
            # end if raise type error
            self._nodename = attr
            return self._setup_node(*args, **kwargs)
        # end def _node
        return _node
    # end def __getattr__

    def _setup_node(self, *args, **kwargs):
        """Setup and return the node.

        @param args <list> Storing args from config file as list
        @param kwargs <dict> Storing keyword args from config file as dict

        @DONE use logging instead of printing
        """
        node = None
        if not self.suffix:
            self.suffix = self._nodes[self._nodename]['__ABBREVIATION__']
        # end if not suffix given use abbreviation list
        firstarg = None
        if args:
            if not args[0] == None:
                firstarg = str(args[0])
            # end if firstarg is not None
        # end if args is given
        shapenodes = ['goe_locator', 'annotationShape', 'locator']
        transformnodes = ['group', 'offset']

        if firstarg:
            if firstarg == 'help':
                msg = "\nValid parameters for the %s node:" % self._nodename
                logging.debug(msg)
                for n in self._nodes[self._nodename].items():
                    if not n[0] == '__ABBREVIATION__':
                        logging.debug('-- %s : <%s>' % (n[0], n[1]))
                    # end if exclude abbreviation
                # end for print parameters and types
                return
            # end if help or set name
            name = '%s_%s%s%s' % (self.side, self.name,
                                  firstarg[0].upper(), firstarg[1:])
            if not self.master:
                name = '%s_%s' % (self.side, firstarg)
            # end if no parent given
            name = '%s%s_%s' % (name, self._get_index(name), self.suffix)
            if self._nodename in shapenodes:
                name = '%sShape' % name
            # end if special treatment
            if self._nodename in transformnodes:
                node = pm.createNode('transform', n=name)
            else:
                node = pm.createNode(self._nodename, n=name)
            # end if transformnodes specified
        else:
            if self.master:
                name = '%s_%s' % (self.side, self.master.name)
                name = '%s%s_%s' % (name, self._get_index(name), self.suffix)
                if self._nodename in shapenodes:
                    name = '%sShape' % name
                # end if special treatment
                if self._nodename in transformnodes:
                    node = pm.createNode('transform', n=name)
                else:
                    node = pm.createNode(self._nodename, n=name)
                # end if transformnodes specified
            else:
                if self._nodename in transformnodes:
                    node = pm.createNode('transform')
                else:
                    node = pm.createNode(self._nodename)
                # end if transformnodes specified
            # end if parent is given
        # end if args exists
        self._setup_attribute(node, **kwargs)
        self.suffix = None
        return node
    # end def _setup_node

    def _get_index(self, name=None, index='', count=0):
        """Recursively check duplicates in the scene and return index.
        @DONE fix index issue.
        """
        if not pm.objExists('%s%s_%s' % (name, index, self.suffix)):
            return index
        # end if name does not exists
        return self._get_index(name, count + 1, count + 1)
    # end def _get_index

    def _tag_node(self, node, nodetype):
        """Create a tag so we can better identify its nodetype.

        @param node <pyNode> PyNode object to set and get attributes
        @param nodetype <string> nodetype of the PyNode
        """
        if not pm.objExists('%s.NODETYPE' % node):
            node.addAttr('NODETYPE', dt='string')
            node.NODETYPE.set(nodetype, type='string', l=True)
        # end if create tag attribute
    # end def _tag_node

    def _setup_attribute(self, node, **kwargs):
        """Set or connect given output into input attributes.

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
            if self._nodes[self._nodename][key] == 'TdataCompound':
                for i, v in enumerate(val):
                    if pm.objExists(str(v)):
                        v.connect(node.attr('%s[%s]' % (key, i)))
                    # end for iterate dataCompound
                # end for iterate dataCompound
            # end if key is dataCompound
            if pm.objExists(str(val)):
                val.connect(node.attr(key))
            else:
                if self._nodes[self._nodename][key] == 'TdataCompound':
                    for i, v in enumerate(val):
                        if not node.attr('%s[%s]' % (key, i)).isConnected():
                            node.setAttr('%s[%s]' % (key, i), v)
                        # end if node is not connected
                    # end for iterate dataCompound
                else:
                    node.setAttr(key, val)
                # end if value is dataCompound
            # end if connect or set attribute
        # end for set attribute
    # end def _setup_attribute
# end class Node

node = Node()
