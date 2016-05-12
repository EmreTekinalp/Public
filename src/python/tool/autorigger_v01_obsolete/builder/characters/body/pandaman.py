'''
Created on 14.10.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@icloud.com
@website: www.gravityofexplosion.com
@brief: This is the pandaman biped body builder
'''

from maya import cmds
from mods import arm, eye, finger, foot, head, leg, neck, spine
from functions import asset, data, hook, puppet, skeleton, skinweight
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
reload(skinweight)
reload(spine)


class BuildBiped(object):
    """
    This dummy class creates a biped body rig system based on the specifications 
    made in the AutoRigger Interface (Properties and Navigator).
    """

    def __init__(self,
                  character = 'PandaMan'):
        #######################  [ BUILD CHARACTER ]  ##########################

        #methods
        self.__create(character = character)
    #END def __init__()

    def __per_character_fixes(self):
        #--- this method setups character specific fixes
        w = skinweight.Weights()
        #--- create skin joints selection set
        skin = w.get_skin_weights()
        cmds.sets(skin[3], name = 'SKINJOINTS')
    #END def __per_character_fixes()

    def __guides(self,
                  character = None):
        #--- create the guides
        #--- SPINE
        self.guide_spine = spine.BipedSpineGuide(character = character)

        #--- NECK
        self.guide_neck = neck.BipedNeckGuide(character = character) 

        #--- HEAD
        self.guide_head = head.BipedHeadGuide(character = character)

        #--- EYES
        self.left_guide_eye = eye.BipedEyeGuide(character = character,
                                                parent = self.guide_head)
        self.right_guide_eye = eye.BipedEyeGuide(character = character,
                                                 side = 'R',
                                                 color = 13,
                                                 mirrorGuideObj=self.left_guide_eye,
                                                 parent = self.guide_head)

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

        #--- eyes
        left_eye = eye.BipedEyePuppet(character = character, 
                                      guideObj = self.left_guide_eye,
                                      puppetObj = center_head)        
        right_eye = eye.BipedEyePuppet(character = character, 
                                       guideObj = self.right_guide_eye,
                                       puppetObj = center_head)

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

        right_thumb = finger.BipedFingerPuppet(character = character, 
                                              guideObj = self.right_guide_thumb,
                                              puppetObj = right_arm)
        right_index = finger.BipedFingerPuppet(character = character, 
                                              guideObj = self.right_guide_index,
                                              puppetObj = right_arm)
        right_middle = finger.BipedFingerPuppet(character = character, 
                                               guideObj = self.right_guide_middle,
                                               puppetObj = right_arm)
        print 'Puppets created!'
    #END def __puppet()

    def __create(self, 
                  character = None):
        #--- this is the main creator of the body rig      
        #--- load the asset
        print 'asset is loading...'
        geo = asset.Asset()
        geo.load_latest_asset(assetPath='D:/Autodesk_Maya/Projects/ProjectPython/scenes/modeling',
                              asset= 'pandaman_mdl') 

        #--- create the guides
        self.__guides(character = character)

        #--- load the guideData
        gd = data.Data()
        gd.load_guide(assetName = 'pandaman') 

        #--- create the skeleton
        self.__skeleton(character = character)

        #--- create the puppet
        self.__puppet(character = character)

        #--- load the locatorData
        gd.load(assetName='pandaman')

        #--- load the weightData
        gd.load(dirName='weightData', assetName='pandaman', dataType='weights')

        #--- per character fixes
        self.__per_character_fixes()
    #END def __create()
#class Builder()

#['R_leg1UpperLeg4_JNT', 'R_leg1UpperLeg3_JNT', 'R_leg1UpperLeg2_JNT', 'R_leg1UpperLeg1_JNT', 'R_leg1Thigh_JNT', 'R_leg1LowerLeg4_JNT', 'R_leg1LowerLeg3_JNT', 'R_leg1LowerLeg2_JNT', 'R_leg1LowerLeg1_JNT', 'R_leg1Knee_JNT', 'R_hip1Pelvis_JNT', 'R_foot1Ball_JNT', 'R_foot1Ankle_JNT', 'R_finger5PinkyE_JNT', 'R_finger5PinkyD_JNT', 'R_finger5PinkyC_JNT', 'R_finger5PinkyB_JNT', 'R_finger5PinkyA_JNT', 'R_finger4RingE_JNT', 'R_finger4RingD_JNT', 'R_finger4RingC_JNT', 'R_finger4RingB_JNT', 'R_finger4RingA_JNT', 'R_finger3MiddleE_JNT', 'R_finger3MiddleD_JNT', 'R_finger3MiddleC_JNT', 'R_finger3MiddleB_JNT', 'R_finger3MiddleA_JNT', 'R_finger2IndexE_JNT', 'R_finger2IndexD_JNT', 'R_finger2IndexC_JNT', 'R_finger2IndexB_JNT', 'R_finger2IndexA_JNT', 'R_finger1ThumbE_JNT', 'R_finger1ThumbD_JNT', 'R_finger1ThumbC_JNT', 'R_finger1ThumbB_JNT', 'R_finger1ThumbA_JNT', 'R_eye1Ball_JNT', 'R_clavicle1Sternal_JNT', 'R_arm1Wrist_JNT', 'R_arm1UpperArm4_JNT', 'R_arm1UpperArm3_JNT', 'R_arm1UpperArm2_JNT', 'R_arm1UpperArm1_JNT', 'R_arm1Shoulder_JNT', 'R_arm1LowerArm4_JNT', 'R_arm1LowerArm3_JNT', 'R_arm1LowerArm2_JNT', 'R_arm1LowerArm1_JNT', 'R_arm1Elbow_JNT', 'L_leg1UpperLeg4_JNT', 'L_leg1UpperLeg3_JNT', 'L_leg1UpperLeg2_JNT', 'L_leg1UpperLeg1_JNT', 'L_leg1Thigh_JNT', 'L_leg1LowerLeg4_JNT', 'L_leg1LowerLeg3_JNT', 'L_leg1LowerLeg2_JNT', 'L_leg1LowerLeg1_JNT', 'L_leg1Knee_JNT', 'L_hip1Pelvis_JNT', 'L_foot1Ball_JNT', 'L_foot1Ankle_JNT', 'L_finger5PinkyE_JNT', 'L_finger5PinkyD_JNT', 'L_finger5PinkyC_JNT', 'L_finger5PinkyB_JNT', 'L_finger5PinkyA_JNT', 'L_finger4RingE_JNT', 'L_finger4RingD_JNT', 'L_finger4RingC_JNT', 'L_finger4RingB_JNT', 'L_finger4RingA_JNT', 'L_finger3MiddleE_JNT', 'L_finger3MiddleD_JNT', 'L_finger3MiddleC_JNT', 'L_finger3MiddleB_JNT', 'L_finger3MiddleA_JNT', 'L_finger2IndexE_JNT', 'L_finger2IndexD_JNT', 'L_finger2IndexC_JNT', 'L_finger2IndexB_JNT', 'L_finger2IndexA_JNT', 'L_finger1ThumbE_JNT', 'L_finger1ThumbD_JNT', 'L_finger1ThumbC_JNT', 'L_finger1ThumbB_JNT', 'L_finger1ThumbA_JNT', 'L_eye1Ball_JNT', 'L_clavicle1Sternal_JNT', 'L_arm1Wrist_JNT', 'L_arm1UpperArm4_JNT', 'L_arm1UpperArm3_JNT', 'L_arm1UpperArm2_JNT', 'L_arm1UpperArm1_JNT', 'L_arm1Shoulder_JNT', 'L_arm1LowerArm4_JNT', 'L_arm1LowerArm3_JNT', 'L_arm1LowerArm2_JNT', 'L_arm1LowerArm1_JNT', 'L_arm1Elbow_JNT', 'C_spine1Vertebrae4_JNT', 'C_spine1Vertebrae3_JNT', 'C_spine1Vertebrae2_JNT', 'C_spine1Vertebrae1_JNT', 'C_spine1Sternum_JNT', 'C_spine1Pelvis_JNT', 'C_neck1CervicalVertebraeA_JNT', 'C_head1Skull_JNT', 'C_head1JawBase_JNT']


BuildBiped()