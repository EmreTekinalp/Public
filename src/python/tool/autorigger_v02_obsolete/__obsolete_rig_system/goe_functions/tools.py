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


def constraint(controlToTransform={},
               constraint=None,
               maintainOffset=True):
    """
    @type  controlToTransform: dict
    @param controlToTransform: specify a key(control) and value(transform), ie.
                               controlToTransform={'controlA:meshB}
                               controlToTransform={'controlA:[meshB, meshC,..]}

    @type  constraint: string
    @param constraint: valid are parent-, point-, orient-, scaleConstraint
                       if None (as default) is set, a parent and scaleConstraint
                       will be created automatically

    @type  maintainOffset: boolean
    @param maintainOffset: Set to True or False
    """
    msg = "controlToTransform: Please specify a valid key and a valid value"
    assert controlToTransform, msg
    for obj in controlToTransform.items():
        key = obj[0]
        value = obj[1]
        msg = "constraint: Key object does not exist: " + str(key)
        assert cmds.objExists(key), msg
        if isinstance(value, list):
            #--- value is a list
            for v in value:
                if constraint == 'parentConstraint':
                    node.parentConstraint(objA=key, objB=v,
                                          maintainOffset=maintainOffset)
                elif constraint == 'pointConstraint':
                    node.pointConstraint(objA=key, objB=v,
                                         maintainOffset=maintainOffset)
                elif constraint == 'orientConstraint':
                    node.orientConstraint(objA=key, objB=v,
                                          maintainOffset=maintainOffset)
                elif constraint == 'scaleConstraint':
                    node.scaleConstraint(objA=key, objB=v,
                                         maintainOffset=maintainOffset)
                else:
                    node.parentConstraint(objA=key, objB=v,
                                          maintainOffset=maintainOffset)
                    node.scaleConstraint(objA=key, objB=v,
                                         maintainOffset=maintainOffset)
        else:
            #--- value is a string
            if constraint == 'parentConstraint':
                node.parentConstraint(objA=key, objB=value,
                                      maintainOffset=maintainOffset)
            elif constraint == 'pointConstraint':
                node.pointConstraint(objA=key, objB=value,
                                     maintainOffset=maintainOffset)
            elif constraint == 'orientConstraint':
                node.orientConstraint(objA=key, objB=value,
                                      maintainOffset=maintainOffset)
            elif constraint == 'scaleConstraint':
                node.scaleConstraint(objA=key, objB=value,
                                     maintainOffset=maintainOffset)
            else:
                node.parentConstraint(objA=key, objB=value,
                                      maintainOffset=maintainOffset)
                node.scaleConstraint(objA=key, objB=value,
                                     maintainOffset=maintainOffset)
#END constraint()


def lock(controlAttributes={}, lock=True, hide=True):
    """
    @type  controlAttributes: dict
    @param controlAttributes: specify a key(control) and value(list), ie.
                              controlToTransform={'controlA:['t', 'sx',...]}

    @type  lock: boolean
    @param lock: lock attributes

    @type  hide: boolean
    @param hide: hide attributes
    """
    if not controlAttributes:
        return
    for attr in controlAttributes.items():
        key = attr[0]
        value = attr[1]
        msg = "lockAttrs: Key object does not exist: " + str(key)
        assert cmds.objExists(key), msg
        for v in value:
            msg = ("lockAttrs: Given key object and value do not exist: " +
                   str(key) + "." + str(v))
            assert (cmds.objExists(key + '.' + v)), msg
        attribute.lock_attributes(key, value, lock, hide)
#END lock()


def limit(limitTransforms=[{'node': None, 'attr': None, 'min': None, 'max': None}]):
    """
    @type  limitTransforms: dictionary in a list
    @param limitTransforms: specify a dictionary in a list which includes
                            the object name, one attribute, the min and the
                            max keys storing the defined limitation values.
                            (ie: [{'node': 'C_bla_CTL',
                                   'attr': 'tx',
                                   'min': -2,
                                   'max': 2}])
    """
    assert limitTransforms, "limit: Please specify valid keys and values!"

    for d in limitTransforms:
        assert isinstance(limitTransforms, list), ("limit: Please specify a list!")
        node = None
        attr = None
        mini = None
        maxi = None
        for i in d.items():
            if i[0] == 'node':
                node = i[1]
            elif i[0] == 'attr':
                attr = i[1]
            elif i[0] == 'min':
                mini = i[1]
            elif i[0] == 'max':
                maxi = i[1]
            else:
                raise Exception("limit: Please define 'node','attr',"
                                "'min','max' as keys!")

        if not node[1]:
            if attr[1]:
                raise Exception("limit: Please specify a node!")
        else:
            if not attr[1]:
                raise Exception("limit: Please specify attribute!")
            if not isinstance(attr[1], str):
                raise Exception("limit: Please specify only one"
                                " valid attribute per dictionary!")

        if node:
            #--- enable the transforms
            enableMin = False
            enableMax = False

            if mini is not None:
                enableMin = True
            if maxi is not None:
                enableMax = True

            #--- specify default limitation values
            if attr.startswith('t'):
                if mini is None:
                    mini = -1
                if maxi is None:
                    maxi = 1
            elif attr.startswith('r'):
                if mini is None:
                    mini = -45
                if maxi is None:
                    maxi = 45
            if attr.startswith('s'):
                if mini is None:
                    mini = -1
                if maxi is None:
                    maxi = 1

            #--- set translation
            if attr == 'tx':
                cmds.transformLimits(node, etx=(enableMin, enableMax), tx=(mini, maxi))
            elif attr == 'ty':
                cmds.transformLimits(node, ety=(enableMin, enableMax), ty=(mini, maxi))
            elif attr == 'tz':
                cmds.transformLimits(node, etz=(enableMin, enableMax), tz=(mini, maxi))

            #--- set rotation
            if attr == 'rx':
                cmds.transformLimits(node, erx=(enableMin, enableMax), rx=(mini, maxi))
            elif attr == 'ry':
                cmds.transformLimits(node, ery=(enableMin, enableMax), ry=(mini, maxi))
            elif attr == 'rz':
                cmds.transformLimits(node, erz=(enableMin, enableMax), rz=(mini, maxi))

            #--- set scale
            if attr == 'sx':
                cmds.transformLimits(node, esx=(enableMin, enableMax), sx=(mini, maxi))
            elif attr == 'sy':
                cmds.transformLimits(node, esy=(enableMin, enableMax), sy=(mini, maxi))
            elif attr == 'sz':
                cmds.transformLimits(node, esz=(enableMin, enableMax), sz=(mini, maxi))
#END limit()


def two_joint_ik(startJoint=None,
                 endEffector=None,
                 ikParent=None):
    """
    @type  startJoint: string
    @param startJoint: specify the startJoint

    @type  endEffector: string
    @param endEffector: specify the endEffector

    @type  ikParent: string
    @param ikParent: specify the parent of the ikHandle
    """
    #--- startJoint
    assert startJoint, "Please specify an existing startJoint!"
    assert cmds.objExists(startJoint), "Please specify an existing startJoint!"
    #--- endEffector
    assert endEffector, "Please specify an existing endEffector!"
    assert cmds.objExists(endEffector), "Please specify an existing endEffector!"
    #--- endParent
    assert ikParent, "Please specify an existing parent for the ikHandle!"
    assert cmds.objExists(ikParent), "Please specify an existing parent node!"

    #--- create joint chain
    child = cmds.listRelatives(startJoint, type='transform')
    if not child or not child[0] == endEffector:
        attribute.lock_attributes(endEffector, ['t', 'r', 's'], False)
        cmds.parent(endEffector, startJoint)
        attribute.lock_attributes(endEffector, ['t', 'r', 's'])
        attribute.lock_attributes(startJoint, ['r'], False)

    #--- compose name
    ikname = ikParent.split('_')[0] + '_' + ikParent.split('_')[1] + '_IKH'
    ikeff = ikParent.split('_')[0] + '_' + ikParent.split('_')[1] + '_EFF'

    #--- create ikHandle
    ik = cmds.ikHandle(startJoint=startJoint, endEffector=endEffector,
                       solver='ikSCsolver', name=ikname)
    eff = cmds.rename(ik[1], ikeff)
    ik.pop(1)
    ik.append(eff)

    #--- parent to ikParent
    cmds.parent(ik[0], ikParent)
    cmds.setAttr(ik[0] + '.t', 0, 0, 0)
    cmds.setAttr(ik[0] + '.r', 0, 0, 0)

    #--- cleanup
    for i in [ik[0], ik[1], 'ikSCsolver']:
        cmds.setAttr(i + '.ihi', 0)
        attribute.lock_all(i)

    return ik
#END two_joint_ik()


def three_joint_ik(jointChain=[],
                   ikParent=None,
                   pvControl=None,
                   pvGroup=None,
                   offset=1):
    """
    @type  jointChain: list
    @param jointChain: specify three joints in a proper order.

    @type  ikParent: string
    @param ikParent: specify the control to parent the ikHandle to

    @type  pvControl: string
    @param pvControl: specify the poleVector control

    @type  pvGroup: string
    @param pvGroup: specify the poleVector group
    """
    #--- jointChain
    assert jointChain, "Please specify an existing startJoint!"

    if not pvControl:
        pvControl = cmds.createNode('transform')
        if not pvGroup:
            pvGroup = pvControl

    jointpos = list()
    #--- create joint chain
    for num, jnt in enumerate(jointChain):
        j = num + 1
        pos = cmds.xform(jnt, query=True, translation=True, worldSpace=True)
        jointpos.append(pos)
        if not j == len(jointChain):
            attribute.lock_attributes(jointChain[j], ['t', 'r', 's', 'v'])
            child = cmds.listRelatives(jnt, type='transform')
            if not child or not child[0] == jointChain[j]:
                cmds.parent(jointChain[j], jnt)
            attribute.lock_attributes(jointChain[j], ['r'], False)
        attribute.lock_attributes(jnt, ['r'], False)

    #--- calculate the polevector position
    attribute.lock_n_hide(pvGroup, ['t', 'r'], True)
    pvpos = goemath.calculate_polevector(jointpos[0], jointpos[1], jointpos[2], offset)
    cmds.xform(pvGroup, translation=(pvpos.x, pvpos.y, pvpos.z), worldSpace=True)
    cmds.setAttr(pvGroup + '.r', 0, 0, 0)
    attribute.lock_n_hide(pvGroup, ['t', 'r'])

    #--- compose name
    ikname = ikParent.split('_')[0] + '_' + ikParent.split('_')[1] + '_IKH'
    ikeff = ikParent.split('_')[0] + '_' + ikParent.split('_')[1] + '_EFF'

    #--- create ikHandle
    ik = cmds.ikHandle(startJoint=jointChain[0], endEffector=jointChain[-1],
                       solver='ikRPsolver', name=ikname)
    eff = cmds.rename(ik[1], ikeff)
    ik.pop(1)
    ik.append(eff)

    #--- create the poleVectorConstraint
    pvc = cmds.poleVectorConstraint(pvControl, ik[0])[0]

    #--- parent to ikParent
    cmds.parent(ik[0], ikParent)
    cmds.setAttr(ik[0] + '.t', 0, 0, 0)
    cmds.setAttr(ik[0] + '.r', 0, 0, 0)

    #--- cleanup
    for i in [ik[0], ik[1], 'ikRPsolver', pvc]:
        cmds.setAttr(i + '.ihi', 0)
        attribute.lock_all(i)
    return ik
#END three_joint_ik()


def n_joint_ik(jointChain=[],
               startJoint=None,
               endEffector=None,
               aimDirection=[1, 0, 0]):
    """
    @type  jointChain: list
    @param jointChain: specify three joints in a proper order.

    @type  startJoint: string
    @param startJoint: specify the startJoint

    @type  endEffector: string
    @param endEffector: specify the endEffector
    """
    pass
#END n_joint_ik()
