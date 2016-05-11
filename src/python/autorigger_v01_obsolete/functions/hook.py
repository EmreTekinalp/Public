'''
Created on 17.10.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: The hook class for the AutoRigger
'''

from maya import cmds
from fundamentals import attribute, node


class Hook(object):
    """
    In this class you create the hooks
    """
    def __init__(self, 
                  mod = None, 
                  hookParent = None,
                  hookChild = None,                  
                  hookType = 'parentConstraint',
                  hookMessage = False,
                  hookParentIndex = -1):
        ########################################################################
        #args
        self.mod             = mod
        self.hookParent      = hookParent
        self.hookChild       = hookChild
        self.hookType        = hookType
        self.hookMessage     = hookMessage
        self.hookParentIndex = hookParentIndex

        #vars
        self.hook_mod        = []
        self.hook_lock       = []
        self.hook_list       = []

        #methods
        self.__create()
    #end def __init__()

    def __hook_prepare(self):
        #--- this method prepares the hooks
        #--- mod
        self.mod = self.mod.gd.mod
        try:
            #--- hookParent            
            self.hookParent = self.hookParent.gd.g_ctl[self.hookParentIndex]
            #--- hookChild
            if isinstance(self.hookChild, list):
                for kid in range(len(self.hookChild)):
                    hook = self.hookChild[kid].gd.g_grp[0]
                    mod = self.hookChild[kid].gd.mod
                    self.hook_list.append(hook)
                    self.hook_mod.append(mod)
            else:
                self.hookChild = self.hookChild.gd.g_grp[0]
                self.hook_mod = self.hookChild.gd.mod
            #--- hookLock
            if isinstance(self.hook_lock, list):
                self.hook_lock = []
                for lock in self.hookChild:
                    hook = lock.main_mod
                    self.hook_lock.append(hook)
            else:
                self.hook_lock = self.hook_lock.main_mod        
        except:
            pass
        if self.hook_list:
            self.hookChild = self.hook_list
    #end def __hook_prepare()

    def __hook_setup(self):
        #--- unlock the self.hookChild attributes
        nd = node.Node()
        attr = attribute.Attribute()
        #--- unlock proper attributes on the child hooks
        try:
            attr.lockAttr(node = self.hookChild, 
                          attribute = ['t', 'r', 's'], 
                          lock = False,
                          show = True)
            if self.hookType:
                if self.hookType == 'parentConstraint':
                    if isinstance(self.hookChild, list):
                        for hook in self.hookChild:
                            pac = nd.parentConstraint(objA = self.hookParent, 
                                                      objB = hook, 
                                                      name = self.mod + 'HOOK', 
                                                      suffix = 'PAC', 
                                                      maintainOffset = True)
                            attr.lockAll(node = hook)
                            attr.lockAttr(node = pac, attribute = ['ihi'])
                    else:
                        pac = nd.parentConstraint(objA = self.hookParent, 
                                                  objB = self.hookChild, 
                                                  name = self.mod + 'HOOK', 
                                                  suffix = 'PAC', 
                                                  maintainOffset = True)
                        attr.lockAll(node = self.hookChild)
                        attr.lockAttr(node = pac, attribute = ['ihi'])
                elif self.hookType == 'pointConstraint':
                    if isinstance(self.hookChild, list):
                        for hook in self.hookChild:
                            pcn = nd.pointConstraint(objA = self.hookParent, 
                                                     objB = hook, 
                                                     name = self.mod + 'HOOK', 
                                                     suffix = 'PAC', 
                                                     maintainOffset = True)
                            attr.lockAll(node = hook)
                            attr.lockAttr(node = pcn, attribute = ['ihi'])
                    else:
                        pcn = nd.pointConstraint(objA = self.hookParent, 
                                                 objB = self.hookChild, 
                                                 name = self.mod + 'HOOK', 
                                                 suffix = 'PAC', 
                                                 maintainOffset = True)
                        attr.lockAll(node = self.hookChild)
                        attr.lockAttr(node = pcn, attribute = ['ihi'])
                elif self.hookType == 'orientConstraint':
                    if isinstance(self.hookChild, list):
                        for hook in self.hookChild:
                            ocn = nd.orientConstraint(objA = self.hookParent, 
                                                      objB = hook, 
                                                      name = self.mod + 'HOOK', 
                                                      suffix = 'PAC', 
                                                      maintainOffset = True)
                            attr.lockAll(node = hook)
                            attr.lockAttr(node = ocn, attribute = ['ihi'])
                    else:
                        ocn = nd.orientConstraint(objA = self.hookParent, 
                                                  objB = self.hookChild, 
                                                  name = self.mod + 'HOOK', 
                                                  suffix = 'PAC', 
                                                  maintainOffset = True)
                        attr.lockAll(node = self.hookChild)
                        attr.lockAttr(node = ocn, attribute = ['ihi'])
        except:
            pass
    #end def __hook_setup()

    def __hook_message(self):
        #--- this method connects the message attributes between the joints
        attr = attribute.Attribute()
        #--- get the guide joints of the selections
        parent_jnt = cmds.listRelatives(self.hookParent, 
                                        allDescendents = True, 
                                        type = 'joint')[0]
        if cmds.objExists(parent_jnt + '.connection'):
            if isinstance(self.hookChild, list):
                for child in self.hookChild:
                    child_jnt = cmds.listRelatives(child, 
                                                   allDescendents = True,
                                                   type = 'joint')[0]
                    if cmds.objExists(child_jnt + '.connection'):
                        cmds.setAttr(child_jnt + '.connection', lock = False)
                        cmds.connectAttr(parent_jnt + '.message', 
                                         child_jnt + '.connection', force = True)
            else:
                child_jnt = cmds.listRelatives(self.hookChild, 
                                               allDescendents = True,
                                               type = 'joint')[0]
                if cmds.objExists(child_jnt + '.connection'):
                    cmds.setAttr(child_jnt + '.connection', lock = False)
                    cmds.connectAttr(parent_jnt + '.message', 
                                     child_jnt + '.connection', force = True)
    #end def __hook_message()

    def __hook_lock_attributes(self):
        #--- this method adds the proper hook attributes to the main mod
        attr = attribute.Attribute()
        #--- add attributes to the main mod
        if isinstance(self.hook_mod, list):
            for mod, main in zip(self.hook_mod, self.hook_lock):
                attr.addAttr(node = main, 
                             attrName = mod + 'Lock', 
                             attrType = 'short', 
                             min = 0, 
                             max = 1, 
                             default = 1, 
                             keyable = False, 
                             channelBox = True)
        else:
            attr.addAttr(node = self.hook_lock, 
                         attrName = self.hook_mod + 'Lock', 
                         attrType = 'short', 
                         min = 0, 
                         max = 1, 
                         default = 1, 
                         keyable = False, 
                         channelBox = True)            
    #end def __hook_lock_attributes()

    def __create(self):
        #--- this method is the main creator
        #--- prepare the hook inputs
        self.__hook_prepare()
        #--- setup the hooks
        self.__hook_setup()
        #--- create hook message connections
        if self.hookMessage:
            self.__hook_message()
        #--- create hook attributes 
        self.__hook_lock_attributes()
    #end def __create()
#end class Hook()
