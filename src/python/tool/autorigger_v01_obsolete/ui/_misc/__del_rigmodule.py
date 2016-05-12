"""Created on 2014/01/15
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: Holds the data for the construction of a module.
"""

from PySide import QtCore

import nodeitemmodel
reload(nodeitemmodel)

import nodeitem
reload(nodeitem)

from utility import datareader
reload(datareader)


class RigModule():
    """Holds the data for the construction of a module in all it's forms, be it
    a simple button or a graphic node representation for this module.
    @todo: generalize more -> remove all occurances of named attributes

    """
    def __init__(self, data):
        self.instances = list()
        self.data = data
        self.attributedefaults = datareader.attributedefaults()
        self.model = self.create_model()
    # end def __init__

    def create_model(self):
        """Creates the data model for this module.
        @todo: provide model cross linking, so that when a joint is created with
               a model, the joint gets the model inserted in his components row

        """
        model = nodeitemmodel.NodeItemModel()
        self.init_top_level(model)
        self.init_attributes(model)
        self.init_components(model)
        return model
    # end def create_model

    def init_top_level(self, model):
        """Initializes the top level items of the RigModule."""
        root = model.invisibleRootItem()
        for attr, value in self.data.iteritems():
            if isinstance(value, list) or isinstance(value, dict):
                continue
            self.init_row(model, attr, value, root)
        # end for attr, value in self.data.iteritems()
    # end def init_top_level

    def init_attributes(self, model):
        """Fills the attribute section in the model of this module."""
        root, empty = self.init_row(model, 'attributes', '', model.invisibleRootItem())
        for attr, value in self.data['attributes'].iteritems():
            self.init_row(model, attr, value, root)
        # end for attr, value in self.data['attributes'].iteritems()
    # end def init_attributes

    def init_components(self, model):
        """Initializes the components section of the model."""
        root, empty = self.init_row(model, 'components', None, model.invisibleRootItem())
    # end def init_components

    def add_component(self, component, model):
        """components
        component1 | shoulder
        component2 | elbow
        component3 | wrist

        # how displayed, maybe like this:

        [tab label: components]
        shoulder | joint | [select button]
        elbow | joint | [select button]

        on select:
            1. select component in the view
            2. switch to attributes tab

        """
        root = model.findItems('components', column=0)[0]
        component_name = component.model.find_values('name')[0].data(QtCore.Qt.DisplayRole)
        component_type = component.model.find_values('moduletype')[0].data(QtCore.Qt.DisplayRole)
        self.init_row(model, component_name, 'select button here', root)
    # end def add_component

    def init_row(self, model, attr, value, parent):
        """Creates NodeItems for the given attr and value and appends them as a
        new row to the given parent NodeItem.
        parent
            |-> |attr|value|
        @param attr: The attribute's name, will be inserted in the first column
        @param value: The value, will be inserted in the second column
        @return: The attr and value NodeItems
        @todo: deal with colors

        """
        # set the attr item just as a string
        attr_item = nodeitem.NodeItem()
        attr_item.setData(attr, QtCore.Qt.DisplayRole)
        attr_item.setData(attr, QtCore.Qt.UserRole)
        value_item = nodeitem.NodeItem()
        # init the value data
        exclusive = False
        display_value = value
        user_value = value
        # check if the attribute can be found in the attributedefaults
        if attr in self.attributedefaults:
            if self.attributedefaults[attr][0] == 'enum':
                user_value = self.attributedefaults[attr][1]
                exclusive = True
        # take care of list type values
        if isinstance(value, list):
            exclusive = True
            display_value = value[0]
        # finally set the value data
        value_item.setData(display_value, QtCore.Qt.DisplayRole, exclusive)
        value_item.setData(user_value, QtCore.Qt.UserRole)
        parent.appendRow([attr_item, value_item])
        return attr_item, value_item
    # end def init_row
# end class RigModule
