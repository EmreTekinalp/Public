'''
@author:  Emre
@date:    Sun 10 May 2015 01:25:23 AM PDT
@mail:    e.tekinalp@icloud.com
'''

from goe_functions import data
reload(data)


class rarm(object):
    def __init__(self):
        self.armShoulderFK = data.InfoPropCmds(grp='R_armShoulderFK_GRP', trn='R_armShoulderFK_CTL', shp='R_armShoulderFK_CTLShape', gmb=None, off=[], jnt='<goe_functions.controls.Control object at 0xefc0450>')
        self.armElbowFK = data.InfoPropCmds(grp='R_armElbowFK_GRP', trn='R_armElbowFK_CTL', shp='R_armElbowFK_CTLShape', gmb=None, off=[], jnt='<goe_functions.controls.Control object at 0x1015c110>')
        self.armWristFK = data.InfoPropCmds(grp='R_armWristFK_GRP', trn='R_armWristFK_CTL', shp='R_armWristFK_CTLShape', gmb=None, off=[], jnt='<goe_functions.controls.Control object at 0x1015c390>')
    #END __init__()
#END rarm()


class larm(object):
    def __init__(self):
        self.armShoulderFK = data.InfoPropCmds(grp='L_armShoulderFK_GRP', trn='L_armShoulderFK_CTL', shp='L_armShoulderFK_CTLShape', gmb=None, off=[], jnt='<goe_functions.controls.Control object at 0xfcffe50>')
        self.armElbowFK = data.InfoPropCmds(grp='L_armElbowFK_GRP', trn='L_armElbowFK_CTL', shp='L_armElbowFK_CTLShape', gmb=None, off=[], jnt='<goe_functions.controls.Control object at 0xefc0510>')
        self.armWristFK = data.InfoPropCmds(grp='L_armWristFK_GRP', trn='L_armWristFK_CTL', shp='L_armWristFK_CTLShape', gmb=None, off=[], jnt='<goe_functions.controls.Control object at 0xefc0710>')
    #END __init__()
#END larm()
