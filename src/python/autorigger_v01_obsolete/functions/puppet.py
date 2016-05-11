'''
Created on 05.11.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: The master of puppets class of the AutoRigger
'''

from maya import cmds
from fundamentals import attribute, node
from functions import guide, control
reload(attribute)
reload(control)
reload(guide)
reload(node)


class Puppet(object):
    """
    In this class you create the main puppet setup
    """

    def __init__(self, 
                  character = None, 
                  guideObj  = None):
        ########################################################################
        #args
        self.character = character
        self.guideObj  = guideObj

        #vars
        self.char_grp        = None
        self.rig_grp         = None
        self.main_mod_grp    = None
        self.main_ctl        = None

        self.side_mod_grp    = None
        self.side_jnt_grp    = None
        self.side_ctl_grp    = None
        self.side_extra_grp  = None

        self.joints          = []
        self.joint_position  = []

        self.side            = None
        self.mod             = None
        self.name            = None
        self.color           = guideObj.color
        self.size            = guideObj.size

        #methods
        self.__create()
    #END def __init__()

    def __create_puppet_setup(self):
        #--- this method creates the group setup properly
        nd = node.Node()
        #--- create the character group
        if self.character:
            if cmds.objExists('CHARACTER_' + self.character):
                self.char_grp = 'CHARACTER_' + self.character
            else:
                self.char_grp = nd.transform(name = 'CHARACTER_' + self.character)
            #--- get the skeleton group and parent it with the joints properly
            if cmds.objExists(self.character):
                child = cmds.listRelatives(self.character, children = True)
                cmds.parent(child, 'SKELETON')
                cmds.delete(self.character)
                cmds.parent('SKELETON', self.char_grp)
                cmds.select(clear = True)
            #--- create the RIG group
            if cmds.objExists('RIG'):
                self.rig_grp = 'RIG'
            else:
                self.rig_grp = nd.transform(name = 'RIG', parent = self.char_grp)                
        else:
            raise Exception('You have to specify a proper character name!')
    #END def __create_puppet_setup()

    def __create_main_control(self):
        #--- this method creates the main control
        nd = node.Node()
        #--- create main control
        if not cmds.objExists('C_' + self.character + 'Main_CTL'):
            main_ctl = control.Control(side = 'C', 
                                       name = self.character + 'Main', 
                                       suffix = 'CTL', 
                                       size = 5, 
                                       shape = 11, 
                                       color = 17,
                                       parent = self.rig_grp)
            self.main_ctl = main_ctl.transform
        else:
            self.main_ctl = 'C_' + self.character + 'Main_CTL'
    #END def __create_main_control

    def __setup_main_control(self):
        #--- this method setups the main control
        if not cmds.objExists(self.main_ctl + '.globalScale'):
            attr = attribute.Attribute()
            attr.addAttr(node= self.main_ctl, 
                         attrName = 'globalScale', 
                         attrType = 'double', 
                         min = 0, 
                         default = 1)
            #--- connect the scale attributes of the main control with the gs
            for axis in 'xyz':
                attr.connectAttr(node = [self.main_ctl, self.main_ctl], 
                                 attribute = ['globalScale', 's' + axis])
            #--- limit the scale minimum to 0.01
            cmds.transformLimits(self.main_ctl, 
                                 scaleX = (0.01,1),
                                 scaleY = (0.01,1),
                                 scaleZ = (0.01,1),
                                 enableScaleX = (1,0),
                                 enableScaleY = (1,0),
                                 enableScaleZ = (1,0))
            #--- lock the scale attributes of the main control
            attr.lockAttr(node = self.main_ctl, 
                          attribute = ['s'])
        if not cmds.objExists(self.main_ctl + '.displayType'):
            attr = attribute.Attribute()
            attr.addAttr(node= self.main_ctl, 
                         attrName = 'displayType',
                         attrType = 'enum', 
                         enum = ['normal', 'template', 'reference'])
            #--- connect the meshes
            for i in cmds.ls(type='mesh'):
                if cmds.objExists(i):
                    attr.setAttr(node=i, attribute=['overrideEnabled'], value=1, lock=True)
                    attr.connectAttr(node=[self.main_ctl, i], 
                                     attribute=['displayType',
                                               'drawOverride.overrideDisplayType'])
            attr.setAttr(node=self.main_ctl, attribute=['displayType'], value=2)
    #END def__setup_main_control

    def __create_modular_setup(self):
        #--- this method creates the modular based group setup
        nd = node.Node()
        iter = 1
        for child in cmds.listRelatives(self.main_ctl, children = True):
            if cmds.ls(child, type = 'transform'):
                for i in cmds.listRelatives(child, children = True):
                    n = self.guideObj.side + '_' + self.guideObj.mod + str(iter)
                    if n in i:
                        iter += 1
        iter = str(iter)
        #--- create the main module group
        if cmds.objExists('MAIN_' + self.guideObj.mod + '_MOD'):
            self.main_mod_grp = 'MAIN_' + self.guideObj.mod + '_MOD'
        else:
            self.main_mod_grp = nd.transform(name = 'MAIN_' + 
                                             self.guideObj.mod,
                                             suffix = 'MOD', 
                                             parent = self.main_ctl)
        #--- create the side module group
        sides = [self.guideObj.gd.side]
        for side in sides:
            if cmds.objExists(side + '_' + self.guideObj.mod + iter + '_MOD'):
                self.side_mod_grp = side + '_' + self.guideObj.mod + iter + '_MOD'
            else:
                self.side_mod_grp = nd.transform(name = (side + '_' + 
                                                         self.guideObj.mod + iter),
                                                 suffix = 'MOD', 
                                                 parent = self.main_mod_grp)
            #--- create the joint group for the side
            if cmds.objExists(side + '_' + self.guideObj.mod + iter + '_JOINTS'):
                self.side_jnt_grp = (side + '_' + self.guideObj.mod + iter + '_JOINTS')
            else:
                self.side_jnt_grp = nd.transform(name = (side + '_' + 
                                                         self.guideObj.mod + iter),
                                                 suffix = 'JOINTS',
                                                 parent = self.side_mod_grp)
            #--- create the control group for the side
            if cmds.objExists(side + '_' + self.guideObj.mod + iter + '_CONTROLS'):
                self.side_ctl_grp = (side + '_' + self.guideObj.mod + iter + '_CONTROLS')
            else:
                self.side_ctl_grp = nd.transform(name = (side + '_' + 
                                                         self.guideObj.mod + iter),
                                                 suffix = 'CONTROLS',
                                                 parent = self.side_mod_grp)
            #--- create the extraNodes group for the side
            if cmds.objExists(side + '_' + self.guideObj.mod + iter + '_EXTRANODES'):
                self.side_extra_grp = (side + '_' + self.guideObj.mod + iter + 
                                       '_EXTRANODES')
            else:
                self.side_extra_grp = nd.transform(name = (side + '_' + 
                                                           self.guideObj.mod + iter),
                                                   suffix = 'EXTRANODES',
                                                   parent = self.side_mod_grp)
    #END def __create_modular_setup()

    def __get_jnt_name(self):
        #--- this method gets the mod specific skeleton joints
        #--- get the guide joints
        try:
            gjnt = self.guideObj.guide_joints 
        except:
            gjnt = self.guideObj.gd.g_jnt
        for g in gjnt:
            jnt = None
            joints = []
            if isinstance(g, list):
                for i in g:
                    #--- convert from GJNT to JNT
                    jnt = i.split('_GJNT')[0] + '_JNT'
                    joints.append(jnt)
            else:
                #--- convert from GJNT to JNT
                jnt = g.split('_GJNT')[0] + '_JNT'
            if joints:
                for jnt in joints:
                    #--- check if character exists (side is not given)
                    if not cmds.getAttr(jnt + '.char') == self.character:
                        #--- delete the unnecessary character group
                        cmds.delete(self.character)
                        raise Exception('Character: ' + self.character + ' does not exist!')
                if joints:
                    self.joints.append(joints)
                else:
                    raise Exception('No joint matches name: ' + jnt)

            else:
                #--- check if character exists (side is not given)
                if cmds.getAttr(jnt + '.char') == self.character:
                    #--- store the joints in a list
                    if jnt:
                        self.joints.append(jnt)
                    else:
                        raise Exception('No joint matches name: ' + jnt)
                else:
                    #--- delete the unnecessary character group
                    cmds.delete(self.character)
                    raise Exception('Character: ' + self.character + ' does not exist!')                
    #END def __get_jnt_name()

    def __get_jnt_position(self):
        #--- this method filters the position values of the joints
        #--- check if there is a list in the list
        if not isinstance(self.joints[0], list):
            for jnt in self.joints:
                pos = cmds.xform(jnt, 
                                 query = True, 
                                 translation = True, 
                                 worldSpace = True)
                self.joint_position.append(pos)
    #END def __get_jnt_position()

    def __parent_jnt_to_mod(self):
        #--- this method parents the joints to the specific modules
        if self.joints:
            if isinstance(self.joints[0], list):
                for jnt in self.joints:
                        #--- parent joints
                        cmds.parent(jnt[0], self.side_jnt_grp)
            else:
                #--- parent joints
                cmds.parent(self.joints[0], self.side_jnt_grp)
        else:
            raise Exception('There are no joints to parent to mod: ' + self.joints)
    #END def __parent_jnt_to_mod

    def __get_guide_info(self):
        #--- this method gets all the necessary guide information
        if self.side_mod_grp:
            self.side = self.side_mod_grp[0]
        self.mod = self.guideObj.gd.mod
        self.name = self.guideObj.gd.name
    #END def __get_guide_info()

    def __cleanup(self):
        #--- this is the cleanup method
        if cmds.objExists('SKELETON'):
            if not cmds.listRelatives('SKELETON', allDescendents = True):
                cmds.delete('SKELETON')
        print self.side + '_' + self.mod.upper() + ' puppet module successfully created!'
    #END def __cleanup()

    def __create(self):
        #--- create the proper puppet setup
        self.__create_puppet_setup()
        #--- create main control
        self.__create_main_control()
        #--- setup main control
        self.__setup_main_control()
        #--- create the modular group system
        self.__create_modular_setup()
        #--- get the joint names
        self.__get_jnt_name()
        #--- get the joint position values
        self.__get_jnt_position()
        #--- parent the joints properly to their specific mods
        self.__parent_jnt_to_mod()
        #--- get all guide information
        self.__get_guide_info()
        #--- cleanup mod
        self.__cleanup()
    #END def __create()
#END class Puppet()
