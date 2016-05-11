'''
Created on 02.11.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: The skeleton class of the AutoRigger
'''

from maya import cmds
from fundamentals import attribute, node
reload(attribute)
reload(node)


class Skeleton(object):
    """
    In this class you create the skeleton
    """

    def __init__(self,
                  character = None):
        ########################################################################
        #args
        self.character    = character

        #vars
        self.skel_grp     = None
        self.characters   = list()
        self.guide_mods   = list()
        self.guide_joints = list()

        self.joints = list()

        #methods
        self.__create(character = character)
    #END def __init__()

    def __create_skeleton_setup(self):
        #--- this method creates the skeleton group
        nd = node.Node()
        if cmds.objExists('SKELETON'):
            self.skel_grp = 'SKELETON'
        else:
            #--- create the group
            self.skel_grp = nd.transform(name = 'SKELETON')
    #END def __create_skeleton_setup()

    def __get_guide_mods(self):
        #--- this method locates and stores the existing mods
        if cmds.objExists('GUIDES'):
            #--- get the character/children of the GUIDES group
            chars = cmds.listRelatives('GUIDES', 
                                       children = True, 
                                       type = 'transform')[0]
            if chars == self.character:
                if cmds.listRelatives(chars, 
                                      allDescendents = True, 
                                      type = 'joint'):
                    self.characters.append(chars)
                mods = cmds.listRelatives(chars, 
                                          children = True, 
                                          type = 'transform')
                if mods:
                    self.guide_mods.append(mods)
    #END def __get_guide_mods()

    def __get_guide_joints(self):
        #--- this method locates and stores the guide joints
        for char in self.guide_mods:
            for mod in char:
                mod_name = mod.split('_GMOD')[0]
                gjnt = cmds.ls('*' + mod_name + '*GJNT', type = 'joint')
                if gjnt:
                    self.guide_joints.append(gjnt)        
    #END def __get_guide_joints()

    def __setup_guide_joints(self):
        #--- this method setups the guide joints properly
        attr = attribute.Attribute()
        #--- unlock all locked attributes of the guide joints
        for gjnt in self.guide_joints:
            attr.lockAttr(node = gjnt,
                          attribute = ['t', 'r', 's', 'v'], 
                          lock = False, show = True)
            #--- unparent the guide joints to the world
            cmds.parent(gjnt, world = True)
            #--- parent the guide joints to the character group
            cmds.parent(gjnt, self.characters[0])
        #--- delete the guides
        for mod in self.guide_mods:
            if mod:
                cmds.delete(mod)
            #--- parent the character to the skeleton group
            cmds.parent(self.characters, self.skel_grp)
            #--- delete the guides group
            cmds.delete('GUIDES')
        #--- unlock visibility of guide joints
        for gjnt in self.guide_joints:
            for jnt in gjnt:
                cmds.setAttr(jnt + '.v', 1)
    #END def __setup_guide_joints()

    def __parent_guide_joints(self):
        #--- this method parents the guide joints together
        attr = attribute.Attribute()
        non_central = []
        #--- get the message infos of each joint
        for gjnt in self.guide_joints:
            for jnt in gjnt:
                if cmds.objExists(jnt + '.connection'):
                    cnt = cmds.listConnections(jnt + '.connection')
                    if cnt:
                        #--- unparent the jnt to the world
                        cmds.parent(jnt, world = True)
                        #--- parent the child joints by message infos
                        cmds.parent(jnt, cnt[0])
                        #--- filter all the joints which need to be mirrored
                        if cnt[0][0] == 'C':
                            if not jnt[0] == 'C':
                                non_central.append(jnt)
                    else:
                        #--- filter all the left joints which need to be mirrored
                        if not jnt[0] == 'C':
                            non_central.append(jnt)      
    #END def __parent_guide_joints()

    def __rename_guide_joints(self):
        #--- this method renames the proper information of the guide joints
        attr = attribute.Attribute()
        sel = cmds.ls('*_GJNT', type = 'joint')
        #--- change the suffix of the hidden attributes to JNT
        for i in sel:
            if cmds.objExists(i + '.suffix'):
                attr.lockAttr(node = i, 
                              attribute = ['suffix'], 
                              lock = False)
                attr.setAttr(node = i, 
                             attribute = 'suffix', 
                             value = 'JNT', 
                             lock = True)
            #--- rename the suffix of the guide joints
            rnm = cmds.rename(i, i.split('GJNT')[0] + 'JNT')
            self.joints.append(rnm)
        cmds.select(clear = True)
        print 'Skeleton created!'        
    #END def __rename_guide_joints()

    def __create(self,
                  character = None):
        #--- the main creation method of the class
        #--- create skeleton setup
        self.__create_skeleton_setup()
        #--- get the guide mods
        self.__get_guide_mods()
        #--- get the guide joints
        self.__get_guide_joints()
        #--- setup guide joints
        self.__setup_guide_joints()
        #--- parent the guide joints
        self.__parent_guide_joints()
        #--- rename the guide joints
        self.__rename_guide_joints()
    #END def __create()
#END class Skeleton()
