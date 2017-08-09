'''
Created on Aug 8, 2015

@author: Emre
'''

from maya import cmds
import pymel.core as pm
import logging
reload(logging)
logging.basicConfig(format='', level=logging.DEBUG)

# constants
MIN = 0
MAX = 1


class Prototype(object):

    """Based on node selection, generate a python code recreating this setup

    @DONE Get hidden locked attributes!
    @todo Generate code based on the data information
    @DONE Fix add attribute issue so that we don't have twice
    @todo Add keyable check for add dictionary
    @todo Find a object oriented way of allocating data instad of dictionary
    @todo Use a non binary tree class to store and access data of a pymel node
    """ 

    def __init__(self):
        """Class constructor"""
        self._data = dict()
        self._attributes = dict()
    # end def __init__

    def generate(self, mode=MIN):
        """Call function to generate the code based on selection"""
        selection = pm.ls(sl=True)
        if not selection:
            logging.debug('Prototype: Please select at least one node!')
            return
        # end if no selection
        for item in selection:
            ud = item.listAttr(ud=True)
            self._data[item] = dict()
            self._data[item]['add'] = self._get_attr_info(ud)
            self._data[item]['set'] = self._get_attributes(item, mode)
            self._data[item]['connect'] = self._get_connections(item)
            self._data[item]['lockhide'] = self._get_lock_hidden_state(item)
        # end for iterate selection
        self._convert_to_code()
    # end def generate

    def _get_attr_info(self, entry):
        """Return user defined attributes from given pynode object"""
        result = dict()
        for a in entry:
            result[a] = {'flagType': 'at', 'type': None, 'value': None,
                         'min': None, 'max': None, 'enums': None,
                         'keyable': True, 'channelbox': False}
            if a.isDynamic():
                if pm.addAttr(a.name(), q=True, at=True) == 'typed':
                    result[a]['flagType'] = 'dt'
                # end if datatype
            # end if attr is dynamic
            if a.type() == 'enum':
                result[a]['enums'] = a.getEnums()
            # end if enumtype
            result[a]['type'] = a.type()
            result[a]['value'] = a.get()
            result[a]['min'] = a.getMin()
            result[a]['max'] = a.getMax()
            result[a]['keyable'] = a.isKeyable()
            result[a]['channelbox'] = a.isInChannelBox()
        # end for iterate attributes
        return result
    # end def _get_attr_info

    def _get_attributes(self, item, mode):
        """Return attribute and value data from given pynode object"""
        omit = list()
        if not mode:
            omit = [item.caching, item.ihi, item.nodeState]
        # end if mode is zero
        attrs = [a for a in item.listAttr(s=True) if a not in omit]
        self._attributes = self._get_attr_info(attrs)
        return self._attributes
    # end def _get_attributes

    def _get_connections(self, item):
        """Return connections from given pynode object"""
        connections = list()
        for c in item.listConnections(c=True, s=False, scn=True, plugs=True):
            if cmds.getClassification(cmds.nodeType(c[-1].name()))[0]:
                connections.append(list(c))
            # end if get valid nodes
        # end for iterate connections
        return connections
    # end def _get_connections

    def _get_lock_hidden_state(self, item):
        """Return lock and keyable state from each attributes"""
        lock_n_hide = list()
        locked = False
        keyable = True

        for a in self._attributes.keys():
            if a.isLocked():
                locked = True
            # end if attr is locked
            if not a.isKeyable():
                keyable = False
            # end if attr is hidden
            lock_n_hide.append([a, locked, keyable])
        # end for iterate attributes
        return lock_n_hide
    # end def _get_lock_hidden_state

    def _convert_to_code(self):
        """Convert the data dictionary into an executing code snippet"""
        print self._create_function_code()
    # end def _convert_to_code

    def _create_function_code(self):
        """Return function code"""
        funcname = '\ndef create():'
        docstring = '"""Please replace this with useful information"""'
        createnode = ''
        addattr = ''
        connect = ''
        endanno = '# end def create'
        self.i = -1
        for key, value in self._data.items():
            self.i += 1
            createnode += self._create_node_code(key)
            addattr += self._add_attr_code(key, value)
            connect += self._connect_attr_code(value['connect'])
        # end for iterate dictionary
        result = [funcname, docstring]
        if createnode:
            result.append(createnode)
        # end if create node
        if addattr:
            result.append(addattr)
        # end if add attr
        if connect:
            result.append(connect)
        # end if connect attr
        result = '%s\n%s' % ('\n    '.join(result), endanno)
        return result
    # end def _create_node_code

    def _create_node_code(self, node):
        """Return a python maya create node command as strings"""
        if self.i == len(self._data.items()) - 1:
            return ''.join("cmds.createNode('%s', n='%s')\n" %
                           (node.type(), node))
        return ''.join("cmds.createNode('%s', n='%s')\n    " %
                       (node.type(), node))
        # end def _connect_attr_str

    def _add_attr_code(self, key, value):
        """Return a python maya add attr command as a string."""
        result = list()
        for k, v in value['add'].items():
            result += ["cmds.addAttr('%s'" % key.name()]
            result += [", ln='%s'" % k.lastPlugAttr(True)]
            result += [", %s='%s'" % (v['flagType'], v['type'])]
            result += [", dv=%s" % v['value']]
            if v['min'] is not None:
                result += [", min=%s" % v['min']]
            # end if min is not none
            if v['max'] is not None:
                result += [", max=%s" % v['max']]
            # end if max is not none
            result += [", k=%s" % v['keyable']]
            if v['enums']:
                result += [", enumName='%s'" % ':'.join(v['enums'].keys())]
            # end if enums exist
            result += [")\n    "]
        # end for iterate value dict
        if result:
            return ''.join(result)
        # end result
        return ''
    # end def _add_attr_string

    def _connect_attr_code(self, connections):
        """Return a python maya connectAttr command as strings"""
        result = list()
        for cnt in connections:
            result += ["cmds.connectAttr('%s', '%s')\n    " % (cnt[0], cnt[1])]
        # end for iterate connections
        if result:
            return ''.join(result)
        # end result
        return ''
    # end def _connect_attr_string

    def _set_attr_code(self, connections):
        """Return a python maya connectAttr command as strings"""
        result = list()
        for cnt in connections:
            result += ["cmds.connectAttr('%s', '%s')\n    " % (cnt[0], cnt[1])]
        # end for iterate connections
        return ''.join(result)
    # end def _connect_attr_string
# end class Prototype


pt = Prototype()
pt.generate()


def create():
    """Please replace this with useful information"""
    cmds.createNode('multDoubleLinear', n='multDoubleLinear1')
    cmds.createNode('multiplyDivide', n='multiplyDivide1')
    cmds.createNode('condition', n='condition1')
    
    cmds.addAttr('multiplyDivide1', ln='bla', at='double', dv=1.24, min=0.0, max=2.0, k=True)
    
    cmds.connectAttr('multDoubleLinear1.output', 'condition1.colorIfTrueR')
    cmds.connectAttr('multiplyDivide1.outputY', 'condition1.colorIfTrueG')
    cmds.connectAttr('multiplyDivide1.outputZ', 'condition1.colorIfTrueB')
    cmds.connectAttr('multiplyDivide1.outputX', 'condition1.secondTerm')
    cmds.connectAttr('multiplyDivide1.bla', 'condition1.firstTerm')
    # end def create
