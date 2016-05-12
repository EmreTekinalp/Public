"""Created on 2014/01/24
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: Manages the

"""
from PySide import QtCore, QtGui
from maya import cmds
from utility import namingconvention
reload(namingconvention)


class NodeDataManager():
    """@todo: manage the different translation values between the ui and maya"""
    def __init__(self, parent=None):
        self.parent = parent
        self.nc = namingconvention.NamingConvention()
    # end def __init__

    def selection_changed(self, selected_items):
        """Changes the data in the attributes view and sets it to the last
        selected item or clears the table.

        """
        if len(selected_items) > 0:
            model = selected_items[-1].model
            # name
            self.parent.attributes_name.set_model(model, model.find_values('name')[0])
            # attributes
            self.parent.attributes_tableview.setModel(model)
            attributes_index = model.indexFromItem(model.findItems('attributes', column=0)[0])
            self.parent.attributes_tableview.setRootIndex(attributes_index)
            self.parent.attributes_tableview.resizeRowsToContents()
            self.parent.attributes_tableview.resizeColumnsToContents()
            # maya name
            self.parent.maya_name.set_model(model, model.find_values('maya_name')[0])
            # module name
            components = model.findItems('components', column=0)[0]
            c_model = components.child(0, 0).data(QtCore.Qt.UserRole).model
            self.parent.module_name.set_model(c_model, c_model.find_values('name')[0])
            # module
            self.parent.module_tableview.setModel(c_model)
            attr_index = c_model.indexFromItem(c_model.findItems('attributes', column=0)[0])
            self.parent.module_tableview.setRootIndex(attr_index)
            self.parent.module_tableview.resizeRowsToContents()
            self.parent.module_tableview.resizeColumnsToContents()
        else:
            empty_model = QtGui.QStandardItemModel()
            self.parent.attributes_tableview.setModel(empty_model)
            self.parent.components_tableview.setModel(empty_model)
            self.parent.module_tableview.setModel(empty_model)
            self.parent.attributes_name.unset_model()
            self.parent.maya_name.unset_model()
            self.parent.module_name.unset_model()
    # end def selection_changed

    def attribute_changed(self, src=-1, attr=None, value=None, model=None, item=None):
        """@param src: -1 - unknown, error
                        0 - model
                        1 - navigator
        @todo: insert doc for attribute_changed"""
        # 0: change originated from the model
        if src == 0:
            attr = model.find_attr(item).data(QtCore.Qt.DisplayRole)
            if attr == 'name' or attr == 'side':
                self.set_maya_name(model)
        # 1: change originated from the navigator
        elif src == 1:
            # 1. release event handler from model
            # 2. change the model
            value = value / 10
            if 'attr' == 'ty':
                value = value * (1)
            self.set_model_attr(model, attr, value)
            # 3. change maya
            maya_name = model.find_values('maya_name')[0].data(QtCore.Qt.DisplayRole)
            try:
                t = cmds.xform(maya_name, q=True, t=True, ws=True)
                if attr == 'tx':
                    t[0] = value
                if attr == 'ty':
                    t[1] = value*(-1)
                print t
                cmds.xform(maya_name, t=t, ws=True)
            except:
                pass
            # 4. re-establish event handler
    # end def attribute_changed

    def set_model_attr(self, model, attr, value):
        """@todo: insert doc for set_model_attr"""
        item = model.find_values(attr)[0]
        item.setData(value, QtCore.Qt.DisplayRole)
        item.setData(value, QtCore.Qt.UserRole)
    # end def set_model_attr

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

    # def rename(self, nodeitem, attr, value, maya_object):
    #     """Takes care of renaming the given maya object."""
    #     side = nodeitem.get_attr('side')
    #     name = name = nodeitem.get_attr('name')
    #     objtype = nodeitem.get_attr('objtype')
    #     if attr.name=='name':
    #         name = value
    #     if attr.name=='side':
    #         side = value
    #     if attr.name=='objtype':
    #         objtype = value
    #     new_name = self.create_name(side, name, objtype)
    #     print new_name
    #     cmds.rename(maya_object, new_name)
    # # end def rename

    def set_maya_name(self, model):
        """Creates and returns the object name from the given information."""
        name = model.name()
        side = model.side()
        module = model.module()
        objtype = 'GCTL'
        maya_name = '%s%s%s1%s%s%s' % (side, self.nc.split, module, name.capitalize(), self.nc.split, objtype)
        model.find_values('maya_name')[0].setData(maya_name, QtCore.Qt.DisplayRole)
    # end def set_maya_name
# end class NodeDataManager
