'''
Created on 09.10.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: The control class for the AutoRigger
'''

import os
from maya import cmds
from functions import data
from fundamentals import attribute, node, parents
reload(attribute)
reload(data)
reload(node)
reload(parents)


class Control(object):
    """
    This class creates the control shapes, which will be used for the rig
    """

    def __init__(self, 
                  side = None, 
                  name = None, 
                  suffix = 'CTL', 
                  size = 1, 
                  shape = 0, 
                  color = 6, 
                  position = [0,0,0],
                  rotation = [0,0,0],
                  offset = [0,0,0],                  
                  orientation = [0,0,0], 
                  rotateOrder = 3, 
                  parent = None,
                  lockAttrs = None):
        ########################################################################

        #args
        self.side = side
        self.name = name
        self.suffix = suffix
        self.size = size
        self.ctl_shape = shape
        self.color = color
        self.position = position
        self.rotation = rotation
        self.offset = offset
        self.orientation = orientation
        self.rotateOrder = rotateOrder
        self.parent = parent
        self.lockAttrs = lockAttrs

        #vars
        self.group     = None
        self.transform = None
        self.shape     = None

        #methods      
        self.__create()
    #end def __init__()

    def __control_setup(self):
        #--- this method setups the control
        attr = attribute.Attribute()
        nd = node.Node()
        #--- create control shape and set it up properly, store it in a dict
        ctl_name = self.side + '_' + self.name + '_' + self.suffix
        grp_name = self.side + '_' + self.name + '_GRP'

        #--- get the path to the shapes
#        root = os.path.dirname(os.path.dirname(__file__))
#        path = os.listdir(os.path.join(root, 'data', 'shapes'))
#        for i in path:
#            if ('shape' + str(self.ctl_shape) + '_') in i:
#                asset = i.split('.')[0]

        #--- load the data
#        d = data.Data()
#        shape_data = d.load(dirName = 'shapes', 
#                            assetName = asset, 
#                            dataType = 'shape')

        #--- create the curve shape
        ctl = nd.eLocator(name = ctl_name,
                          shape = self.ctl_shape,
                          size = self.size, 
                          color = self.color,
                          offset = self.offset)

#        ctl = cmds.curve(degree = 1, point = shape_data, name = ctl_name)
#        shp = cmds.rename(cmds.listRelatives(ctl, allDescendents = True), 
#                          ctl_name + 'Shape')

        #--- setup the size
#        cvs = cmds.ls(ctl + '.cv[*]', flatten = 1)
#        cmds.xform(cvs, relative = True, scale = [self.size, self.size, self.size])

        #--- setup a parent functionality for the control offset group
        grp = nd.transform(name = grp_name)
        parents.Parents(child = ctl['transform'], parent = grp)
        if self.parent:
            parents.Parents(child = grp, parent = self.parent)

        #--- create global variabes including transform, group and shape
        self.group     = grp
        self.transform = ctl['transform']
        self.shape     = ctl['shape']

        #--- translate and rotate the guide control group
        attr.setAttr(node = self.group, 
                     attribute = 't', 
                     value = self.position)
        attr.setAttr(node = self.group, 
                     attribute = 'r', 
                     value = self.rotation)

        #--- rotate the shape
#        cmds.setAttr(self.shape +'.orientation')
#        cmds.xform(cvs, relative = True, rotation = self.orientation)

        #--- offset the shape
#        cmds.xform(cvs, relative = True, translation = self.offset)        

        #--- set the rotateOrder of the control
        attr.setAttr(node = self.transform, 
                     attribute = 'rotateOrder', value = self.rotateOrder)
    #end def __control_setup()

    def __set_color(self):
        #--- this method defines the color of the control shape
        attr = attribute.Attribute()
        #--- set the color for the control
        attr.setColor(node = self.shape, color = self.color)
    #end def _set_color()

    def __lock_attributes(self):
        #--- this method locks all given attributes on the control
        attr = attribute.Attribute()
        #--- lock the specified attributes
        if self.lockAttrs:
            if isinstance(self.lockAttrs, list):
                for i in self.lockAttrs:
                    attr.lockAttr(node = self.transform, 
                                  attribute = i, 
                                  lock = True, 
                                  show = False)
            else:
                attr.lockAttr(node = self.transform, 
                              attribute = self.lockAttrs, 
                              lock = True, 
                              show = False)
    #end def __lock_attributes()

    def __create(self):
        ########################################################################
        #--- setup the control
        self.__control_setup()
        #--- set the color
#        self.__set_color()
        #--- lock attributes on the control
        self.__lock_attributes()
    #end def __create()
#end class Control()
