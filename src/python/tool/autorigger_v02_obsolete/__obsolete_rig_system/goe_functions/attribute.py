'''
@author:  etekinalp
@date:    Sep 12, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module contains checking methods
'''

from maya import cmds
from goe_functions import check
reload(check)


def lock_n_hide(obj=None, attr=None, unlock=False):
    #--- check parameters
    assert obj, check.error(obj, 1, `obj`)
    assert attr, check.error(attr, 1, `attr`)
    assert isinstance(attr, list), check.error(obj, 12, `attr`)

    for a in attr:
        compound = cmds.attributeQuery(a, node=obj, listChildren=True)
        if compound:
            for c in compound:
                if unlock:
                    cmds.setAttr(obj + '.' + c, lock=False, keyable=True)
                else:
                    cmds.setAttr(obj + '.' + c, lock=True, keyable=False)
        else:
            if unlock:
                cmds.setAttr(obj + '.' + a, lock=False, keyable=True)
            else:
                cmds.setAttr(obj + '.' + a, lock=True, keyable=False)
#END lock_n_hide()


def lock_all(obj=None, unlock=False):
    #--- check parameters
    assert obj, check.error(obj, 1, `obj`)

    if isinstance(obj, list):
        for i in obj:
            lock_all(i, unlock)
        return

    k = cmds.listAttr(obj, k=True)
    cb = cmds.listAttr(obj, cb=True)
    l = cmds.listAttr(obj, l=True)
    if unlock:
        if not l:
            return
        for a in l:
            if (a == 'caching' or a == 'nodeState' or a == 'blackBox' or a == 'CTL'):
                continue
            if ('shear' in a or 'rotateAxis' in a or
                    'inheritsTransform' in a or 'rotateOrder' in a):
                cmds.setAttr(obj + '.' + a, lock=False)
            else:
                cmds.setAttr(obj + '.' + a, lock=False, keyable=True)
    else:
        if not k:
            return
        for a in k:
            try:
                cmds.setAttr(obj + '.' + a, lock=True, keyable=False)
            except:
                pass
        if cb:
            for a in cb:
                cmds.setAttr(obj + '.' + a, lock=True, keyable=False)
                cmds.setAttr(obj + '.' + a, edit=True, channelBox=False)
        for a in ['shearXY', 'shearYZ', 'shearXZ', 'rotateAxisX', 'rotateAxisY',
                  'rotateAxisZ', 'inheritsTransform', 'rotateOrder']:
            if cmds.objExists(obj + '.' + a):
                cmds.setAttr(obj + '.' + a, lock=True, keyable=False)
#END lock_all()


def lock_attributes(obj=None, attr=None, lock=True, hide=True):
    #--- check parameters
    assert obj, check.error(obj, 1, `obj`)
    assert attr, check.error(attr, 1, `attr`)
    assert isinstance(attr, list), check.error(obj, 12, `attr`)

    if isinstance(obj, list):
        for i in obj:
            for a in attr:
                compound = cmds.attributeQuery(a, node=i, listChildren=True)
                if compound:
                    for c in compound:
                        if hide:
                            cmds.setAttr(i + '.' + c, lock=lock, keyable=False)
                        else:
                            cmds.setAttr(i + '.' + c, lock=lock, keyable=True)
                else:
                    if hide:
                        cmds.setAttr(i + '.' + a, lock=lock, keyable=False)
                    else:
                        cmds.setAttr(i + '.' + a, lock=lock, keyable=True)
        return
    for a in attr:
        compound = cmds.attributeQuery(a, node=obj, listChildren=True)
        if compound:
            for c in compound:
                if hide:
                    cmds.setAttr(obj + '.' + c, lock=lock, keyable=False)
                else:
                    cmds.setAttr(obj + '.' + c, lock=lock, keyable=True)
        else:
            if hide:
                cmds.setAttr(obj + '.' + a, lock=lock, keyable=False)
            else:
                cmds.setAttr(obj + '.' + a, lock=lock, keyable=True)
#END lock_attributes()


def hide(obj=None):
    """ Hide the specified node """
    assert obj, "Please specify a transform node"
    cmds.setAttr(obj + '.v', lock=False)
    cmds.setAttr(obj + '.v', 0)
#END hide()
