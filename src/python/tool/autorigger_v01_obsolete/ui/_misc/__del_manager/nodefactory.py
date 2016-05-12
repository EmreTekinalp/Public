"""
Created on 10/04/2013
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: The NodeFactory creates a node and sets it's inital data.
"""

from PySide import QtCore, QtGui
from ui.qtcustom import node, nodeconnection
from utility import datareader
from ui.model import nodedata, nodedatamodel
reload(nodedata)
reload(datareader)
reload(node)
reload(nodedatamodel)
reload(nodeconnection)


class NodeFactory():
    """The NodeFactory creates a node and sets it's initial data.
    @todo: Create nodeconnection
    @todo: rename methods from 'create_...' to just '...'

    """
    def __init__(self):
        self.dreader = datareader.DataReader()
    # end def __init__

    def create_module(self, module, autorigger):
        """"""
        module_data = self.dreader.parse_json('modules', module)
        nodegroup = self.create_nodegroup(module_data, self)
        jnodes = list()
        for jnt in module_data['joints']:
            jnode = self.create_rignode(jnt, nodegroup, autorigger)
            autorigger.graphics_view.scene().addItem(jnode)
            jnodes.append(jnode)
        # end for jnt in module_data['joints']
        self.hook_up_nodes(jnodes)
        return jnodes
    # end def create_module

    def create_nodegroup(self, data, autorigger):
        """Creates a standard node group."""
        riggroup = nodedatamodel.NodeDataModel('nodegroup', data)
        return riggroup
    # end def create_nodegroup

    def create_rignode(self, data, nodegroup, autorigger):
        """Creates a standard rig node.
        @todo: Rename to jointnode

        """
        datamodel = nodedatamodel.NodeDataModel('joint', data)
        rignode = node.RigNode(datamodel, autorigger, nodegroup=nodegroup)
        return rignode
    # end def create_rignode

    def create_mousenode(self, autorigger, x, y):
        """Creates a node at the current mouse position. This node will
        automatically be removed on a mouse release event.

        """
        dreader = datareader.DataReader()
        dreader.parse_json('modules', 'mousenode')
        datamodel = nodedatamodel.NodeDataModel('mousenode')
        tx = x-datamodel.get_attr('size').data(QtCore.Qt.DisplayRole)/2
        ty = y-datamodel.get_attr('size').data(QtCore.Qt.DisplayRole)/2
        datamodel.set_attr('tx', tx)
        datamodel.set_attr('ty', ty)
        mousenode = node.MouseNode(datamodel, autorigger)
        mousenode.setPos(tx, ty)
        return mousenode
    # end def create_rignode

    def hook_up_nodes(self, nodes):
        """Hooks up the given nodes with one another."""
        for hook in ['inhook', 'outhook']:
            for node in nodes:
                hookattr = node.data.get_attr(hook, column='name')
                for row in range(hookattr.rowCount()):
                    hook_item = node.data.get_attr('%s%s' % (hook, row))
                    hook_name = hook_item.data(QtCore.Qt.DisplayRole)
                    for checknode in nodes:
                        checknode_name = checknode.data.get_attr('name').data(QtCore.Qt.DisplayRole)
                        if checknode_name in hook_name:
                            node.remove_hook(hook, checknode_name)
                            node.add_hook(checknode, hook)
                            if hook == 'outhook':
                                node.add_connection(checknode, True)
                    # end for checknode in nodes
                # end for row in range(hookattr.rowCount())
            # end for node in nodes
        # end for hook in ['inhook', 'outhook']
    # end def hook_up_nodes
# end class NodeFactory
