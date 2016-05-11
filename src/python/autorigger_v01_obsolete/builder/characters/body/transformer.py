'''
Created on 14.10.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: This is the transformer biped body builder
'''

from maya import cmds
from mods import arm, eye, finger, foot, head, leg, neck, spine
from functions import asset, data, hook, puppet, skeleton
reload(arm)
reload(asset)
reload(data)
reload(eye)
reload(finger)
reload(foot)
reload(head)
reload(hook)
reload(leg)
reload(neck)
reload(puppet)
reload(skeleton)
reload(spine)


class BuildBiped(object):
    """
    This dummy class creates a biped body rig system based on the specifications 
    made in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = 'transformer'):
        #######################  [ BUILD CHARACTER ]  ##########################

        #methods
        self.__create(character = character)
    #END def __init__()

    def __guides(self,
                  character = None):
        #--- create the guides
        #--- SPINE
        self.guide_spine = spine.BipedSpineGuide(character = character)

        #--- NECK
        self.guide_neck = neck.BipedNeckGuide(character = character) 

        #--- HEAD
        self.guide_head = head.BipedHeadGuide(character = character)

        #--- ARMS
        self.left_guide_arm = arm.BipedArmGuide(character = character, 
                                                side = 'L')
        self.right_guide_arm = arm.BipedArmGuide(character = character,
                                                 side = 'R',
                                                 color = 13,
                                                 mirrorGuideObj=self.left_guide_arm)

        #--- FINGERS
        #--- thumb
        self.left_guide_thumb = finger.BipedFingerGuide(character = character, 
                                                        side = 'L', 
                                                        name = 'thumb', 
                                                        position = [[12,20,1],
                                                                    [13,20,1],
                                                                    [14,20,1],
                                                                    [15,20,1]],
                                                        parent = self.left_guide_arm)
        self.right_guide_thumb = finger.BipedFingerGuide(character = character, 
                                                         side = 'R', 
                                                         name = 'thumb', 
                                                         color = 13,
                                                         mirrorGuideObj = self.left_guide_thumb,
                                                         parent = self.right_guide_arm)

        #--- index
        self.left_guide_index = finger.BipedFingerGuide(character = character, 
                                                        side = 'L', 
                                                        name = 'index', 
                                                        position = [[12,20,0.5],
                                                                    [13,20,0.5],
                                                                    [14,20,0.5],
                                                                    [15,20,0.5]],
                                                        parent = self.left_guide_arm)
        self.right_guide_index = finger.BipedFingerGuide(character = character, 
                                                         side = 'R', 
                                                         name = 'index', 
                                                         color = 13,
                                                         mirrorGuideObj = self.left_guide_index,
                                                         parent = self.right_guide_arm)

        #--- middle
        self.left_guide_middle = finger.BipedFingerGuide(character = character, 
                                                         side = 'L', 
                                                         name = 'middle', 
                                                         position = [[12,20,0],
                                                                     [13,20,0],
                                                                     [14,20,0],
                                                                     [15,20,0]],
                                                         parent = self.left_guide_arm)
        self.right_guide_middle = finger.BipedFingerGuide(character = character, 
                                                          side = 'R', 
                                                          name = 'middle', 
                                                          color = 13,
                                                          mirrorGuideObj = self.left_guide_middle,
                                                          parent = self.right_guide_arm)

        #--- ring
        self.left_guide_ring = finger.BipedFingerGuide(character = character, 
                                                       side = 'L', 
                                                       name = 'ring', 
                                                       position = [[12,20,-0.5],
                                                                   [13,20,-0.5],
                                                                   [14,20,-0.5],
                                                                   [15,20,-0.5]],
                                                       parent = self.left_guide_arm)
        self.right_guide_ring = finger.BipedFingerGuide(character = character, 
                                                        side = 'R', 
                                                        name = 'ring', 
                                                        color = 13,
                                                        mirrorGuideObj = self.left_guide_ring,
                                                        parent = self.right_guide_arm)

        #--- LEGS
        self.left_guide_leg = leg.BipedLegGuide(character = character, side = 'L')
        self.right_guide_leg = leg.BipedLegGuide(character = character,side = 'R',
                                                 color = 13,
                                                 mirrorGuideObj = self.left_guide_leg)

        #--- FOOT
        self.left_guide_foot = foot.BipedFootGuide(character = character, side = 'L')
        self.right_guide_foot = foot.BipedFootGuide(character = character, side = 'R',
                                                    color = 13,
                                                    mirrorGuideObj = self.left_guide_foot)

        #--- ADDITIONAL GUIDES
        #--- mouth claws
        self.left_guide_claw = finger.BipedFingerGuide(character = character, 
                                                        side = 'L', 
                                                        name = 'claw', 
                                                        position = [[12,20,1],
                                                                    [13,20,1],
                                                                    [14,20,1],
                                                                    [15,20,1]],
                                                        parent = self.guide_head)
        self.right_guide_claw = finger.BipedFingerGuide(character = character, 
                                                         side = 'R', 
                                                         name = 'claw', 
                                                         color = 13,
                                                         mirrorGuideObj = self.left_guide_claw,
                                                         parent = self.guide_head)

        #--- uppermouth
        self.guide_uppermouth = finger.BipedFingerGuide(character = character, 
                                                        side = 'C', 
                                                        name = 'upperMoouth', 
                                                        position = [[12,20,0.5],
                                                                    [13,20,0.5],
                                                                    [14,20,0.5],
                                                                    [15,20,0.5]],
                                                        parent = self.guide_head)
        #--- guide belly
        self.guide_belly = finger.BipedFingerGuide(character = character, 
                                                         side = 'C', 
                                                         name = 'belly', 
                                                         color = 13,
                                                         parent = self.guide_spine)

        #--- elbow
        self.left_guide_elbow = finger.BipedFingerGuide(character = character, 
                                                         side = 'L', 
                                                         name = 'elbow', 
                                                         position = [[12,20,0],
                                                                     [13,20,0],
                                                                     [14,20,0],
                                                                     [15,20,0]],
                                                         parent = self.left_guide_arm)
        self.right_guide_elbow = finger.BipedFingerGuide(character = character, 
                                                          side = 'R', 
                                                          name = 'elbow', 
                                                          color = 13,
                                                          mirrorGuideObj = self.left_guide_elbow,
                                                          parent = self.right_guide_arm)

        #--- leg support
        self.left_guide_femur = finger.BipedFingerGuide(character = character, 
                                                         side = 'L', 
                                                         name = 'femur', 
                                                         position = [[12,20,0],
                                                                     [13,20,0],
                                                                     [14,20,0],
                                                                     [15,20,0]],
                                                         parent = self.left_guide_leg)
        self.right_guide_femur = finger.BipedFingerGuide(character = character, 
                                                          side = 'R', 
                                                          name = 'femur', 
                                                          color = 13,
                                                          mirrorGuideObj = self.left_guide_femur,
                                                          parent = self.right_guide_leg)

        self.left_guide_tibia = finger.BipedFingerGuide(character = character, 
                                                         side = 'L', 
                                                         name = 'tibia', 
                                                         position = [[12,20,0],
                                                                     [13,20,0],
                                                                     [14,20,0],
                                                                     [15,20,0]],
                                                         parent = self.left_guide_leg)
        self.right_guide_tibia = finger.BipedFingerGuide(character = character, 
                                                          side = 'R', 
                                                          name = 'tibia', 
                                                          color = 13,
                                                          mirrorGuideObj = self.left_guide_tibia,
                                                          parent = self.right_guide_leg)

        #--- create the hooks
        self.__hooks(character = character)
    #END def __guides()

    def __hooks(self, 
                character = None):
        #--- this method creates the guide hooks
        #--- hook head into neck
        hook.Hook(mod = self.guide_head, 
                  hookParent = self.guide_neck, 
                  hookChild = self.guide_head)
        #--- hook clavicle and neck into chest
        hook.Hook(mod = self.guide_spine, 
                  hookParent = self.guide_spine, 
                  hookChild = [self.left_guide_arm,
                               self.left_guide_arm.clavicle,
                               self.guide_neck])
        #--- hook leg into spine
        hook.Hook(mod = self.left_guide_leg.hip, 
                  hookParent = self.guide_spine, 
                  hookChild = self.left_guide_leg.hip,
                  hookParentIndex = 0)
        #--- hook left foot into leg
        hook.Hook(mod = self.left_guide_leg, 
                  hookParent = self.left_guide_leg, 
                  hookChild = self.left_guide_foot,
                  hookType = 'pointConstraint')
        print 'Hooks created!'      
    #END def __hooks()

    def __skeleton(self, 
                   character = None):
        #--- this method creates the skeleton
        skeleton.Skeleton(character = character)
    #END def __skeleton()

    def __puppet(self,
                 character = None):
        #--- this method creates the puppet rigs
        #--- spine
        center_spine = spine.BipedSpinePuppet(character = character,
                                              guideObj = self.guide_spine)

        #--- neck
        center_neck = neck.BipedNeckPuppet(character = character, 
                                           guideObj = self.guide_neck,
                                           puppetObj = center_spine)

        #--- head
        center_head = head.BipedHeadPuppet(character = character, 
                                           guideObj = self.guide_head,
                                           puppetObj = center_neck)

        #--- leg
        left_leg = leg.BipedLegPuppet(character = character,
                                      guideObj = self.left_guide_leg,
                                      puppetObj = center_spine)
        right_leg = leg.BipedLegPuppet(character = character,
                                       guideObj = self.right_guide_leg,
                                       puppetObj = center_spine)

        #--- foot
        left_foot = foot.BipedFootPuppet(character = character, 
                                         guideObj = self.left_guide_foot,
                                         puppetObj = left_leg)
        right_foot = foot.BipedFootPuppet(character = character, 
                                          guideObj = self.right_guide_foot,
                                          puppetObj = right_leg)

        #--- arm
        left_arm = arm.BipedArmPuppet(character = character,  
                                      guideObj = self.left_guide_arm,
                                      puppetObj = center_spine)
        right_arm = arm.BipedArmPuppet(character = character,  
                                       guideObj = self.right_guide_arm,
                                       puppetObj = center_spine)

        #--- finger
        left_thumb = finger.BipedFingerPuppet(character = character, 
                                              guideObj= self.left_guide_thumb,
                                              puppetObj = left_arm)
        left_index = finger.BipedFingerPuppet(character = character, 
                                              guideObj = self.left_guide_index,
                                              puppetObj = left_arm)
        left_middle = finger.BipedFingerPuppet(character = character, 
                                               guideObj = self.left_guide_middle,
                                               puppetObj = left_arm)
        left_ring = finger.BipedFingerPuppet(character = character, 
                                             guideObj = self.left_guide_ring,
                                             puppetObj = left_arm)
        left_pinky = finger.BipedFingerPuppet(character = character, 
                                              guideObj = self.left_guide_pinky,
                                              puppetObj = left_arm)

        right_thumb = finger.BipedFingerPuppet(character = character, 
                                              guideObj = self.right_guide_thumb,
                                              puppetObj = right_arm)
        right_index = finger.BipedFingerPuppet(character = character, 
                                              guideObj = self.right_guide_index,
                                              puppetObj = right_arm)
        right_middle = finger.BipedFingerPuppet(character = character, 
                                               guideObj = self.right_guide_middle,
                                               puppetObj = right_arm)
        right_ring = finger.BipedFingerPuppet(character = character, 
                                              guideObj = self.right_guide_ring,
                                              puppetObj = right_arm)
        right_pinky = finger.BipedFingerPuppet(character = character, 
                                               guideObj = self.right_guide_pinky,
                                               puppetObj = right_arm)
        print 'Puppets created!'
    #END def __puppet()

    def __create(self, 
                  character = None):
        #--- this is the main creator of the body rig      
        #--- load the asset
        print 'asset is loading...'
        geo = asset.Asset()
        geo.load_latest_asset(assetPath='D:/Autodesk_Maya/Projects/ShowReel_2014/scenes/modeling',
                              asset= 'transformer_mdl') 

        #--- create the guides
        self.__guides(character = character)
        
        #--- load the guideData
        gd = data.Data()
        gd.load_guide(assetName = 'transformer') 
        return
        #--- create the skeleton
        self.__skeleton(character = character)

        #--- create the puppet
        self.__puppet(character = character)

        #--- load the locatorData
        gd.load(assetName='transformer') 
    #END def __create()
#class Builder()

BuildBiped()