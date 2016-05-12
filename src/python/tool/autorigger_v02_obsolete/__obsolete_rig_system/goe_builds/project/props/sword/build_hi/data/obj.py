'''
@author:  Emre
@date:    Mon 17 Nov 2014 11:29:19 PM PST
@mail:    e.tekinalp@icloud.com
'''

from goe_functions import data
reload(data)


class lsphere(object):
    def __init__(self):
        self.sphere0= data.InfoPropCmds(grp='L_sphere0_GRP', trn='L_sphere0_CTL', shp='L_sphere0_CTLShape', gmb=None, off=[], jnt='L_sphere0_JNT')
    #END __init__()
#END lsphere()


class cball(object):
    def __init__(self):
        self.ball0= data.InfoPropCmds(grp='C_ball0_GRP', trn='C_ball0_CTL', shp='C_ball0_CTLShape', gmb=None, off=[], jnt='C_ball0_JNT')
        self.ball1= data.InfoPropCmds(grp='C_ball1_GRP', trn='C_ball1_CTL', shp='C_ball1_CTLShape', gmb=None, off=[], jnt='C_ball1_JNT')
    #END __init__()
#END cball()


class rsphere(object):
    def __init__(self):
        self.sphere0= data.InfoPropCmds(grp='R_sphere0_GRP', trn='R_sphere0_CTL', shp='R_sphere0_CTLShape', gmb=None, off=[], jnt='R_sphere0_JNT')
    #END __init__()
#END rsphere()
