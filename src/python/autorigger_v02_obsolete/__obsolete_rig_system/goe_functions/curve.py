'''
Created on 11.11.2013
@author: Emre Tekinalp
@email: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: This is the curve class
'''

from maya import cmds


class Curve(object):
    """ This class creates nurbsCurves based on the given specifications """

    def __init__(self,
                 side=None,
                 mod=None,
                 name=None,
                 suffix=None,
                 degree=1,
                 point=[0, 0, 0]):

        #--- args
        self._side = side
        self._mod = mod
        self._name = name
        self._suffix = suffix
        self._degree = degree
        self._point = point

        #--- vars
        self.name = list()
        self.transform = None
        self.shape = None

        self.point = point
        self.cv = list()

        self.info = None
        self.arclen = 0.0

        #--- methods
        self.__create()
    #END __init__()

    def __create_curve(self):
        """ Create a curve """
        crv = cmds.curve(degree=self._degree, point=self._point)
        #--- get the curve name based on the given specifications
        crv_name = self.__get_curve_name(curve=crv)

        #--- rename the curve
        curve = cmds.rename(crv, crv_name)
        shape = cmds.listRelatives(curve, allDescendents=True, type='shape')[0]
        #--- append the curve transform and shape node to self.name
        self.name.append(curve)
        self.name.append(shape)
        #--- add the curve transform node to self.transform
        self.transform = curve
        #--- add the curve shape node to self.shape
        self.shape = shape
    #END__create_curve()

    def __get_curve_name(self, curve=None):
        """ Get the curve name """
        crv = None
        if self._mod:
            if self._side:
                if self._name:
                    if self._suffix:
                        #--- side_modName_suffix
                        crv = (self._side + '_' + self._mod + self._name[0].upper()
                               + self._name[1:] + '_' + self._suffix)
                    else:
                        #--- side_modName
                        crv = (self._side + '_' + self._mod +
                               self._name[0].upper() + self._name[1:])
                else:
                    if self._suffix:
                        #--- side_modCrv_suffix
                        crv = (self._side + '_' + self._mod + curve[0].upper() +
                               curve[1:] + '_' + self._suffix)
                    else:
                        #--- side_modCrv
                        crv = (self._side + '_' + self._mod +
                               curve[0].upper() + curve[1:])
            else:
                if self._name:
                    if self._suffix:
                        #--- modName_suffix
                        crv = (self._mod + self._name[0].upper() +
                               self._name[1:] + '_' + self._suffix)
                    else:
                        #--- modName
                        crv = self._mod + self._name[0].upper() + self._name[1:]
                else:
                    #--- modCrv
                    crv = self._mod + curve[0].upper() + curve[1:]
        else:
            if self._side:
                if self._name:
                    if self._suffix:
                        #--- side_name_suffix
                        crv = self._side + '_' + self._name + '_' + self._suffix
                    else:
                        #--- side_name
                        crv = self._side + '_' + self._name
                else:
                    if self._suffix:
                        #--- side_crv_suffix
                        crv = self._side + '_' + curve + '_' + self._suffix
                    else:
                        #--- side_crv
                        crv = self._side + '_' + curve
            else:
                if self._name:
                    if self._suffix:
                        #--- name_suffix
                        crv = (self._name + '_' + self._suffix)
                    else:
                        #--- name
                        crv = (self._name)
                else:
                    #--- crv
                    crv = (curve)
        return crv

    def __get_curve_cv(self):
        """ Store the cv names of the curve """
        cv = cmds.ls(self.transform + '.cv[*]', flatten=True)
        self.cv = cv
    #END __get_curve_cv()

    def __get_curve_info(self):
        """ Get the curve info """
        crv_info = cmds.arclen(self.transform, constructionHistory=True)
        self.info = cmds.rename(crv_info, self._side + '_' + self._mod +
                                self._name[0].upper() + self._name[1:] + 'Info_CRV')
        self.arclen = cmds.arclen(self.transform)
    #END __get_curve_info()

    def __create(self):
        """ Call the methods in the proper order """
        #--- create the curve
        self.__create_curve()
        #--- get the cv names of the curve
        self.__get_curve_cv()
        #--- get the curve info of the curve
        self.__get_curve_info()
    #END __create()
#END Curve()
