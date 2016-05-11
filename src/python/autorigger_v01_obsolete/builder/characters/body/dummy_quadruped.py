'''
Created on 20.10.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: This is the dummy quadruped body builder
'''

from maya import cmds
from mods import arm, foot, head, leg, neck, spine, tail
from functions import data, hook


class BuildQuadruped(object):
    """
    This dummy class creates a quadruped body rig system based on the 
    specifications made in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = 'PEGASUS'):
        ########################################################################
        #vars

        #methods
        self.__create(character = character)
    #end def __init__()

    def __reload_modules(self):
        #--- reload all necessary mods
        reload(arm)
        reload(data)
        reload(foot)
        reload(head)
        reload(hook)
        reload(leg)
        reload(neck)
        reload(spine)
        reload(tail)
    #end def __reload_modules()

    def __guides(self, 
                 character = None):
        #--- create the guides
        self.guide_spine = spine.QuadrupedSpineGuide(character = character, 
                                                     color = 22)
        self.guide_hind_leg = leg.QuadrupedLegGuide(character = character,
                                                    mod = 'hindLeg', 
                                                    color = 15)
        self.guide_hind_foot = foot.QuadrupedFootGuide(character = character,
                                                       mod = 'hindFoot',
                                                       color = 15)
        self.guide_front_leg = arm.QuadrupedArmGuide(character = character,
                                                     mod = 'frontLeg',
                                                     color = 15)
        self.guide_front_foot = foot.QuadrupedFootGuide(character = character,
                                                        mod = 'frontFoot',
                                                        color = 15,
                                                        position = [[2.5, 3.0, 5],
                                                                    [2.5, 1.5, 6],
                                                                    [2.5, 0, 7]])
        self.guide_neck = neck.QuadrupedNeckGuide(character = character,
                                                  color = 22) 
        self.guide_head = head.QuadrupedHeadGuide(character = character,
                                                  color = 22)
        self.guide_tail = tail.QuadrupedTailGuide(character = character,
                                                  color = 17)

        #--- create the hooks
        self.__hooks(character = character)

        #--- load the guides
        gd = data.Data()
        gd.load_guide(assetName = character)
    #end def __guides()

    def __hooks(self, 
                 character = None):
        #--- this method creates the guide hooks
        #--- hook head into neck
        hook.Hook(mod = self.guide_head.gd.mod, 
                  hookParent = self.guide_neck.gd.g_ctl[-1], 
                  hookChild = self.guide_head.gd.g_grp[0])
        #--- hook frontLeg and neck into spine
        hook.Hook(mod = self.guide_spine.gd.mod, 
                  hookParent = self.guide_spine.gd.g_ctl[-1], 
                  hookChild = [self.guide_front_leg.scapula.gd.g_grp[0],
                               self.guide_neck.gd.g_grp[0]])
        #--- hook guide_front_foot into guide_front_leg
        hook.Hook(mod = self.guide_front_leg.gd.mod, 
                  hookParent = self.guide_front_leg.gd.g_ctl[-1], 
                  hookChild = self.guide_front_foot.gd.g_grp[0])
        #--- hook guide_hind_leg into spine
        hook.Hook(mod = self.guide_hind_leg.hip.gd.mod, 
                  hookParent = self.guide_spine.gd.g_ctl[0], 
                  hookChild = self.guide_hind_leg.hip.gd.g_grp[0])
        #--- hook guide_hind_foot into guide_hind_leg
        hook.Hook(mod = self.guide_hind_leg.gd.mod, 
                  hookParent = self.guide_hind_leg.gd.g_ctl[-1], 
                  hookChild = self.guide_hind_foot.gd.g_grp[0],
                  hookType = 'pointConstraint')
        #--- hook guide_tail into guide_spine
        hook.Hook(mod = self.guide_head.gd.mod, 
                  hookParent = self.guide_spine.gd.g_ctl[0], 
                  hookChild = self.guide_tail.gd.g_grp[0])
        print 'Hooks created!'        
    #end def __hooks()

    def __skeleton(self):
        #--- this method creates the skeleton
        pass
    #end def __skeleton()

    def __puppet(self,
                  character = None):
        #--- this method creates the puppet rigs
        #--- get the guide joints
        pass
    #end def __puppet()

    def __create(self, 
                  character = None):
        #--- this is the main creator of the body rig
        #--- open a new file scene
        cmds.file(new = 1, force = 1)

        #--- reload the mods
        self.__reload_modules()

        #--- create the guides
        self.__guides(character = character)

        #--- create the puppet
        self.__puppet(character = character)
    #end def __create()
#class Builder()

BuildQuadruped()