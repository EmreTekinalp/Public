'''
Created on 28.08.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: This is the ikHandle class
'''

from maya import cmds


class IkHandle(object):
    """
    This is the base ik class, which will be used to create 
    everything dealing with iks
    """

    def __init__(self):
        ########################################################################
        #vars
        self.ik_name = []
    #end def __init__()

    def __check_ik_joints(self, 
                            startJoint = None, 
                            endEffector = None): 
        #--- check if startJoint and endEffector exists
        if cmds.objExists(startJoint):
            if cmds.objExists(endEffector):
                pass
            else:
                raise Exception('EndEffector to ' + startJoint + ' is missing!')
        else:
            raise Exception('StartJoint is missing, cannot create ik_handle!')        
    #end def __check_ik_joints()

    def __check_ik_name(self, 
                          startJoint = None, 
                          endEffector = None, 
                          side = None, 
                          name = None, 
                          suffix = None):
        #--- check if joints exist
        self.__check_ik_joints(startJoint = startJoint, endEffector = endEffector)

        #--- get the side info of the startJoint and store it
        side_list = ['C_', 'L_', 'R_', 'c_', 'l_', 'r_']
        for i in side_list:
            if i in startJoint:
                side = startJoint[0]
                break
            elif i in endEffector:
                side = endEffector[0]

        #--- check names
        if side == None:
            if name == None:
                if suffix == None:
                    self.ik_name = 'ik_handle'
                elif suffix == 'JNT':
                    self.ik_name = 'ik_handle_IK'
                else:
                    self.ik_name = 'ik_handle_' + suffix 
            else:
                if suffix == None:
                    self.ik_name = name
                elif suffix == 'JNT':
                    self.ik_name = name + '_IK'
                else:
                    self.ik_name = name + '_' + suffix
        else:
            if name == None:
                if suffix == None:
                    self.ik_name = side + '_ik_handle'
                elif suffix == 'JNT':
                    self.ik_name = side + '_ik_handle_IK'
                else:
                    self.ik_name = side + '_ik_handle_' + suffix 
            else:
                if suffix == None:
                    self.ik_name = side + '_' + name + '_IK'
                elif suffix == 'JNT':
                    self.ik_name = side + '_' + name + '_IK'
                else:
                    self.ik_name = side + '_' + name + '_' + suffix 

        if name == None:
            if side == None:
                if suffix == None:
                    self.ik_name = 'ik_handle'
                elif suffix == 'JNT':
                    self.ik_name = 'ik_handle_IK'
                else:
                    self.ik_name = 'ik_handle_' + suffix 
            else:
                if suffix == None:
                    self.ik_name = side + '_ik_handle'
                elif suffix == 'JNT':
                    self.ik_name = side + 'ik_handle_IK'
                else:
                    self.ik_name = side + '_ik_handle_' + suffix
        else:
            if side == None:
                if suffix == None:
                    self.ik_name = name
                elif suffix == 'JNT':
                    self.ik_name = name + '_IK'
                else:
                    self.ik_name = name + '_' + suffix 
            else:
                if suffix == None:
                    self.ik_name = side + '_' + name + '_IK'
                elif suffix == 'JNT':
                    self.ik_name = side + '_' + name + '_IK'
                else:
                    self.ik_name = side + '_' + name + '_' + suffix 
    #end def __check_ik_name()

    def ikSCsolver(self, 
                    startJoint = None, 
                    endEffector = None, 
                    side = None, 
                    name = None, 
                    suffix = None,
                    parent = None,
                    hide = False):
        #--- do the proper naming checks
        self.__check_ik_name(startJoint = startJoint, endEffector = endEffector, 
                           side = side, name = name, suffix = suffix)

        #--- create the ik_handle
        ik = cmds.ikHandle(startJoint = startJoint, endEffector = endEffector, 
                            name = self.ik_name, solver = 'ikSCsolver')

        #--- rename the effector
        eff = cmds.rename(ik[-1], ik[0] + 'EFF')

        #--- store the ik_handle and effector in a list to return
        ik_handle = [ik[0], eff]

        #--- parent the ik_handle under the specified parent
        if parent:
            cmds.parent(ik_handle[0], parent)

        #--- hide the ikHandle
        if hide:
            cmds.setAttr(ik_handle[0] + '.v', 0)

        cmds.select(clear = 1)
        return ik_handle
    #end def ikSCsolver()

    def ikRPsolver(self, 
                    startJoint = None, 
                    endEffector = None, 
                    side = None, 
                    name = None, 
                    suffix = None,
                    parent = None,
                    hide = False):
        #--- do the proper naming checks
        self.__check_ik_name(startJoint = startJoint, endEffector = endEffector, 
                           side = side, name = name, suffix = suffix)

        #--- create the ik_handle
        ik = cmds.ikHandle(startJoint = startJoint, endEffector = endEffector, 
                           name = self.ik_name, solver = 'ikRPsolver')

        #--- rename the effector
        eff = cmds.rename(ik[-1], ik[0] + 'EFF')

        #--- store the ik_handle and effector in a list to return
        ik_handle = [ik[0], eff]

        #--- parent the ik_handle under the specified parent
        if parent:
            cmds.parent(ik_handle[0], parent)

        #--- hide the ik handle
        if hide:
            cmds.setAttr(ik_handle[0] + '.v', 0)

        cmds.select(clear = 1)
        return ik_handle
    #end def ikRPsolver()

    def ikSplineSolver(self, 
                         startJoint = None, 
                         endEffector = None, 
                         curve = None, 
                         side = None, 
                         name = None, 
                         suffix = None,
                         parent = None,
                         hide = False):
        #--- do the proper naming checks
        self.__check_ik_name(startJoint = startJoint, endEffector = endEffector, 
                           side = side, name = name, suffix = suffix)

        #--- create the ik_handle
        if curve == None:
            ik = cmds.ikHandle(startJoint = startJoint, 
                                endEffector = endEffector, 
                                createCurve = True, 
                                name = self.ik_name, solver = 'ikSplineSolver')
        else:
            if cmds.objExists(curve):
                ik = cmds.ikHandle(startJoint = startJoint, 
                                    endEffector = endEffector, 
                                    curve = curve, createCurve = False, 
                                    name = self.ik_name, solver = 'ikSplineSolver')
            else:
                raise Exception('There is no specified curve: ' + curve )

        #--- rename the effector
        eff = cmds.rename(ik[1], ik[0] + 'EFF')

        #--- store the ik_handle and effector in a list to return
        ik_handle = []
        if curve == None:
            #--- rename the automated curve
            crv = cmds.rename(ik[-1], ik[0] + 'CRV')
            ik_handle = [ik[0], eff, crv]
        else:
            ik_handle = [ik[0], eff, curve]

        #--- parent the ik_handle under the specified parent
        if parent:
            cmds.parent(ik_handle[0], parent)

        #--- hide the ikHandle
        if hide:
            cmds.setAttr(ik_handle[0] + '.v', 0)

        cmds.select(clear = 1)
        return ik_handle
    #end def ikSplineSolver()
#end class IkHandle()