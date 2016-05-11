'''
@author:  Emre
@date:    Sun 26 Oct 2014 09:12:17 PM PDT
@mail:    e.tekinalp@icloud.com
@brief:   add additional code inside this module
'''


from maya import cmds

from goe_functions import attribute, node
from goe_functions import goemath

reload(attribute)
reload(goemath)
reload(node)


def setAttr(*args, **kwargs):
    """
    @type  args: *args
    @param args: specify nodes as you would do usually with maya cmds
    """
    assert args, "Please specify an existing node and attr."
    assert cmds.objExists(args[0]), "Please specify an existing node and attr."

    #--- vars
    check = False
    obj = args[0].split('.')[0]
    attr = args[0].split('.')[1]

    #--- unlock the attributes
    compound = cmds.attributeQuery(attr, node=obj, listChildren=True)
    if compound:
        for c in compound:
            if cmds.getAttr(obj + '.' + c, lock=True):
                attribute.lock_n_hide(obj, [c], True)
                check = True
    else:
        if cmds.getAttr(args[0], lock=True):
            attribute.lock_n_hide(obj, [attr], True)
            check = True

    #--- set attribute
    try:
        cmds.setAttr(args[0], args[1], args[2], args[3])
    except:
        cmds.setAttr(args[0], args[1])

    #--- lock the attribute
    if check:
        attribute.lock_n_hide(obj, [attr])
#END setAttr()


def connectAttr(*args, **kwargs):
    """
    @type  args: *args
    @param args: specify nodes as you would do usually with maya cmds
    """
    assert args, "Please specify an existing node and attr."
    assert cmds.objExists(args[0]), "Please specify an existing node and attr."
    assert cmds.objExists(args[1]), "Please specify an existing node and attr."

    #--- vars
    check = False

    for arg in args:
        obj = arg.split('.')[0]
        attr = arg.split('.')[1]
        #--- unlock the attributes
        compound = None
        try:
            compound = cmds.attributeQuery(attr, node=obj, listChildren=True)
        except:
            pass
        if compound:
            for c in compound:
                if cmds.getAttr(obj + '.' + c, lock=True):
                    attribute.lock_n_hide(obj, [c], True)
                    check = True
        else:
            if cmds.getAttr(arg, lock=True):
                attribute.lock_n_hide(obj, [attr], True)
                check = True

    #--- set attribute
    cmds.connectAttr(args[0], args[1])

    #--- lock the attribute
    if check:
        obj = args[1].split('.')[0]
        attr = args[1].split('.')[1]
        attribute.lock_n_hide(obj, [attr])
#END connectAttr()


def parent(*args):
    """
    @type  args: *args
    @param args: specify nodes as you would do usually with maya cmds
    """
    for i in args:
        assert i, "Please specify a valid child and a valid parent node"
        assert cmds.objExists(i), "Please specify existing children and parent"
    assert len(args) > 1, "Please specify a valid child and a valid parent node"

    #--- unlock the attributes
    attribute.lock_attributes(list(args[:-1]), ['t', 'r', 's'], False)
    cmds.parent(args)
    attribute.lock_attributes(list(args[:-1]), ['t', 'r', 's'])
#END parent()
