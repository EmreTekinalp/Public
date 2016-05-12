'''
Created on 31.08.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: Create different JointChains
'''

from maya import cmds
from fundamentals import joint, ik


class Chain(object):
    """this is the base jointChain class, which will be used to create jointChains"""

    def __init__(self, 
                  side = None, 
                  name = None, 
                  suffix = None, 
                  position = [0,0,0],
                  orientation = [0.0, 0.0, 0.0], 
                  offset = [0,0,0], 
                  amount = 0, 
                  mirror = False, 
                  radius = 1):
        #vars
        self.joint_names          = []
        self.mirrored_joint_names = []

        #methods
        self.__create(side = side, 
                      name = name, 
                      suffix = suffix, 
                      position = position, 
                      orientation = orientation,
                      offset = offset, 
                      amount = amount, 
                      mirror = mirror, 
                      radius = radius)
    #end def __init__()

    def __reload_modules(self):
        reload(joint)
    #end def __reload_modules()

    def __create_chain(self, 
                         side = None, 
                         name = None, 
                         suffix = None, 
                         position = [0,0,0], 
                         orientation = [0.0, 0.0, 0.0], 
                         offset = [0,0,0], 
                         amount = 3, 
                         mirror = False, 
                         radius = 1):
        #---  this method creates a joint chain by specified flags and values
        jnt_chain = []
        if isinstance(name, list):
            for i in range(len(name)):
                if position == []:
                    if offset == [0, 0, 0]:
                        off = [0, 0 + i, 0]
                        jnt = joint.Joint(side = side, name = name[i], 
                                          suffix = suffix, position = off, 
                                          parent = True, radius = radius)
                        jnt_chain.append(jnt.name)                        
                    elif offset[0] > 0:
                        if offset[1] > 0:
                            if offset[2] > 0:
                                off = [offset[0] + i, offset[1] + i, 
                                       offset[2] + i]
                                jnt = joint.Joint(side = side, name = name[i], 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                jnt_chain.append(jnt.name)
                            else:
                                off = [offset[0] + i, offset[1] + i, 0]
                                jnt = joint.Joint(side = side, name = name[i], 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                jnt_chain.append(jnt.name)
                        else:
                            off = [offset[0] + i, 0, 0]
                            jnt = joint.Joint(side = side, name = name[i], 
                                              suffix = suffix, position = off, 
                                              parent = True, radius = radius)
                            jnt_chain.append(jnt.name)
                    else:
                        if offset[1] > 0:
                            if offset[2] > 0:
                                off = [0, offset[1] + i, offset[2] + i]
                                jnt = joint.Joint(side = side, name = name[i], 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                jnt_chain.append(jnt.name)
                            else:
                                off = [0, offset[1] + i, 0]
                                jnt = joint.Joint(side = side, name = name[i], 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                jnt_chain.append(jnt.name)
                        else:
                            off = [0, 0 + i, 0]
                            jnt = joint.Joint(side = side, name = name[i], 
                                              suffix = suffix, position = off, 
                                              parent = True, radius = radius)
                            jnt_chain.append(jnt.name)
                else:
                    jnt = joint.Joint(side = side, name = name[i], 
                                      suffix = suffix, position = position[i], 
                                      orientation = orientation[i], parent = True, 
                                      radius = radius)       
                    jnt_chain.append(jnt.name)
        else:
            for i in range(amount):
                if position == []:
                    if offset == [0, 0, 0]:
                        off = [0, 0 + i, 0]
                        jnt = joint.Joint(side = side, name = name + `i`, 
                                          suffix = suffix, position = off, 
                                          parent = True, radius = radius)
                        jnt_chain.append(jnt.name)                        
                    elif offset[0] > 0:
                        if offset[1] > 0:
                            if offset[2] > 0:
                                off = [offset[0] + i, offset[1] + i, offset[2] + i]
                                jnt = joint.Joint(side = side, name = name + `i`, 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                jnt_chain.append(jnt.name)
                            else:
                                off = [offset[0] + i, offset[1] + i, 0]
                                jnt = joint.Joint(side = side, name = name + `i`, 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                jnt_chain.append(jnt.name)
                        else:
                            off = [offset[0] + i, 0, 0]
                            jnt = joint.Joint(side = side, name = name + `i`, 
                                              suffix = suffix, position = off, 
                                              parent = True, radius = radius)
                            jnt_chain.append(jnt.name)
                    else:
                        if offset[1] > 0:
                            if offset[2] > 0:
                                off = [0, offset[1] + i, offset[2] + i]
                                jnt = joint.Joint(side = side, name = name + `i`, 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                jnt_chain.append(jnt.name)
                            else:
                                off = [0, offset[1] + i, 0]
                                jnt = joint.Joint(side = side, name = name + `i`, 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                jnt_chain.append(jnt.name)
                        else:
                            off = [0, 0 + i, 0]
                            jnt = joint.Joint(side = side, name = name + `i`, 
                                              suffix = suffix, position = off, 
                                              parent = True, radius = radius)
                            jnt_chain.append(jnt.name)
                else:
                    jnt = joint.Joint(side = side, name = name + `i`, 
                                      suffix = suffix, position = position[i],
                                      orientation = orientation[i], 
                                      parent = True, radius = radius)                    
                    jnt_chain.append(jnt.name)

        cmds.select(clear = 1)
        self.joint_names = jnt_chain

        #--- reorient the jointChain
        for i in self.joint_names:
            cmds.joint(i, 
                       edit = True, 
                       zeroScaleOrient = True, 
                       orientJoint = 'xyz', 
                       secondaryAxisOrient = 'yup')
        #--- zero out the jointOrient values of the last joint
        cmds.setAttr(self.joint_names[-1] + '.jointOrient', 0,0,0)

        #--- mirror joints if specified
        if mirror:
            self.__mirror_chain(side = side)

        return jnt_chain
    #end def __create_chain()

    def __mirror_chain(self, 
                         side = None):
        #--- this method mirros the created jointChain
        #--- create one temporary joint at the origin
        tmp_jnt = cmds.joint(position = [0,0,0])

        #--- parent the chain to that joint
        cmds.parent(self.joint_names[0], tmp_jnt)

        #--- mirror the chain and rename the mirrored side
        if side == 'L':
            self.mirrored_joint_names = cmds.mirrorJoint(self.joint_names[0], 
                                                         mirrorYZ = 1, 
                                                         mirrorBehavior = 1, 
                                                         searchReplace = (side, 'R'))
        elif side == 'l':
            self.mirrored_joint_names = cmds.mirrorJoint(self.joint_names[0], 
                                                         mirrorYZ = 1, 
                                                         mirrorBehavior = 1, 
                                                         searchReplace = (side, 'r'))
        elif side == 'R':
            self.mirrored_joint_names = cmds.mirrorJoint(self.joint_names[0], 
                                                         mirrorYZ = 1, 
                                                         mirrorBehavior = 1, 
                                                         searchReplace = (side, 'L'))
        elif side == 'r':
            self.mirrored_joint_names = cmds.mirrorJoint(self.joint_names[0], 
                                                         mirrorYZ = 1, 
                                                         mirrorBehavior = 1, 
                                                         searchReplace = (side, 'l'))
        else:
            self.mirrored_joint_names = cmds.mirrorJoint(self.joint_names[0], 
                                                         mirrorYZ = 1, 
                                                         mirrorBehavior = 1)

        #--- unparent the chain and delete the temporary joint
        cmds.parent(self.joint_names[0], self.mirrored_joint_names[0], world = 1)        
        cmds.delete(tmp_jnt)

        cmds.select(clear = 1)        
        return self.mirrored_joint_names
    #end def __mirror_chain()

    def __create(self, 
                  side = None, 
                  name = None, 
                  suffix = None, 
                  position = [0,0,0],
                  orientation = [0,0,0], 
                  offset = [0,0,0],
                  amount = 3, 
                  mirror = False, 
                  radius = 1):
        #--- this is the main create method
        #--- reload modules
        self.__reload_modules()
        #--- create the chain
        self.__create_chain(side = side, 
                            name = name, 
                            suffix = suffix, 
                            position = position, 
                            orientation = orientation, 
                            offset = offset, 
                            amount = amount, 
                            mirror = mirror, 
                            radius = radius)
    #end def __create()
#end class Chain()

class FkChain(object):
    """this is the fk_chain class, which will be used to create fk based 
    jointChains with fkControls"""

    def __init__(self, 
                  side = None, 
                  name = None, 
                  suffix = None, 
                  position = [0,0,0], 
                  orientation = [0,0,0], 
                  offset = [0,0,0], 
                  amount = 3, 
                  mirror = False, 
                  radius = 1):
        #vars
        self.fk_joint_names          = []
        self.mirrored_fk_joint_names = []

        #methods
        self.__create(side = side, name = name, suffix = suffix, 
                      position = position, orientation = orientation,
                      offset = offset, amount = amount, mirror = mirror, 
                      radius = radius)
    #end def __init__()

    def reload_modules(self):
        reload(joint)
    #end def reload_modules()

    def create_chain(self, side = None, name = [], suffix = None, position = [], 
                      orientation = [], offset = [0, 0, 0], amount = 3, 
                      mirror = False, radius = 1):
        fk_chain = []
        if isinstance(name, list):
            for i in range(len(name)):
                if position == []:
                    if offset == [0, 0, 0]:
                        off = [0, 0 + i, 0]
                        jnt = joint.Joint(side = side, name = name[i] + 'FK', 
                                          suffix = suffix, position = off, 
                                          parent = True, radius = radius)
                        fk_chain.append(jnt.name)                        
                    elif offset[0] > 0:
                        if offset[1] > 0:
                            if offset[2] > 0:
                                off = [offset[0] + i, offset[1] + i, offset[2] + i]
                                jnt = joint.Joint(side = side, name = name[i] + 'FK', 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                fk_chain.append(jnt.name)
                            else:
                                off = [offset[0] + i, offset[1] + i, 0]
                                jnt = joint.Joint(side = side, name = name[i] + 'FK', 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                fk_chain.append(jnt.name)
                        else:
                            off = [offset[0] + i, 0, 0]
                            jnt = joint.Joint(side = side, name = name[i] + 'FK', 
                                              suffix = suffix, position = off, 
                                              parent = True, radius = radius)
                            fk_chain.append(jnt.name)
                    else:
                        if offset[1] > 0:
                            if offset[2] > 0:
                                off = [0, offset[1] + i, offset[2] + i]
                                jnt = joint.Joint(side = side, name = name[i] + 'FK', 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                fk_chain.append(jnt.name)
                            else:
                                off = [0, offset[1] + i, 0]
                                jnt = joint.Joint(side = side, name = name[i] + 'FK', 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                fk_chain.append(jnt.name)
                        else:
                            off = [0, 0 + i, 0]
                            jnt = joint.Joint(side = side, name = name[i] + 'FK', 
                                              suffix = suffix, position = off, 
                                              parent = True, radius = radius)
                            fk_chain.append(jnt.name)
                else:
                    jnt = joint.Joint(side = side, name = name[i] + 'FK', 
                                      suffix = suffix, position = position[i],
                                      orientation = orientation[i], 
                                      parent = True, radius = radius)                    
                    fk_chain.append(jnt.name)
        else:
            for i in range(amount):
                if position == []:
                    if offset == [0, 0, 0]:
                        off = [0, 0 + i, 0]
                        jnt = joint.Joint(side = side, name = name + `i` + 'FK', 
                                          suffix = suffix, position = off, 
                                          parent = True, radius = radius)
                        fk_chain.append(jnt.name)                        
                    elif offset[0] > 0:
                        if offset[1] > 0:
                            if offset[2] > 0:
                                off = [offset[0] + i, offset[1] + i, offset[2] + i]
                                jnt = joint.Joint(side = side, name = name + `i` + 'FK', 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                fk_chain.append(jnt.name)
                            else:
                                off = [offset[0] + i, offset[1] + i, 0]
                                jnt = joint.Joint(side = side, name = name + `i` + 'FK', 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                fk_chain.append(jnt.name)
                        else:
                            off = [offset[0] + i, 0, 0]
                            jnt = joint.Joint(side = side, name = name + `i` + 'FK', 
                                              suffix = suffix, position = off, 
                                              parent = True, radius = radius)
                            fk_chain.append(jnt.name)
                    else:
                        if offset[1] > 0:
                            if offset[2] > 0:
                                off = [0, offset[1] + i, offset[2] + i]
                                jnt = joint.Joint(side = side, name = name + `i` + 'FK', 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                fk_chain.append(jnt.name)
                            else:
                                off = [0, offset[1] + i, 0]
                                jnt = joint.Joint(side = side, name = name + `i` + 'FK', 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                fk_chain.append(jnt.name)
                        else:
                            off = [0, 0 + i, 0]
                            jnt = joint.Joint(side = side, name = name + `i` + 'FK', 
                                              suffix = suffix, position = off, 
                                              parent = True, radius = radius)
                            fk_chain.append(jnt.name)
                else:
                    jnt = joint.Joint(side = side, name = name + `i` + 'FK', 
                                      suffix = suffix, position = position[i], 
                                      orientation = orientation[i],
                                      parent = True, radius = radius)                    
                    fk_chain.append(jnt.name)

        cmds.select(clear = 1)
        self.fk_joint_names = fk_chain

        #mirror joints if specified
        if mirror == True:
            self.mirror_chain(side = side)

        return fk_chain
    #end def create_chain()

    def mirror_chain(self, side = None):
        #--- create one temporary joint at the origin
        tmp_jnt = cmds.joint(position = [0, 0, 0])

        #--- parent the chain to that joint
        cmds.parent(self.fk_joint_names[0], tmp_jnt)

        #--- mirror the chain and rename the mirrored side
        if side == 'L':
            self.mirrored_fk_joint_names = cmds.mirrorJoint(self.fk_joint_names[0], 
                                                            mirrorYZ = 1, 
                                                            mirrorBehavior = 1, 
                                                            searchReplace = (side, 'R'))
        elif side == 'l':
            self.mirrored_fk_joint_names = cmds.mirrorJoint(self.fk_joint_names[0], 
                                                            mirrorYZ = 1, 
                                                            mirrorBehavior = 1, 
                                                            searchReplace = (side, 'r'))
        elif side == 'R':
            self.mirrored_fk_joint_names = cmds.mirrorJoint(self.fk_joint_names[0], 
                                                            mirrorYZ = 1, 
                                                            mirrorBehavior = 1, 
                                                            searchReplace = (side, 'L'))
        elif side == 'r':
            self.mirrored_fk_joint_names = cmds.mirrorJoint(self.fk_joint_names[0], 
                                                            mirrorYZ = 1, 
                                                            mirrorBehavior = 1, 
                                                            searchReplace = (side, 'l'))
        else:
            self.mirrored_fk_joint_names = cmds.mirrorJoint(self.fk_joint_names[0], 
                                                            mirrorYZ = 1, 
                                                            mirrorBehavior = 1)

        #unparent the chain and delete the temporary joint
        cmds.parent(self.fk_joint_names[0], self.mirrored_fk_joint_names[0], world = 1)        
        cmds.delete(tmp_jnt)

        cmds.select(clear = 1)        
        return self.mirrored_fk_joint_names
    #end def mirror_chain()

    def __create(self, side = None, name = [], suffix = None, position = [], 
                  orientation = [], offset = [0, 0, 0], amount = 3, 
                  mirror = False, radius = 1):
        self.reload_modules()
        self.create_chain(side = side, name = name, suffix = suffix, 
                          position = position, orientation = orientation,
                          offset = offset, amount = amount, mirror = mirror, 
                          radius = radius)
    #end def __create()


class IkChain(object):
    """
    this is the ik_chain class, which will be used to create an ik based 
    jointChain with an specified ik_solver
    """

    def __init__(self, 
                  side = None, 
                  name = None, 
                  suffix = None, 
                  position = [0,0,0],
                  orientation = [0,0,0], 
                  ikSolver = 'ikRPSolver', 
                  ikCurve = None, 
                  ikName = None, 
                  offset = [0, 0, 0], 
                  amount = 0, 
                  mirror = False, 
                  radius = 1,
                  parentJoint = None,
                  parentIk = None):
        ########################################################################
        #vars
        self.ik_joint_names   = []
        self.ik_handle_names  = []

        self.mirrored_ik_joint_names  = []
        self.mirrored_ik_handle_names = []        

        #methods
        self.__create(side = side, 
                      name = name, 
                      suffix = suffix, 
                      position = position, 
                      orientation = orientation, 
                      ikSolver = ikSolver, 
                      ikCurve = ikCurve, 
                      ikName = ikName, 
                      offset = offset, 
                      amount = amount, 
                      mirror = mirror, 
                      radius = radius,
                      parentJoint = parentJoint,
                      parentIk = parentIk)
    #end def __init__()

    def __reload_modules(self):
        reload(joint)
        reload(ik)
    #end def __reload_modules()

    def __create_chain(self, 
                         side = None, 
                         name = None, 
                         suffix = None, 
                         position = [0,0,0],
                         orientation = [0,0,0], 
                         ikSolver = 'ikRPsolver', 
                         ikCurve = None, 
                         ikName = None, 
                         offset = [0, 0, 0], 
                         amount = 0, 
                         mirror = True, 
                         radius = 1,
                         parentJoint = None,
                         parentIk = None):
        #--- this method creates the ikChain
        cmds.select(clear = True)
        ik_chain = []
        if isinstance(name, list):
            for i in range(len(name)):
                if position == []:
                    if offset == [0, 0, 0]:
                        off = [0, 0 + i, 0]
                        jnt = joint.Joint(side = side, name = name[i] + 'IK', 
                                          suffix = suffix, position = off, 
                                          parent = True, radius = radius)
                        ik_chain.append(jnt.name)                        
                    elif offset[0] > 0:
                        if offset[1] > 0:
                            if offset[2] > 0:
                                off = [offset[0] + i, offset[1] + i, offset[2] + i]
                                jnt = joint.Joint(side = side, name = name[i] + 'IK', 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                ik_chain.append(jnt.name)
                            else:
                                off = [offset[0] + i, offset[1] + i, 0]
                                jnt = joint.Joint(side = side, name = name[i] + 'IK', 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                ik_chain.append(jnt.name)
                        else:
                            off = [0 + i, 0, 0]
                            jnt = joint.Joint(side = side, name = name[i] + 'IK', 
                                              suffix = suffix, position = off, 
                                              parent = True, radius = radius)
                            ik_chain.append(jnt.name)
                    else:
                        if offset[1] > 0:
                            if offset[2] > 0:
                                off = [0, offset[1] + i, offset[2] + i]
                                jnt = joint.Joint(side = side, name = name[i] + 'IK', 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                ik_chain.append(jnt.name)
                            else:
                                off = [0, offset[1] + i, 0]
                                jnt = joint.Joint(side = side, name = name[i] + 'IK', 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                ik_chain.append(jnt.name)
                        else:
                            off = [0, 0 + i, 0]
                            jnt = joint.Joint(side = side, name = name[i] + 'IK', 
                                              suffix = suffix, position = off, 
                                              parent = True, radius = radius)
                            ik_chain.append(jnt.name)
                else:
                    if not len(orientation) == len(name):
                        jnt = joint.Joint(side = side, name = name[i] + 'IK', 
                                          suffix = suffix, position = position[i],
                                          orientation = orientation, 
                                          parent = True, radius = radius)
                    else:
                        jnt = joint.Joint(side = side, name = name[i] + 'IK', 
                                          suffix = suffix, position = position[i],
                                          orientation = orientation[i], 
                                          parent = True, radius = radius)                        
                    ik_chain.append(jnt.name)
        else:
            for i in range(amount):
                if position == []:
                    if offset == [0, 0, 0]:
                        off = [0, 0 + i, 0]
                        jnt = joint.Joint(side = side, name = name + `i` + 'IK', 
                                          suffix = suffix, position = off, 
                                          parent = True, radius = radius)
                        ik_chain.append(jnt.name)                        
                    elif offset[0] > 0:
                        if offset[1] > 0:
                            if offset[2] > 0:
                                off = [offset[0] + i, offset[1] + i, offset[2] + i]
                                jnt = joint.Joint(side = side, name = name + `i` + 'IK', 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                ik_chain.append(jnt.name)
                            else:
                                off = [offset[0] + i, offset[1] + i, 0]
                                jnt = joint.Joint(side = side, name = name + `i` + 'IK', 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                ik_chain.append(jnt.name)
                        else:
                            off = [offset[0] + i, 0, 0]
                            jnt = joint.Joint(side = side, name = name + `i` + 'IK', 
                                              suffix = suffix, position = off, 
                                              parent = True, radius = radius)
                            ik_chain.append(jnt.name)
                    else:
                        if offset[1] > 0:
                            if offset[2] > 0:
                                off = [0, offset[1] + i, offset[2] + i]
                                jnt = joint.Joint(side = side, name = name + `i` + 'IK', 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                ik_chain.append(jnt.name)
                            else:
                                off = [0, offset[1] + i, 0]
                                jnt = joint.Joint(side = side, name = name + `i` + 'IK', 
                                                  suffix = suffix, position = off, 
                                                  parent = True, radius = radius)
                                ik_chain.append(jnt.name)
                        else:
                            off = [0, 0 + i, 0]
                            jnt = joint.Joint(side = side, name = name + `i` + 'IK', 
                                              suffix = suffix, position = off, 
                                              parent = True, radius = radius)
                            ik_chain.append(jnt.name)
                else:
                    if not len(orientation) == len(name):
                        jnt = joint.Joint(side = side, name = name + `i` + 'IK', 
                                          suffix = suffix, position = position[i], 
                                          orientation = orientation,
                                          parent = True, radius = radius)                    
                    else:
                        jnt = joint.Joint(side = side, name = name + `i` + 'IK', 
                                          suffix = suffix, position = position[i], 
                                          orientation = orientation[i],
                                          parent = True, radius = radius)                    
                    ik_chain.append(jnt.name)

        cmds.select(clear = 1)
        self.ik_joint_names = ik_chain

        #--- reorient the jointChain
        for i in self.ik_joint_names:
            cmds.joint(i, 
                       edit = True, 
                       zeroScaleOrient = True, 
                       orientJoint = 'xyz', 
                       secondaryAxisOrient = 'yup')
        #--- zero out the jointOrient values of the last joint
        cmds.setAttr(self.ik_joint_names[-1] + '.jointOrient', 0,0,0)

        #--- create ikHandle
        self.__create_ik_handle(side = side, 
                                name = name, 
                                suffix = suffix, 
                                ikSolver = ikSolver, 
                                ikCurve = ikCurve, 
                                ikName = ikName)

        #--- mirror joints
        if mirror:
            self.__mirror_chain(side = side)

        #--- parent the joints and ikHandles
        #--- joints
        if parentJoint:
            if mirror:
                if isinstance(parentJoint, list):
                    if len(parentJoint) == 2:
                        cmds.parent(self.ik_joint_names[0], parentJoint[0])
                        cmds.parent(self.mirrored_ik_joint_names[0], parentJoint[1])
                    else:
                        raise Exception('First element is left and second is right!'
                                        'You have to specify proper parent nodes!')
                else:
                    cmds.parent(self.ik_joint_names[0], 
                                self.mirrored_ik_joint_names[0],
                                parentIk)
            else:
                cmds.parent(self.ik_joint_names[0], parentJoint)
        #-- ikHandles
        if parentIk:
            if mirror:
                if isinstance(parentIk, list):
                    if len(parentIk) == 2:
                        cmds.parent(self.ik_handle_names[0], parentIk[0])
                        cmds.parent(self.mirrored_ik_handle_names[0], parentIk[1])
                    else:
                        raise Exception('First element is left and second is right!'
                                        'You have to specify proper parent nodes!')
                else:
                    cmds.parent(self.ik_handle_names[0], 
                                self.mirrored_ik_handle_names[0],
                                parentIk)
            else:
                cmds.parent(self.ik_handle_names[0], parentIk)
    #end def __create_chain()

    def __create_ik_handle(self,
                             side = None, 
                             name = None, 
                             suffix = None, 
                             ikSolver = 'ikRPSolver', 
                             ikCurve = None, 
                             ikName = None):
        #--- this method creates the specified ikHandle
        ikH = ik.IkHandle()
        if ikName == None:
            #--- ikSCSolver
            if ikSolver == 'ikSCSolver':
                self.ik_handle_names = ikH.ikSCsolver(startJoint = self.ik_joint_names[0], 
                                                      endEffector = self.ik_joint_names[-1], 
                                                      side = side, name = name[0], 
                                                      suffix = suffix)
            #--- ikSplineSolver
            elif ikSolver == 'ikSplineSolver':
                self.ik_handle_names = ikH.ikSplineSolver(startJoint = self.ik_joint_names[0],
                                                          endEffector = self.ik_joint_names[-1], 
                                                          curve = ikCurve, 
                                                          side = side, 
                                                          name = name[0], 
                                                          suffix = suffix)
            #--- ikRPsolver
            else:
                self.ik_handle_names = ikH.ikRPsolver(startJoint = self.ik_joint_names[0], 
                                                      endEffector = self.ik_joint_names[-1], 
                                                      side = side, name = name[0], 
                                                      suffix = suffix)
        else:
            #--- ikSCSolver            
            if ikSolver == 'ikSCSolver':
                self.ik_handle_names = ikH.ikSCsolver(startJoint = self.ik_joint_names[0], 
                                                      endEffector = self.ik_joint_names[-1], 
                                                      side = side, name = ikName, 
                                                      suffix = suffix)
            #--- ikSplineSolver
            elif ikSolver == 'ikSplineSolver':
                self.ik_handle_names = ikH.ikSplineSolver(startJoint = self.ik_joint_names[0],
                                                          endEffector = self.ik_joint_names[-1], 
                                                          curve = ikCurve, 
                                                          side = side, 
                                                          name = ikName, 
                                                          suffix = suffix)
            #--- ikRPsolver
            else:
                self.ik_handle_names = ikH.ikRPsolver(startJoint = self.ik_joint_names[0], 
                                                      endEffector = self.ik_joint_names[-1], 
                                                      side = side, 
                                                      name = ikName, 
                                                      suffix = suffix)
        return self.ik_handle_names
    #end def __create_ik_handle()

    def __mirror_chain(self,
                         side = None):
        #--- this method mirrors the jointChain and the ikHandle
        #--- create one temporary joint at the origin
        tmp_jnt = cmds.joint(position = [0, 0, 0])

        #--- parent the chain to that joint
        cmds.parent(self.ik_joint_names[0], tmp_jnt)

        #--- mirror the chain and rename the mirrored side
        if side == 'L':
            self.mirrored_ik_joint_names = cmds.mirrorJoint(self.ik_joint_names[0], 
                                                            mirrorYZ = 1, 
                                                            mirrorBehavior = 1, 
                                                            searchReplace = (side, 'R'))
        elif side == 'l':
            self.mirrored_ik_joint_names = cmds.mirrorJoint(self.ik_joint_names[0],
                                                            mirrorYZ = 1, 
                                                            mirrorBehavior = 1, 
                                                            searchReplace = (side, 'r'))
        elif side == 'R':
            self.mirrored_ik_joint_names = cmds.mirrorJoint(self.ik_joint_names[0], 
                                                            mirrorYZ = 1, 
                                                            mirrorBehavior = 1, 
                                                            searchReplace = (side, 'L'))
        elif side == 'r':
            self.mirrored_ik_joint_names = cmds.mirrorJoint(self.ik_joint_names[0], 
                                                            mirrorYZ = 1, 
                                                            mirrorBehavior = 1, 
                                                            searchReplace = (side, 'l'))
        else:
            self.mirrored_ik_joint_names = cmds.mirrorJoint(self.ik_joint_names[0], 
                                                            mirrorYZ = 1, 
                                                            mirrorBehavior = 1)

        #--- unparent the chain and delete the temporary joint
        cmds.parent(self.ik_joint_names[0], self.mirrored_ik_joint_names[0],
                    world = 1)        
        cmds.delete(tmp_jnt)

        cmds.select(clear = 1)

        #--- rename the side of the mirrored effector correctly and store the ik 
        #--- and effector in a list
        mirrored_ik  = self.mirrored_ik_joint_names[0][0] + self.ik_handle_names[0][1:]
        mirrored_eff = cmds.rename(self.mirrored_ik_joint_names[-1], 
                                   self.mirrored_ik_joint_names[0][0] + 
                                   self.ik_handle_names[-1][1:])
        self.mirrored_ik_handle_names = [mirrored_ik, mirrored_eff]
        self.mirrored_ik_joint_names.pop(-1)
    #end def __mirror_chain()

    def __create(self, 
                  side = None, 
                  name = None, 
                  suffix = None, 
                  position = [0,0,0], 
                  orientation = [0,0,0], 
                  ikSolver = 'ikRPsolver', 
                  ikCurve = None, 
                  ikName = None, 
                  offset = [0, 0, 0], 
                  amount = 0, 
                  mirror = True, 
                  radius = 1,
                  parentJoint = None,
                  parentIk = None):
        #--- this is the main create method
        #--- reload modules
        self.__reload_modules()
        #--- create the ik chain
        self.__create_chain(side = side, 
                            name = name, 
                            suffix =suffix, 
                            position = position, 
                            orientation = orientation, 
                            ikSolver = ikSolver, 
                            ikCurve = ikCurve, 
                            ikName = ikName,
                            offset = offset, 
                            amount = amount, 
                            mirror = mirror, 
                            radius = radius,
                            parentJoint = parentJoint,
                            parentIk = parentIk)
    #end def __create()
#end class IkChain()