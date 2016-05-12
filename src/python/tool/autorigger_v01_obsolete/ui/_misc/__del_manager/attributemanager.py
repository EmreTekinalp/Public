"""
Created on 17.09.2013
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: The Manager for the attributes.
"""

from functools import partial
from PySide import QtCore, QtGui
from maya import cmds
import utility
from utility import namingconvention
reload(namingconvention)


class AttributeManager():
    """
    @todo: improve custom nodes
    @todo: rebuild maya's channel box behaviour:
    DONE * only show last selected in the channelbox
    DONE * set model of a fixed tree view -> way faster
    * way to deal with node groups -> give node grp as sub element
    * try to combine model approach with custom added QStandardModelItems
    * convert named entries in node and nodegroup to object links on creation
    """
    def __init__(self, autorigger=None):
        self.ar = autorigger
        self.nc = utility.namingconvention.NamingConvention()
        self.ar.graphics_view.scene().selectionChanged.connect(self.display_attributes)
    # end def __init__

    def display_attributes(self):
        """Iterates over all selected items and displays their attributes in
        the attribute manager.

        """
        nodeitems = self.ar.graphics_view.scene().get_selected_node_items()
        attrtree = self.ar.attributes_right_treeview
        grptree = self.ar.nodegroup_right_treeview
        if len(nodeitems) == 0:
            empty_model = QtGui.QStandardItemModel()
            attrtree.setModel(empty_model)
            grptree.setModel(empty_model)
        else:
            attrtree.setModel(nodeitems[0].data)
            grptree.setModel(nodeitems[0].nodegroup)
            for i in range(2, 6):
                attrtree.hideColumn(i)
                grptree.hideColumn(i)
            # end for i in range(2, 6)
    # end def def display_attributes


    def change_event(self, sender_type, sender):
        """
        @todo: disconnect event propagation before change to avoid double changes
        1. if sender is navigator:
            * get positions
            * transfer to datamodel
            * transfer to maya
        2. if sender is datamodel:
            * get value
            * transfer to navigator
            * transfer to maya
        3. if sender is maya:
            * get positions
            * transfer to navigator
            * transfer to datamodel
        """
        if sender_type == 'navigator':
            x = sender.pos().x()
            y = sender.pos().y()

            try:
                sender.data.itemChanged.disconnect()
                sender.data.set_attr('tx', x)
                sender.data.set_attr('ty', y)
                sender.data.itemChanged.connect(partial(self.change_event, 'datamodel'))
            except:
                sender.data.itemChanged.connect(partial(self.change_event, 'datamodel'))

            #self.change_mayaattr(sender, 'tx', x)
            #self.change_mayaattr(sender, 'ty', y)

        # sender is datamodel
        if sender_type == 'datamodel':
            attr = sender.parent().child(sender.row(), 0)
            if attr is None:
                return
            attr = attr.data(QtCore.Qt.DisplayRole)
            value = sender.data(QtCore.Qt.DisplayRole)
            sender.model().itemChanged.disconnect()
            if attr == 'tx' or attr == 'ty' or attr == 'tz':
                for node in sender.model().nodes:
                    if attr == 'tx':
                        node.setX(value)
                    elif attr == 'ty':
                        node.setY(value)
                    elif attr == 'tz':
                        node.setZValue(value)
            sender.model().itemChanged.connect(partial(self.change_event, 'datamodel'))
        # sender is maya

    # end def change_event








    def change_mayaattr(self, nodeitem, attr, value=None):
        """Changes the corresponding maya attr if any corresponding maya object
        exists.
        @todo: get rid of all the specialties and exceptions, especially tx, ty, tz

        """
        maya_object = self.get_corresponding_maya_object(nodeitem)
        if cmds.objExists(maya_object):
            obj_attr = '%s.%s' % (maya_object, attr)
            # if attr.name=='name' or attr.name=='side' or attr.name=='objtype':
            #    self.rename(nodeitem, attr, value, maya_object)
            if cmds.objExists(obj_attr):
                cmds.setAttr(obj_attr, value)
    # end def change_mayaattr

    def get_corresponding_maya_object(self, nodeitem):
        """Checks if the node corresponds to a maya object and if so, returns
        this corresponding object.

        """
        name = nodeitem.data.get_attr('name').data(QtCore.Qt.DisplayRole)
        objtype = nodeitem.data.get_attr('objtype').data(QtCore.Qt.DisplayRole)
        if objtype == 'group':
            return ''
        side = nodeitem.data.get_attr('side').data(QtCore.Qt.DisplayRole)
        maya_object = self.create_name(side, name, objtype)
        return maya_object
    # end def get_corresponding_maya_object











##################### REWORK THESE #############################################


    def rename(self, nodeitem, attr, value, maya_object):
        """Takes care of renaming the given maya object."""
        side = nodeitem.get_attr('side')
        name = name = nodeitem.get_attr('name')
        objtype = nodeitem.get_attr('objtype')
        if attr.name=='name':
            name = value
        if attr.name=='side':
            side = value
        if attr.name=='objtype':
            objtype = value
        new_name = self.create_name(side, name, objtype)
        print new_name
        cmds.rename(maya_object, new_name)
    # end def rename

    def create_name(self, side, name, objtype):
        """Creates and returns the object name from the given information."""
        exec 'side = self.nc.%s' % side
        exec 'objtype = self.nc.%s' % objtype
        return '%s%s%s%s%s' % (side, self.nc.split, name, self.nc.split, objtype)
    # end def create_name

    def change_qtattr(self, nodeitem, attr):
        """Changes the qt attribute """
        if attr.qtwidget is None:
            return
        if attr.attrtype == 'floatattr':
            attr.qtwidget.spinbox.setValue(attr.value)
    # end def change_qtattr
# end class AttributeManager
