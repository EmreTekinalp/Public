'''
@author:  etekinalp
@date:    Nov 26, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module contains renaming methods
'''

from maya import cmds


def deformer(mod=None,
             side=None,
             name=None,
             suffix=None,
             obj=None):
    """ Rename the given node and return its final name """
    #--- check which one of the given obj is the transform node
    trn = list()
    non = list()
    if isinstance(obj, list):
        for i in obj:
            if cmds.nodeType(i) == 'transform':
                trn.append(i)
            else:
                if not cmds.nodeType(i) == 'shape':
                    non.append(i)
    else:
        if cmds.nodeType(obj) == 'transform':
            trn.append(obj)
        else:
            if not cmds.nodeType(obj) == 'shape':
                non.append(obj)
    if trn:
        obj = trn[0]
    if non:
        non = non[0]
    obj_name = None
    #--- get the curve name based on the given specifications
    if mod:
        if side:
            if name:
                if suffix:
                    #--- side_modName_suffix
                    obj_name = (side + '_' + mod + name[0].upper() +
                                name[1:] + '_' + suffix)
                else:
                    #--- side_modName
                    obj_name = side + '_' + mod + name[0].upper() + name[1:]
            else:
                if suffix:
                    #--- side_modCrv_suffix
                    obj_name = (side + '_' + mod + obj[0].upper() +
                                obj[1:] + '_' + suffix)
                else:
                    #--- side_modCrv
                    obj_name = side + '_' + mod + obj[0].upper() + obj[1:]
        else:
            if name:
                if suffix:
                    #--- modName_suffix
                    obj_name = mod + name[0].upper() + name[1:] + '_' + suffix
                else:
                    #--- modName
                    obj_name = mod + name[0].upper() + name[1:]
            else:
                #--- modCrv
                obj_name = mod + obj[0].upper() + obj[1:]
    else:
        if side:
            if name:
                if suffix:
                    #--- side_name_suffix
                    obj_name = side + '_' + name + '_' + suffix
                else:
                    #--- side_name
                    obj_name = side + '_' + name
            else:
                if suffix:
                    #--- side_obj_suffix
                    obj_name = side + '_' + obj + '_' + suffix
                else:
                    #--- side_obj
                    obj_name = side + '_' + obj
        else:
            if name:
                if suffix:
                    #--- name_suffix
                    obj_name = name + '_' + suffix
                else:
                    #--- name
                    obj_name = name
            else:
                #--- obj
                obj_name = obj
    #--- rename the obj
    transform = cmds.rename(obj, obj_name)
    shape = list()
    if cmds.listRelatives(transform, children=True):
        shape = cmds.listRelatives(transform, allDescendents=True, type='shape')[0]
    #--- rename the nonTransform/nonShape obj
    result = list()
    if non:
        if cmds.objExists(non):
            non = cmds.rename(non, obj_name + non[0].upper() + non[1:])
            result = [transform, shape, non]
        else:
            if shape:
                result = [transform, shape]
            else:
                result = transform
    else:
        result = [transform, shape]
    return result
#END deformer()
