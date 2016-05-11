'''
Created on Aug 23, 2015

@author: Emre
'''

from src.python.core import interface
from src.python.setup.arm import biped_arm
from src.python.setup.leg import biped_leg
from src.python.setup.spine import biped_spine


rig = interface.Constructor()

rig.element = biped_spine.Spine('C', 'spine')
rig.element = biped_arm.Arm('L', 'arm')
rig.element = biped_arm.Arm('R', 'arm')
rig.element = biped_leg.Leg('L', 'leg')
rig.element = biped_leg.Leg('R', 'leg')

rig.create_guide()

# bb = BipedB('C', 'bipedB')
# bb.element = Head('C', 'head')
# bb.element = Neck('C', 'neck')
# bb.element = ba
#
# bc = BipedB('C', 'bipedC')
# bc.element = bb
# print '\nguides:\n'
# bc.create_guide()
# print '\npuppets:\n'
# bc.create_puppet()