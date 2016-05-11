'''
Created on 11.11.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: This is the curve class
'''

from maya import cmds

class Curve(object):
    '''
    This class creates nurbsCurves based on the given specifications
    '''

    def __init__(self,
                  character = None,
                  mod = None,
                  side = None,
                  name = None,
                  suffix = None,
                  degree = 1,
                  point = [0,0,0]):
        ########################################################################
        #vars
        self.name       = []
        self.transform  = None
        self.shape      = None

        self.point      = point
        self.cv         = []

        self.info       = None
        self.arclen     = 0.0

        #methods
        self.__create(character = character,
                      mod = mod,
                      side = side,
                      name = name,
                      suffix = suffix,
                      degree = degree,
                      point = point)
    #end def __init__()

    def __create_curve(self,
                         character = None,
                         mod = None,
                         side = None,
                         name = None,
                         suffix = None,
                         degree = 1,
                         point = [0,0,0]):
        #--- this method creates a curve
        crv = cmds.curve(degree = degree, point = point)
        crv_name = None
        #--- get the curve name based on the given specifications
        if mod:
            if side:
                if name:
                    if suffix:
                        #--- side_modName_suffix
                        crv_name = (side + '_' + mod + name[0].upper() +
                                    name[1:] + '_' + suffix)
                    else:
                        #--- side_modName
                        crv_name = (side + '_' + mod + name[0].upper() +
                                    name[1:])
                else:
                    if suffix:
                        #--- side_modCrv_suffix
                        crv_name = (side + '_' + mod + crv[0].upper() +
                                    crv[1:] + '_' + suffix)
                    else:
                        #--- side_modCrv
                        crv_name = (side + '_' + mod + crv[0].upper() +
                                    crv[1:])
            else:
                if name:
                    if suffix:
                        #--- modName_suffix
                        crv_name = (mod + name[0].upper() +
                                    name[1:] + '_' + suffix)
                    else:
                        #--- modName
                        crv_name = (mod + name[0].upper() + name[1:])
                else:
                    #--- modCrv
                    crv_name = (mod + crv[0].upper() + crv[1:])
        else:
            if side:
                if name:
                    if suffix:
                        #--- side_name_suffix
                        crv_name = (side + '_' + name + '_' + suffix)
                    else:
                        #--- side_name
                        crv_name = (side + '_' + name)
                else:
                    if suffix:
                        #--- side_crv_suffix
                        crv_name = (side + '_' + crv + '_' + suffix)
                    else:
                        #--- side_crv
                        crv_name = (side + '_' + crv)
            else:
                if name:
                    if suffix:
                        #--- name_suffix
                        crv_name = (name + '_' + suffix)
                    else:
                        #--- name
                        crv_name = (name)
                else:
                    #--- crv
                    crv_name = (crv)
        #--- rename the curve
        curve = cmds.rename(crv, crv_name)
        shape = cmds.listRelatives(curve,
                                   allDescendents = True,
                                   type = 'shape')[0]
        #--- append the curve transform and shape node to self.name
        self.name.append(curve)
        self.name.append(shape)
        #--- add the curve transform node to self.transform
        self.transform = curve
        #--- add the curve shape node to self.shape
        self.shape = shape
    #end def __create_curve()

    def __get_curve_cv(self):
        #--- this method stores the cv names of the curve
        cv = cmds.ls(self.transform + '.cv[*]', flatten = True)
        self.cv = cv
    #end def __get_curve_cv()

    def __get_curve_info(self,
                           character = None,
                           mod = None,
                           side = None,
                           name = None):
        #--- this method gets the curve info
        crv_info = cmds.arclen(self.transform, constructionHistory = True)
        self.info = cmds.rename(crv_info, side + '_' + mod + name[0].upper() +
                                name[1:] + 'Info_CRV')
        self.arclen = cmds.arclen(self.transform)
    #end def __get_curve_info()

    def __create(self,
                  character = None,
                  mod = None,
                  side = None,
                  name = None,
                  suffix = None,
                  degree = 1,
                  point = [0,0,0]):
        #--- this is the main creation method
        #--- create the curve
        self.__create_curve(character = character,
                            mod = mod,
                            side = side,
                            name = name,
                            suffix = suffix,
                            degree = degree,
                            point = point)
        #--- get the cv names of the curve
        self.__get_curve_cv()
        #--- get the curve info of the curve
        self.__get_curve_info(character = character,
                              mod = mod,
                              side = side,
                              name = name)
    #end def __create()
#end class Curve()