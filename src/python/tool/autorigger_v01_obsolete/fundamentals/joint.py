'''
Created on 28.08.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: The base joint class
'''

from maya import cmds


class Joint(object):
    """
    This is the base joint class, which will be used to create 
    everything dealing with joints
    """

    def __init__(self, 
                  side = None, 
                  name = None, 
                  suffix = None, 
                  position = [0.0, 0.0, 0.0], 
                  orientation = [0.0, 0.0, 0.0], 
                  parent = True, 
                  radius = 1,
                  skinTag = True):
        ########################################################################
        #vars
        self.name        = list()
        self.position    = list()
        self.orientation = list()
    
        #methods
        self.__create(side = side, 
                      name = name, 
                      suffix = suffix, 
                      position = position, 
                      orientation = orientation,
                      parent = parent, 
                      radius = radius,
                      skinTag = skinTag)
    #END def __init__()

    def __check_joint_name(self, 
                             side = None, 
                             name = None, 
                             suffix = None):
        #--- this method checks the name for the joint      
        if side == None:
            if name == None:
                if suffix == None:
                    self.name = 'joint'
                else:
                    self.name = 'joint_' + suffix 
            else:
                if suffix == None:
                    self.name = name
                else:
                    self.name = name + '_' + suffix
        else:
            if name == None:
                if suffix == None:
                    self.name = side + '_joint'
                else:
                    self.name = side + '_joint_' + suffix 
            else:
                if suffix == None:
                    self.name = side + '_' + name + '_JNT'
                else:
                    self.name = side + '_' + name + '_' + suffix 

        if name == None:
            if side == None:
                if suffix == None:
                    self.name = 'joint'
                else:
                    self.name = 'joint_' + suffix 
            else:
                if suffix == None:
                    self.name = side + '_joint'
                else:
                    self.name = side + '_joint_' + suffix
        else:
            if side == None:
                if suffix == None:
                    self.name = name
                else:
                    self.name = name + '_' + suffix 
            else:
                if suffix == None:
                    self.name = side + '_' + name + '_JNT'
                else:
                    self.name = side + '_' + name + '_' + suffix 
    #END def __check_joint_name()

    def __create_joint(self, 
                         position = [0.0, 0.0, 0.0], 
                         orientation = [0.0, 0.0, 0.0], 
                         parent = True, 
                         radius = 1):
        #--- this method creates a joint
        jnt = None     
        if parent == True:
            sel = cmds.ls(selection = True)
            if not sel:
                jnt = cmds.joint(name = self.name, 
                                 position = position, 
                                 orientation = orientation, 
                                 radius = radius)           
            else:
                if not cmds.nodeType(sel[0]) == 'joint':
                    jnt = cmds.joint(name = self.name, 
                                     position = position, 
                                     orientation = orientation, 
                                     radius = radius)           
                    cmds.setAttr(jnt + '.t', 0,0,0)
                    cmds.setAttr(jnt + '.r', 0,0,0)
                    cmds.setAttr(jnt + '.s', 1,1,1)
                else:
                    jnt = cmds.joint(name = self.name, 
                                     position = position, 
                                     orientation = orientation, 
                                     radius = radius)
                    if "|" in jnt:
                        self.name = jnt.split("|")[-1]
                    else:
                        self.name = jnt
        else:
            jnt = cmds.joint(name = self.name, 
                             position = position,
                             orientation = orientation, 
                             radius = radius)
            self.name = jnt
            cmds.select(clear = 1)
        return self.name
    #END def __create_joint()

    def __add_skin_tag(self, joints = None, skinTag = False):
        #--- this method adds a skin tag to the joint
        if joints:
            if isinstance(joints, list):
                for jnt in joints:
                    cmds.addAttr(jnt, 
                                 longName='SKIN', 
                                 shortName='SKIN', 
                                 attributeType = 'bool')
                    if skinTag:
                        cmds.setAttr(jnt + '.SKIN', 1)
                    else:
                        cmds.setAttr(jnt + '.SKIN', 0)
            else:
                cmds.addAttr(joints, 
                             longName='SKIN', 
                             shortName='SKIN', 
                             attributeType = 'bool')
                if skinTag:
                    cmds.setAttr(joints + '.SKIN', 1)
                else:
                    cmds.setAttr(joints + '.SKIN', 0)
    #END def __add_skin_tag()

    def __create(self, 
                  side = None, 
                  name = None, 
                  suffix = None, 
                  position = [0.0, 0.0, 0.0], 
                  orientation = [0.0, 0.0, 0.0], 
                  parent = True, 
                  radius = 1,
                  skinTag = False):
        #--- this is the main create method
        #--- check the joint name
        self.__check_joint_name(side = side, 
                                name = name, 
                                suffix = suffix)
        #--- create a joint
        self.__create_joint(position = position, 
                            orientation = orientation, 
                            parent = parent, 
                            radius = radius)
        #--- add skin tag
        self.__add_skin_tag(joints = self.name, skinTag = skinTag)
    #END def __create()
#END class Joint()