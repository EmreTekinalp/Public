"""Created on 2014/01/19
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: Constructs various types of RigModules

"""
from PySide import QtCore, QtGui
import collections

from mods import arm

import nodeitemmodel
reload(nodeitemmodel)

import nodeitem
reload(nodeitem)

from utility import datareader
reload(datareader)

from widget import rignode
reload(rignode)

from widget import compoundnode
reload(compoundnode)

import enum
reload(enum)


class RigModuleFactory():
    """@todo: insert doc for RigModuleFactory"""
    def __init__(self, parent=None):
        self.parent = parent
        self.attributedefaults = datareader.attributedefaults()
    # end def __init__

    def create_rigmodule(self, module, custom_data=None):
        """@todo: really should work on the names: data, moduletype etc., it's a mess!!!
        @todo: create all components, if any

        """
        nodes = list()
        data = self.create_final_data_dict(module, custom_data)
        main_node = self.create_component(module)
        nodes.append(main_node)
        for k, v in data['components']['data'].iteritems():
            node = self.create_component(v['data']['moduletype']['data'], custom_data=v['data'])
            self.add_component(main_node.model, node)
            self.add_component(node.model, main_node)
            self.parent.nodedatamanager.set_maya_name(node.model)
            nodes[0].add_inner_node(node)
            nodes.append(node)
        # end for k, v in data['components']['data'].iteritems()
        self.create_guides(main_node)
        return nodes
        #     # insert inhook and outhooks
        #     for comp_node in comp_nodes:
        #         # find respective inhook node
        #         inhook = self.find_node_by_attr('name', comp_nodes, comp_node.model.find_values('inhook')[0].data(QtCore.Qt.DisplayRole))
        #         # check for inhook
        #         if inhook is not None:
        #             item = comp_node.model.find_values('inhook')[0]
        #             row = item.row()
        #             parent = item.parent()
        #             new_item = nodeitem.NodeItem()
        #             new_item.setData(inhook.model.name(), QtCore.Qt.DisplayRole, True)
        #             new_item.setData(inhook, QtCore.Qt.UserRole)
        #             parent.takeChild(row, 1)
        #             parent.setChild(row, 1, new_item)

        #         # outhooks = comp_node.model.find_values('outhooks')[0].data(QtCore.Qt.UserRole)
        #         # item = comp_node.model.find_values('outhooks')[0]
        #         # row = item.row()
        #         # parent = item.parent()
        #         # parent.takeChild(row, 1)
        #         # for outhook in outhooks:
        #         #     self.init_row(comp_node.model, outhook, outhook, parent.child(row, 0))
        #             # outhook = self.find_node_by_attr('name', comp_nodes, comp_node.model.find_values('outhook')[0].data(QtCore.Qt.DisplayRole))

        #             #for outhook in comp_node.model.find_values('outhook')[0]:

        #             # end for outhook in comp_node.model.find_values('outhook')[0]
        #     # end for comp_node in comp_nodes
        #     # add the compound nodes to the nodes list
            # nodes += comp_nodes

        # self.create_guides(moduletype)
        # return nodes
    # end def create_rigmodule

    def create_component(self, module, custom_data=None):
        """@todo: insert doc for init_component"""
        data = self.create_final_data_dict(module, custom_data)
        model = self.create_model(data)
        return self.create_node(model)
    # end def init_component

    def add_component(self, model, node):
        """@todo: insert doc for add_component"""
        parent_item = model.components()
        item = nodeitem.NodeItem()
        item.setData(node.model.name(), QtCore.Qt.DisplayRole)
        item.setData(node, QtCore.Qt.UserRole)
        parent_item.appendRow(item)
    # end def add_component

    def create_guides(self, node):
        """@todo: insert doc for create_guides"""
        construct_str = 'arm.BipedArmGuide('
        attrs = list()
        model = node.model
        attributes = model.findItems('attributes')[0]
        for row in range(attributes.rowCount()):
            attr = attributes.child(row, 0).data(QtCore.Qt.DisplayRole)
            dataitem = attributes.child(row, 1)
            if not dataitem.guide:
                continue
            data = dataitem.data(QtCore.Qt.DisplayRole)
            if isinstance(data, unicode):
                data = '"%s"' % data
            attrs.append('%s=%s' % (attr, data))
        # end for row in node.model.rowCount()
        construct_str += str(attrs).strip('[]').replace('u\'', '').replace('\'', '')
        construct_str += ')'
        eval(construct_str)
    # end def create_guides

    def find_node_by_attr(self, attr, nodes, name):
        """@todo: insert doc for find_node_by_attr"""
        matched_node = None
        for node in nodes:
            if name == node.model.find_values(attr)[0].data(QtCore.Qt.DisplayRole):
                matched_node = node
        return matched_node
    # end def find_node_by_attr

    def create_final_data_dict(self, module, custom_data=None):
        """@todo: insert doc for create_final_data_dict"""
        mod = datareader.module(module)
        mod_parent = datareader.module(mod['moduletype']['data'])
        defaults = datareader.moduledefaults()
        step1 = self.m_dicts(defaults, mod_parent)
        step2 = self.m_dicts(step1, mod)
        if custom_data is not None:
            return self.m_dicts(step2, custom_data)
        else:
            return step2
    # end def create_final_data_dict

    def m_dicts(self, d1, d2):
        for k, v in d1.iteritems():
            # check if key is in d2
            if k in d2.keys():
                if isinstance(v, collections.OrderedDict):
                    d1[k] = self.m_dicts(v, d2[k])
                # if value is not a dict, override the value of d1 with the value from d2
                else:
                    d1[k] = d2[k]
        for k, v in d2.iteritems():
            # check if key is in d1, if not, add it
            if k not in d1.keys():
                d1[k] =v
        return d1
    # end def m_dicts

    def create_model(self, data):
        """Creates the data model for this module.
        @todo: provide model cross linking, so that when a joint is created with
               a model, the joint gets the model inserted in his components row

        """
        model = nodeitemmodel.NodeItemModel(self.parent.nodedatamanager)
        root = model.invisibleRootItem()
        for attr, value in data.iteritems():
            # components will be initialized separately later
            if attr == 'components':
                self.init_row(model, attr, None, root)
            else:
                self.init_row(model, attr, value, root)
        # end for attr, value in data.iteritems()
        return model
    # end def create_model

    def init_row(self, model, attr, data, parent):
        """Creates NodeItems for the given attr and data and appends them as a
        new row to the given parent NodeItem.
        parent
            |-> |attr|data|
        @param attr: The attribute's name, will be inserted in the first column
        @param data: The data, will be inserted in the second column
        @return: The attr and data NodeItems
        @todo: deal with colors

        """
        # set the attr item just as a string
        attr_item = nodeitem.NodeItem()
        attr_item.setData(attr, QtCore.Qt.DisplayRole)
        attr_item.setData(attr, QtCore.Qt.UserRole)
        data_item = self.init_data_item(data)
        if data is None:
            pass
        elif isinstance(data['data'], collections.OrderedDict):
            for k, v in data['data'].iteritems():
                self.init_row(model, k, v, attr_item)
            # end for k, v in data['data'].iteritems()
        else:
            exclusive = False
            display_data = data['data']
            user_data = data['data']
            # check if the attribute can be found in the attributedefaults
            if attr in self.attributedefaults:
                # enum attributes with predefined options
                if self.attributedefaults[attr][0] == 'enum':
                    user_data = enum.Enum(self.attributedefaults[attr][1])
                    user_data.set_current(display_data)
                    exclusive = True
            elif isinstance(display_data, list):
                exclusive = True
                display_data = str(display_data)
            elif isinstance(display_data, nodeitemmodel.NodeItemModel):
                exclusive = True
                display_data = attr
            elif (isinstance(display_data, rignode.RigNode) or
                  isinstance(display_data, compoundnode.CompoundNode)):
                exclusive = True
                display_data = attr
            data_item.setData(display_data, QtCore.Qt.DisplayRole, exclusive)
            data_item.setData(user_data, QtCore.Qt.UserRole)
        parent.appendRow([attr_item, data_item])
        return attr_item, data_item
    # end def init_row

    def init_data_item(self, data):
        """Initializes a data item by setting the available attributes for that
        data item.
        Possible attributes are:
        * visible
        * editable
        * min
        * max
        @param data: the data with the attributes for that item
        @return: the data item

        """
        construct_str = 'nodeitem.NodeItem('
        attrs = list()
        if data is not None:
            for attr, value in data.iteritems():
                if attr != 'data':
                    attrs.append('%s=%s' % (attr, value))
        construct_str += str(attrs).strip('[]').replace('u\'', '').replace('\'', '')
        construct_str += ')'
        return eval(construct_str)
    # end def init_data_item

    def create_node(self, model):
        """@todo: insert doc for create_node"""
        moduletype = model.find_values('moduletype')[0].data()
        if moduletype == 'compound':
            node = compoundnode.CompoundNode(model)
        if moduletype == 'joint':
            node = rignode.RigNode(model)
            node.setX(model.find_values('tx')[0].data(QtCore.Qt.DisplayRole)*10)
            node.setY(model.find_values('ty')[0].data(QtCore.Qt.DisplayRole)*(-10))
        return node
    # end def create_node
# end class RigModuleFactory
