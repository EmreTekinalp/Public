'''
@author:  Emre
@date:    Sun 26 Oct 2014 09:12:17 PM PDT
@mail:    e.tekinalp@icloud.com
@brief:   add additional code inside this module
'''

from goe_builds.project.props.robot.build_hi.data import obj
from goe_functions import tools
reload(tools)
reload(obj)

lleg = obj.crhrhr()
rleg = obj.cAasdasda()
asd = obj.larm()


def parent_and_child():
    ''' this method setups the parent and children '''
    print asd.arm0.transform
#END parent_and_child()


def mesh_constraints():
    ''' this method setups the mesh constraints '''
    pass
#END mesh_constraints()


def ik_handle():
    ''' this method creates the ik handles '''
    pass
#END ik_handle()


def limit_transforms():
    ''' this method limits the transforms '''
    pass
#END limit_transforms()


def lock_and_hide():
    ''' this method locks and hides attributes and nodes '''
    pass
#END lock_and_hide()


def build():
    ''' this method should be used to call all the other methods '''
    #--- parent_and_child
    parent_and_child()

    #--- mesh_constraints
    mesh_constraints()

    #--- ik handle
    ik_handle()

    #--- limit transforms
    limit_transforms()

    #--- lock and hide
    lock_and_hide()
#END build()


build()
