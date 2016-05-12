"""
Created on 11.21.2013
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: The data model for the nodes.
"""

from PySide import QtCore, QtGui
from utility import datareader


class NodeDataModel(QtGui.QStandardItemModel):
    """@todo: use invisible top item"""
    def __init__(self, datatype, data=None):
        super(NodeDataModel, self).__init__()
        self.nodes = list()
        self.init_columns()
        self.create_default_attrs(datatype)
        if data is not None:
            self.create_from_json(data, self)
    # end def __init__

    def init_columns(self):
        """Initializes the columns."""
        self.columns = dict()
        labels = ['name', 'value', 'editable', 'attrtype', 'visible', 'mattr']
        self.setHorizontalHeaderLabels(labels)
        self.set_default_values()
        for i, label in enumerate(labels):
            self.columns[label] = i
        # end for i, label in enumerate(labels)
    # end def init_columns

    def set_default_values(self):
        """Sets the default values for the columns."""
        self.default_value = dict()
        self.default_value['name'] = 'name not set'
        self.default_value['value'] = ''
        self.default_value['attrtype'] = 'strattr'
        self.default_value['editable'] = True
        self.default_value['visible'] = True
        self.default_value['mattr'] = ''
    # end def set_default_values

    def setChild(self, row, column, item):
        """"""
        self.setItem(row, column, item)
    # end def setChild

    def child(self, row, column):
        """"""
        return self.item(row, column)
    # end def child

    def create_default_attrs(self, datatype):
        """Sets the default attributes for this model.
        @todo: Check second appearance of this in another
               place somewhere in PB ???

        """
        dreader = datareader.DataReader()
        default_data = dreader.parse_json('modules', datatype)
        self.create_from_json(default_data, self)
    # end def create_default_attrs

    def create_from_json(self, data, parent):
        """Sets all the attrs in the given data object onto this object."""
        for key, values in data.iteritems():
            exists = self.check_attr_existance(key, parent)
            if not exists:
                row = self.add_attr(key, parent)
            else:
                row = parent.findItems(key, column=self.columns['name'])[0].row()
            if isinstance(values, dict):
                if 'value' in values:
                    for prop, value in values.iteritems():
                        self.set_attr(key, value, parent, prop=prop)
                else:
                    self.create_from_json(values, parent.child(row, self.columns['name']))
            elif isinstance(values, list) or isinstance(values, tuple):
                valuedict = {'%s%s' % (key, i): v for i, v in enumerate(values)}
                self.create_from_json(valuedict, parent.child(row, self.columns['name']))
            else:
                valueitem = NodeDataItem()
                valueitem.set_data(values)
                parent.setChild(row, self.columns['value'], valueitem)
        # end for key, values in data.iteritems()
    # end def create_from_json

    def check_attr_existance(self, text, parent):
        """Returns the row."""
        indices = parent.findItems(text, column=self.columns['name'])
        if len(indices) == 0:
            return False
        else:
            return True
    # end def check_attr_existance

    def add_attr(self, attr, parent):
        """Sets the given attribute to the given value."""
        row = parent.rowCount()
        for label, column in self.columns.items():
            item = NodeDataItem()
            item.set_data(self.default_value[label])
            parent.setChild(row, column, item)
        # end for label, column in self.columns.items()
        nameitem = NodeDataItem()
        nameitem.setText(attr)
        nameitem.set_data(attr)
        nameitem.setEditable(False)
        parent.setChild(row, self.columns['name'], nameitem)
        return row
    # end def add_attr

    def set_attr(self, key, value, parent=None, prop='value'):
        """Sets the given attribute to the given value."""
        item = self.get_attr(key, parent)
        if item is None:
            return
        valueitem = item.parent().child(item.row(), self.columns[prop])
        valueitem.set_data(value)
    # end def set_attr

    def get_attr(self, attr, parent=None, column='value'):
        """Returns the value of the given attribute"""
        attritem = None
        if parent is None:
            parent = self
        for i in range(parent.rowCount()):
            item = parent.child(i, self.columns['name'])
            if item is None:
                continue
            name = item.text()
            if name == attr:
                return parent.child(i, self.columns[column])
            if item.rowCount() > 0:
                data = self.get_attr(attr, item, column)
                if data is not None:
                    return data
        # end for i in range(parent.rowCount())
        return attritem
    # end def get_attr
# end class NodeDataModel


class NodeDataItem(QtGui.QStandardItem):
    """docstring for NodeDataModelItem"""
    def __init__(self):
        super(NodeDataItem, self).__init__()
        self.datadict = dict()
    # end def __init__

    def findItems(self, text, role=QtCore.Qt.DisplayRole, flags=None, column=None):
        """"""
        items = list()
        for r in range(self.rowCount()):
            if column is None:
                start = 0
                end = self.columnCount()
            else:
                start = column
                end = column+1
            for c in range(start, end):
                item = self.child(r, c)
                itemdata = item.data(role)
                if itemdata == text:
                    items.append(item)
        return items
    # end def findItems

    def type(self):
        """"""
        return QtGui.QStandardItem().type() + 1
    # end def type

    def set_data(self, data):
        """"""
        self.setData(data)
        self.setData(data, QtCore.Qt.DisplayRole)
        self.setData(data, QtCore.Qt.EditRole)
        self.setData(data, QtCore.Qt.UserRole)
    # end def set_data

    def setData(self, data, role=QtCore.Qt.UserRole):
        """"""
        self.datadict[role.__int__()] = data
        if role.__int__() == QtCore.Qt.DisplayRole.__int__():
            self.datadict[QtCore.Qt.EditRole.__int__()] = data
        if role.__int__() == QtCore.Qt.EditRole.__int__():
            self.datadict[QtCore.Qt.DisplayRole.__int__()] = data
        self.emitDataChanged()
    # end def setData

    def data(self, role=QtCore.Qt.UserRole):
        """"""
        if role.__int__() in self.datadict.keys():
            return self.datadict[role.__int__()]
    # end data
# end NodeDataItem
