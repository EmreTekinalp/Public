"""
Created on 2014/01/16
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: The data model for the node editor; sub-classed from
        QtGui.QStandardItemModel
"""
from PySide import QtCore, QtGui
import nodeitem
reload(nodeitem)


class NodeItemModel(QtGui.QStandardItemModel):
    """
    item table:
    | name | value |
    ----------------
    |      |       |

    """
    def __init__(self, nodedatamanager):
        super(NodeItemModel, self).__init__()
        self.nodedatamanager = nodedatamanager
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['name', 'value'])
        self.views = list()
        self.itemChanged.connect(self.data_changed)
    # end def __init__

    def add_view(self, view):
        """@todo: insert doc for add_view"""
        self.views.append(view)
    # end def add_view

    def remove_view(self, view):
        """@todo: insert doc for add_view"""
        self.views.remove(view)
    # end def remove_view

    def data_changed(self, item):
        """@todo: insert doc for data_changed"""
        for view in self.views:
            view.update()
        # end for view in self.views
        if item.mayachange:
            self.nodedatamanager.attribute_changed(0, model=self, item=item)
    # end def data_changed

    def find_values(self, attr):
        """@todo: insert doc for find_value"""
        value_items = list()
        for item in self.findItems(attr, QtCore.Qt.MatchRecursive|QtCore.Qt.MatchExactly, column=0):
            parent = item.parent()
            if parent is not None:
                value_item = parent.child(item.row(), 1)
            else:
                value_item = self.item(item.row(), 1)
            value_items.append(value_item)
        # end for item in self.findItems(attr, QtCore.Qt.MatchRecursive|QtCore.Qt.MatchExactly, column=0)
        return value_items
    # end def find_values

    def find_attr(self, item):
        """@todo: insert doc for find_value"""
        parent = item.parent()
        if parent is not None:
            return parent.child(item.row(), 0)
        else:
            return self.item(item.row(), 0)
    # end def find_attr

    def name(self):
        """@todo: insert doc for name"""
        return self.find_values('name')[0].data(QtCore.Qt.DisplayRole)
    # end def name

    def side(self):
        """@todo: insert doc for side"""
        return self.find_values('side')[0].data(QtCore.Qt.DisplayRole)
    # end def side

    def module(self):
        """@todo: insert doc for module"""
        components = self.findItems('components', column=0)[0]
        return components.child(0, 0).data(QtCore.Qt.UserRole).model.name()
    # end def module

    def moduletype(self):
        """@todo: insert doc for moduletype"""
        return self.find_values('moduletype')[0].data(QtCore.Qt.DisplayRole)
    # end def moduletype

    def description(self):
        """@todo: insert doc for description"""
        return self.find_values('description')[0].data(QtCore.Qt.DisplayRole)
    # end def description

    def components(self):
        """@todo: insert doc for components"""
        return self.findItems('components')[0]
    # end def components

# end class NodeItemModel
