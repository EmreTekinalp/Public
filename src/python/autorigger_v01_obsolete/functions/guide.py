'''
Created on 08.10.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: The guide class of the AutoRigger
'''

import re
from maya import cmds
from functions import control
from fundamentals import attribute, joint, node
reload(attribute)
reload(control)
reload(joint)
reload(node)


class Guide(object):
    """
    In this class you create the guides
    """

    def __init__(self,
                  character = None,
                  mod = None, 
                  side = None, 
                  name = None, 
                  suffix = 'GCTL',
                  size = 1, 
                  shape = 0,
                  orientation = [0,0,0],
                  color = 0, 
                  position = [0,0,0],
                  rotation = [0,0,0],
                  upVectorOffset = [0,6,0], 
                  aimVector = [1,0,0], 
                  upVector = [0,1,0],
                  rotateOrder = 3,
                  flip = False,
                  mirrorGuideObj = None):
        ########################################################################        
        #args
        self.character      = character
        self.mod            = mod
        self.side           = side
        self.name           = name
        self.suffix         = suffix
        self.size           = size
        self.shape          = shape
        self.orientation    = orientation 
        self.color          = color
        self.position       = position
        self.rotation       = rotation
        self.upVectorOffset = upVectorOffset
        self.aimVector      = aimVector
        self.upVector       = upVector
        self.rotateOrder    = rotateOrder
        self.flip           = flip
        self.mirrorGuideObj = mirrorGuideObj

        #vars
        self.main_mod    = [] 
        self.side_mod    = []
        self.right_mod   = []     
        self.extras      = []

        self.ctl         = []
        self.g_ctl       = []
        self.g_grp       = []
        self.g_jnt       = []
        self.g_jnt_off   = []
        self.g_loc       = []

        self.crv         = []

        #methods
        self.__create()
    #END def __init__()

    def __iterate_mod(self, 
                        mod = None):
        #--- in this method you check and iterate the mod
        #--- list all main GMOD groups
        sel = cmds.ls(mod + '*' + '_GMOD')
        iter = 1
        #--- check existence otherwise set mod iterator to 1
        if sel:
            for obj in sel:
                if cmds.objExists(obj):
                    #--- get the integer number and check if there is one
                    new = obj.split(mod)[1].split('_GMOD')[0]
                    if not new == '':
                        #--- iterate the existing one by +1
                        if new.isdigit:
                            #--- list the children to check which side is inside
                            side_child = cmds.listRelatives(obj, children = True)
                            for child in side_child:
                                if not '_GTMP' in child:
                                    if not child == self.side + '_' + mod + str(iter) + '_GMOD':
                                        self.mod = mod + str(iter)
                                    else:
                                        iter = int(new) + 1
                            self.mod = mod + str(iter)
                    else:
                        self.mod = mod + str(1)
                else:
                    self.mod = mod + str(1)                    
        else:
            self.mod = mod + str(1)
    #END def __iterate_mod()

    def __setup_mod(self):
        #--- in this method you create the mod setup hierarchy
        nd = node.Node()
        attr = attribute.Attribute()

        #--- check and create the constant guides group
        if cmds.objExists('GUIDES'):
            self.guide_grp = 'GUIDES'
        else:
            self.guide_grp = nd.transform(name = 'GUIDES', suffix = None)

        #--- check character name for whitespaces
        if '' in self.character:
            character = self.character.replace(' ', '_')

        #--- check and create the dynamic character group
        if self.character:
            if cmds.objExists(self.character):
                self.char_grp = self.character
            else:
                self.char_grp = nd.transform(name = self.character,
                                             parent = self.guide_grp)
        else:
            if cmds.objExists('CHARACTER'):
                self.char_grp = 'CHARACTER'
            else:
                self.char_grp = nd.transform(name = 'CHARACTER',
                                             parent = self.guide_grp)

        #--- check if mod hierarchy exists, otherwise create it properly
        if self.mod:
            if cmds.objExists(self.mod + '_GMOD'):
                self.main_mod = self.mod + '_GMOD'
                if cmds.objExists(self.mod + '_GTMP'):
                    self.extras = self.mod + '_GTMP'
                else:
                    self.extras = nd.transform(name = self.mod, 
                                               suffix = 'GTMP', 
                                               parent = self.main_mod)
                if cmds.objExists(self.side + '_' + self.mod + '_' + 'GMOD'):
                    self.side_mod = self.side + '_' + self.mod + '_' + 'GMOD'
                else:
                    self.side_mod = nd.transform(name = self.side + '_' + self.mod, 
                                                 suffix = 'GMOD', 
                                                 parent = self.main_mod)
            else:
                self.main_mod = nd.transform(name = self.mod, 
                                             suffix = 'GMOD',
                                             parent = self.char_grp)
                self.side_mod = nd.transform(name = self.side + '_' + self.mod, 
                                             suffix = 'GMOD', 
                                             parent = self.main_mod)
                self.extras = nd.transform(name = self.mod, 
                                           suffix = 'GTMP', 
                                           parent = self.main_mod)                
        else:
            if cmds.objExists('MOD_GMOD'):
                self.main_mod = self.side + '_MOD_GMOD'
                if cmds.objExists(self.side + '_MOD_GMOD'):
                    self.side_mod = self.side + '_MOD_GMOD'
                else:
                    self.side_mod = nd.transform(name = self.side + '_MOD', 
                                                 suffix = 'GMOD',
                                                 parent = self.main_mod)
            else:
                self.main_mod = nd.transform(name = 'MOD', 
                                             suffix = 'GMOD',
                                             parent = self.char_grp)
                self.side_mod = nd.transform(name = self.side + '_MOD', 
                                             suffix = 'GMOD',
                                             parent = self.main_mod)
    #END def __setup_mod()

    def __add_mod_attributes(self):
        #--- this method adds attributes to the main mod
        attr = attribute.Attribute()
        #--- showJoints
        if not cmds.objExists(self.main_mod + '.showJoints'):
            attr.addAttr(node = self.main_mod, 
                         attrName = 'showJoints', 
                         attrType = 'short', 
                         min = 0, 
                         max = 1, 
                         default = 0, 
                         keyable = False, 
                         channelBox = True)
        #--- showUpVectors
        if not cmds.objExists(self.main_mod + '.showUpVectors'):
            attr.addAttr(node = self.main_mod, 
                         attrName = 'showUpVectors', 
                         attrType = 'short', 
                         min = 0, 
                         max = 1, 
                         default = 0, 
                         keyable = False, 
                         channelBox = True)
        #--- showLabels
        if not cmds.objExists(self.main_mod + '.showLabels'):
            attr.addAttr(node = self.main_mod, 
                         attrName = 'showLabels', 
                         attrType = 'short', 
                         min = 0, 
                         max = 1, 
                         default = 0, 
                         keyable = False, 
                         channelBox = True)
    #END def __add_mod_attributes()

    def __create_control(self, 
                           name = None,
                           position = [0,0,0]):
        #--- in this method you create the guide control
        self.ctl = control.Control(side = self.side, 
                                   name = name, 
                                   suffix = self.suffix, 
                                   size = self.size, 
                                   shape = self.shape,
                                   orientation = self.orientation,
                                   color = self.color, 
                                   position = position,
                                   rotation = self.rotation,
                                   parent = self.side_mod,
                                   rotateOrder = self.rotateOrder)
        self.g_ctl.append(self.ctl.transform)
        self.g_grp.append(self.ctl.group)
    #END def __create_control()

    def __setup_control(self, 
                          name = None):
        #--- in this method you create the joint and upVector setup and reposition
        attr = attribute.Attribute()
        nd = node.Node()
        #--- create joint
        jnt = None        
        jnt_grp = nd.transform(name = self.side + '_' + name, 
                               suffix = 'GOFF', 
                               parent = self.ctl.transform)
        if self.flip:
            if self.upVectorOffset[0]:
                jnt = joint.Joint(side = self.side, 
                                  name = name, 
                                  suffix = 'GJNT', 
                                  radius = self.size * 0.9,
                                  orientation = [0,180,0])
            elif self.upVectorOffset[1]:
                jnt = joint.Joint(side = self.side, 
                                  name = name, 
                                  suffix = 'GJNT', 
                                  radius = self.size * 0.9,
                                  orientation = [0,0,180])
            elif self.upVectorOffset[2]:
                jnt = joint.Joint(side = self.side, 
                                  name = name, 
                                  suffix = 'GJNT', 
                                  radius = self.size * 0.9,
                                  orientation = [180,0,0])
        else:
            jnt = joint.Joint(side = self.side, 
                              name = name, 
                              suffix = 'GJNT', 
                              radius = self.size * 0.9)

        #--- zero out the joints position
        attr.setAttr(node = jnt.name, attribute = 't', value = [0,0,0])

        #--- setup and connect the joint labels
        if self.side == 'L' or self.side == 'l' or self.side == 'Left' or self.side == 'left':
            cmds.setAttr(jnt.name + '.side', 1)
        elif self.side == 'R' or self.side == 'r' or self.side == 'Right' or self.side == 'right':
            cmds.setAttr(jnt.name + '.side', 2)
        elif self.side == 'C' or self.side == 'c' or self.side == 'Center' or self.side == 'center':
            cmds.setAttr(jnt.name + '.side', 0)
        cmds.setAttr(jnt.name + '.type', 18)
        cmds.setAttr(jnt.name + '.otherType', 
                     name[0].upper() + name[1:], 
                     type = 'string')
        cmds.connectAttr(self.main_mod + '.showLabels', jnt.name + '.drawLabel')

        #--- set the displayType of the joints
        attr.setColor(node = jnt.name, displayType = 0)

        #--- upVector setup
        up_vector = nd.locator(name = self.side + '_' + name, 
                               suffix = 'GLOC',
                               parent = self.ctl.transform)

        #--- offset the position of the locator
        attr.setAttr(node = up_vector, 
                     attribute = 't', 
                     value = self.upVectorOffset)

        #--- set the color of the upVector locators
        attr.setColor(node = up_vector, color = self.color)

        #--- store the nodes properly
        self.g_jnt.append(jnt.name)
        self.g_jnt_off.append(jnt_grp)
        self.g_loc.append(up_vector)
    #END def __setup_control()

    def __setup_aim(self):
        #--- setup the aimConstraints for the joints
        nd = node.Node()
        #--- iterate through the joint groups
        for i in range(len(self.g_jnt_off)):
            if not len(self.g_jnt_off) > 1:
                #--- setup for all joints except the last one
                aim = nd.aimConstraint(target = self.g_loc[i], 
                                       source = self.g_jnt_off[i], 
                                       suffix = 'AIM',
                                       aimVector = self.aimVector,
                                       upVector = self.upVector,
                                       worldUpObject = self.g_loc[i], 
                                       worldUpType = 'object')                
            else:
                j = i + 1
                if not j == len(self.g_jnt_off):
                    #--- setup for all joints except the last one
                    aim = nd.aimConstraint(target = self.g_jnt[j], 
                                           source = self.g_jnt_off[i], 
                                           suffix = 'AIM', 
                                           aimVector = self.aimVector,
                                           upVector = self.upVector,
                                           worldUpObject = self.g_loc[i], 
                                           worldUpType = 'object')
                else:
                    #--- setup for the last joint
                    if self.aimVector[0] == 1:
                        self.aimVector = [-1,0,0]
                    elif self.aimVector[1] == 1:
                        self.aimVector = [0,-1,0]
                    elif self.aimVector[2] == 1:
                        self.aimVector = [0,0,-1]
                    aim = nd.aimConstraint(target = self.g_jnt_off[i-1], 
                                           source = self.g_jnt_off[i], 
                                           suffix = 'AIM', 
                                           aimVector = self.aimVector,
                                           upVector = self.upVector,
                                           worldUpObject = self.g_loc[i], 
                                           worldUpType = 'object')
    #END def __setup_aim()

    def __create_connection_curve(self,
                                     obj = None,
                                     parent = None):
        #--- this method creates the curves whicht connects the guides
        attr = attribute.Attribute()
        nd   = node.Node()
        #--- create the curve 
        crv = cmds.curve(degree = 1, point = self.position)
        cmds.parent(crv, self.extras)
        crvShp = cmds.listRelatives(crv, allDescendents = True)[0]
        crvShp = cmds.rename(crvShp, crv + 'Shape')
        rel = cmds.listRelatives(crv, allDescendents = 1)[0]
        #--- connect the cvs to the controls by matrix
        for i in range(len(obj)):
            #--- create decomposeMatrix nodes
            dcm = nd.decomposeMatrix(name = obj[i])
            #--- connect the control with the decomposeMatrix
            attr.connectAttr(node = [obj[i], dcm], 
                             attribute = ['worldMatrix[0]', 'inputMatrix'])
            attr.connectAttr(node = [dcm, rel], 
                             attribute = ['outputTranslate', 
                                          'controlPoints[' + `i` + ']'])

            #--- create the visibility connections of the main mod node
            if cmds.nodeType(obj[i]) == 'joint':
                attr.connectAttr(node = [self.main_mod, obj[i]], 
                                 attribute = ['showJoints', 'v'])
                attr.connectAttr(node = [self.main_mod, self.g_loc[i]], 
                                 attribute = ['showUpVectors', 'v'])
        #--- set the displayType of the curve Shape to template
        attr.setColor(node = crvShp, displayType = 1)
    #END def __create_connection_curve()

    def __create_guides(self):
        #--- in this method you can create multiple or single guides
        if self.mirrorGuideObj:
            self.position = self.mirrorGuideObj.position
            self.name = self.mirrorGuideObj.name
        #--- multiple guides setup
        if isinstance(self.name, list):
            if isinstance(self.position[0], list):
                for obj, pos in zip(self.name, self.position):
                    obj = obj[0].upper() + obj[1:]
                    #--- create the control (position is a list)
                    self.__create_control(name = self.mod + obj, position = pos)
                    #--- setup the control (position is a list)
                    self.__setup_control(name = self.mod + obj)
                #--- create the connection curves (position is a list)
                self.__create_connection_curve(obj = self.g_jnt,
                                               parent = self.side_mod)
                #--- setup aimVector (position is a list)
                self.__setup_aim()
            else:
                for obj, pos in zip(self.name, self.position):
                    obj = obj[0].upper() + obj[1:]                   
                    #--- create the control (position is not a list)
                    self.__create_control(name = self.mod + obj, position = pos)
                    #--- setup the control (position is not a list)                    
                    self.__setup_control(name = self.mod + obj)
                #--- create the connection curves (position is not a list                    
                self.__create_connection_curve(obj = self.g_jnt,
                                               parent = self.side_mod)
                #--- setup aimVector (position is not a list)
                self.__setup_aim()
        else:
            #--- single guide setup
            name = self.name[0].upper() + self.name[1:]
            #--- create the control
            self.__create_control(name = self.mod + name, position = self.position)
            #--- setup the control
            self.__setup_control(name = self.mod + name)
            #--- create the connection curve
            self.__create_connection_curve(obj = self.g_jnt, parent = self.side_mod)
            #--- setup aimVector (single guide)
            self.__setup_aim()
    #END def __create_guides()

    def __add_guide_info(self):
        #--- in this method you add proper information to the guides
        attr = attribute.Attribute()
        #--- add all necessary attributes as strings to ctl, mirror, jnt and mod
        attribute_list = ['char','mod','sides','name','suffix','size','shape',
                          'orientation','color','position','upVectorOffset', 
                          'aimVector','upVector','rotationOrder']
        method_list = [self.character,self.mod,self.side,self.name,self.suffix,
                       self.size,self.shape,self.orientation,self.color,
                       self.position,self.upVectorOffset,self.aimVector,
                       self.upVector,self.rotateOrder]
        for ctl in (self.g_jnt, self.g_ctl, self.main_mod):
            if ctl:
                for a in attribute_list:
                    if not isinstance(ctl, list):
                        #--- check if control, mod exists
                        if not cmds.objExists(ctl + '.' + a):
                            attr.addAttr(node = ctl, 
                                         attrName = a, 
                                         attrType = 'string')
                        if not cmds.objExists(ctl + '.' + a):
                            print 'no ctl ', ctl                  
                    else:
                        attr.addAttr(node = ctl, 
                                     attrName = a, 
                                     attrType = 'string')
                        for i in ctl:
                            if not cmds.objExists(i + '.' + a):
                                print 'no ', i                      

        #--- add a message attribute to the guide joints and the main mod
        if not cmds.objExists(self.main_mod + '.' + self.side + '_connection'):
            cmds.addAttr(self.main_mod, 
                         longName = self.side + '_connection', 
                         shortName = self.side + '_connection', 
                         attributeType = 'message')
        cmds.addAttr(self.g_jnt, 
                     longName = 'connection', 
                     shortName = 'connection', 
                     attributeType = 'message') 

        #--- set the content of the string attributes
        for ctl in (self.g_ctl, self.g_jnt):
            if ctl:
                for i in range(len(ctl)):
                    attr.setAttr(node = ctl[i], attribute = 'char', 
                                 value = self.character, lock = True)
                    attr.setAttr(node = ctl[i], attribute = 'mod', 
                                 value = self.mod, lock = True)
                    attr.setAttr(node = ctl[i], attribute = 'sides', 
                                 value = self.side, lock = True)
                    if isinstance(self.name, list):
                        attr.setAttr(node = ctl[i], attribute = 'name', 
                                     value = self.name[i], lock = True)
                    else:
                        attr.setAttr(node = ctl[i], attribute = 'name', 
                                     value = self.name, lock = True)
                    attr.setAttr(node = ctl[i], attribute = 'suffix', 
                                 value = self.suffix, lock = True)
                    attr.setAttr(node = ctl[i], attribute = 'size', 
                                 value = self.size, lock = True)
                    attr.setAttr(node = ctl[i], attribute = 'shape', 
                                 value = self.shape, lock = True)
                    attr.setAttr(node = ctl[i], attribute = 'orientation', 
                                 value = self.orientation, lock = True)                    
                    attr.setAttr(node = ctl[i], attribute = 'color', 
                                 value = self.color, lock = True)
                    attr.setAttr(node = ctl[i], attribute = 'position', 
                                 value = self.position[i], lock = True)
                    attr.setAttr(node = ctl[i], attribute = 'upVectorOffset', 
                                 value = self.upVectorOffset, lock = True)            
                    attr.setAttr(node = ctl[i], attribute = 'aimVector', 
                                 value = self.aimVector, lock = True)
                    attr.setAttr(node = ctl[i], attribute = 'upVector', 
                                 value = self.upVector, lock = True)
                    attr.setAttr(node = ctl[i], attribute = 'rotationOrder', 
                                 value = self.rotateOrder, lock = True)
        #--- set the specific attributes for the main mod
        for i in cmds.ls(self.main_mod):
            if i:
                for a in attribute_list:
                    if not cmds.getAttr(i + '.' + a, lock = True):
                        for a, m in zip(attribute_list, method_list):
                            attr.setAttr(node = i, attribute = a, 
                                         value = m, lock = True)
    #END def __add_guide_info

    def __mirror_guides(self):
        #--- this method mirrors the guides properly and set them up
        attr = attribute.Attribute()
        nd = node.Node()
        #--- create the mirror node and the proper connections
        guides = self.mirrorGuideObj
        mirrors = []
        if isinstance(guides.name, list):
            for obj in range(len(guides.name)):
                mirror = nd.mirrorSwitch(name = (self.side + '_' + self.mod + 
                                                 guides.name[obj][0].upper() + 
                                                 guides.name[obj][1:]))
                attr.connectAttr(node = [guides.gd.g_ctl[obj], mirror], 
                                 attribute = ['worldMatrix', 'inputMatrix'])
                for axis in 'xyz':
                    attr.lockAttr(node = [self.g_grp[obj]], 
                                  attribute = ['t', 'r'], lock = False, show = True)
                    #--- connect outPos and outRot with translate and rotate
                    attr.connectAttr(node = [mirror, self.g_grp[obj]], 
                                     attribute = ['op' + axis, 't' + axis])
                    attr.connectAttr(node = [mirror, self.g_grp[obj]], 
                                     attribute = ['or' + axis, 'r' + axis])
                cmds.setAttr(mirror + '.ihi', 0)
                mirrors.append(mirror)
        else:
            mirror = nd.mirrorSwitch(name = (self.side + '_' + self.mod + 
                                             guides.name[0].upper() + 
                                             guides.name[1:]))
            attr.connectAttr(node = [guides.gd.g_ctl[0], mirror], 
                             attribute = ['worldMatrix', 'inputMatrix'])
            for axis in 'xyz':
                attr.lockAttr(node = [self.g_grp[0]], 
                              attribute = ['t', 'r'], lock = False, show = True)
                #--- connect outPos and outRot with translate and rotate
                attr.connectAttr(node = [mirror, self.g_grp[0]], 
                                 attribute = ['op' + axis, 't' + axis])
                attr.connectAttr(node = [mirror, self.g_grp[0]], 
                                 attribute = ['or' + axis, 'r' + axis])
            cmds.setAttr(mirror + '.ihi', 0)
            mirrors.append(mirror)
        self.mirrors = mirrors
    #END def __mirror_guides()

    def __add_mirror_attributes(self):
        #--- this method adds mirror attributes to the main mod
        attr = attribute.Attribute()
        #--- mirror
        attr.addAttr(node = self.main_mod, 
                     attrName = 'mirror', 
                     attrType = 'short', 
                     min = 0, 
                     max = 1, 
                     default = 1, 
                     keyable = False, 
                     channelBox = True)
        #--- mirrorLock
        attr.addAttr(node = self.main_mod, 
                     attrName = 'mirrorLock', 
                     attrType = 'short', 
                     min = 0, 
                     max = 1, 
                     default = 1, 
                     keyable = False, 
                     channelBox = True)
        #--- mirrorAxis
        cmds.addAttr(self.main_mod, 
                     longName = 'mirrorAxis', 
                     attributeType = 'enum', 
                     enumName = 'yz:xz:xy',
                     keyable=True)
        cmds.setAttr(self.main_mod + '.mirrorAxis', edit=True, 
                     keyable=False, 
                     channelBox=True)
        #--- connect the mirror attributes properly with the main mod
        for i in self.mirrors:
            attr.connectAttr(node = [self.main_mod, i], 
                             attribute = ['mirror', 'mirror'])
            attr.connectAttr(node = [self.main_mod, i], 
                             attribute = ['mirrorAxis', 
                                          'mirrorAxis'])
        for i in self.g_ctl:
            attr.connectAttr(node = [self.main_mod, i + 'Shape'], 
                             attribute = ['mirrorLock', 
                                          'drawOverride.overrideDisplayType'])
    #END def __add_mirror_attributes()

    def __cleanup_setup(self):
        #--- this method hides and locks unnecessary nodes and attributes        
        attr = attribute.Attribute()
        attr.lockAll(node = [self.guide_grp, self.char_grp])
        attr.lockAll(node = self.g_jnt)
        attr.lockAll(node = self.g_jnt_off)
        attr.lockAll(node = self.g_loc)
        attr.lockAll(node = self.main_mod)
        attr.lockAll(node = self.extras)        
        attr.lockAttr(node = self.side_mod, 
                      attribute = ['t','r','s','v','ihi'], 
                      lock = True, 
                      show = False)
        for i in cmds.ls('*GCRV','*DCM', '*AIM', '*Shapes', '*MLT', 'curve*'):
            attr.lockAll(node = i)
    #END def __cleanup_setup()

    def __create(self):
        #--- get the iterator of the mod
        self.__iterate_mod(mod = self.mod)
        #--- setup mod
        self.__setup_mod()
        #--- add mod attributes
        self.__add_mod_attributes()
        #--- create the guides
        self.__create_guides()
        #--- add guide info
        self.__add_guide_info()
        #--- mirror the guides
        if self.mirrorGuideObj:
            #--- mirror mode on this node
            self.__mirror_guides()
            #--- add mirror attribute to the main mod
            self.__add_mirror_attributes()
        #--- cleanup the guides
        self.__cleanup_setup()
    #END def __create()
#END class Guide()