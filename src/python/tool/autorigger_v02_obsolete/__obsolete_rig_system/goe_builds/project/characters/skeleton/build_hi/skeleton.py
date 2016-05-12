'''
@author:  Emre
@date:    Thu 20 Nov 2014 08:47:40 PM PST
@mail:    ENTER YOUR EMAIL ADRESS HERE
@brief:   add additional code inside this module
'''

from goe_builds.project.characters.skeleton.build_hi.data import obj
from goe_functions import tools

reload(obj)


def parent_and_child():
    #--- this method setups the parents and children
    arm = obj.larm()
    print arm.armElbowFK.transform
#END parent_and_child()


def mesh_constraints():
    #--- this method setups the mesh constraints
    pass
#END mesh_constraints()


def limit_transforms():
    #--- this method limits the transforms
    pass
#END limit_transforms()


def lock_and_hide():
    #--- this method locks and hides attributes
    pass
#END lock_and_hide()


def build():
    '''this method should be used to call all the other methods'''
    #--- parents and children
    parent_and_child()

    #--- mesh constraints
    mesh_constraints()

    #--- limit transforms
    limit_transforms()

    #--- lock and hide
    lock_and_hide()
#END build()

build()
