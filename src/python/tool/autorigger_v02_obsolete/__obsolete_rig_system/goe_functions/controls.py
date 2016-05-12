'''
@author:  etekinalp
@date:    Aug 30, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module creates the main controls
'''

from maya import cmds
from goe_plugins import plugin_master
from goe_functions import attribute, check


class Control(object):
    def __init__(self,
                 side=None,
                 name=None,
                 shape=0,
                 size=1,
                 orientation=0,
                 color=0,
                 shapeOffset=[0, 0, 0],
                 shapeScale=[1, 1, 1],
                 position=[0, 0, 0],
                 rotation=[0, 0, 0],
                 rotateOrder='xyz',
                 offsetGroups=0,
                 withGimbal=False,
                 limitTransforms=[{'node': None, 'attr': None,
                                   'min': None, 'max': None}],
                 lockAttrs={None: [None]},
                 lockGroups=True,
                 parent=None,
                 exists=False):
        """
        @type  side: string
        @param side: specify the side. Valid sides are 'C', 'L', 'R'.

        @type  name: string
        @param name: specify the name. Non-valid characters are '_'.

        @type  shape: integer
        @param shape: specify the shape number. The range goes from 0-38.

        @type  size: float
        @param size: specify the global size of the shape.

        @type  orientation: integer
        @param orientation: specify the orientation of the shape.

        @type  color: integer
        @param color: specify the 'maya numeric style' color of the shape.

        @type  shapeOffset: 3Float list
        @param shapeOffset: specify the shapeOffset of the control shape.

        @type  shapeScale: 3Float list
        @param shapeScale: specify the local scale of the control shape.

        @type  position: 3Float list
        @param position: specify the position of the top control group.

        @type  rotation: 3Float list
        @param rotation: specify the rotation of the top control group.

        @type  rotateOrder: string
        @param rotateOrder: specify the rotateOrder of the control.

        @type  offsetGroups: integer
        @param offsetGroups: specify the amount of offset groups of the control.

        @type  withGimbal: bool
        @param withGimbal: specify if a gimbalLock control should be created.

        @type  limitTransforms: dict in a list
        @param limitTransforms: node = 'group', 'offset0-n', 'transform', 'shape'
                                attr = specify one single attribute as string
                                min = specify any kind of numeric value
                                max = specify any kind of numeric value

        @type  lockAttrs: dict
        @param lockAttrs: key = specify 'group', 'offset0-n', 'transform', 'shape'
                          value = specify a list with limitless valid attributes

        @type  lockGroups: bool
        @param lockGroups: all attributes of offset and top groups will be locked

        @type  parent: string
        @param parent: specify the parent of the top control group.

        @type  exists: bool
        @param exists: specify if control exists and return transform, group
                       and the shape of the given specifications.
        """
        #--- args
        self._side              = side
        self._name              = name
        self._shape             = shape
        self._size              = size
        self._orientation       = orientation
        self._color             = color
        self._shapeOffset       = shapeOffset
        self._shapeScale        = shapeScale
        self._position          = position
        self._rotation          = rotation
        self._rotateOrder       = rotateOrder
        self._offsetGroups      = offsetGroups
        self._withGimbal        = withGimbal
        self._limitTransforms   = limitTransforms
        self._lockAttrs         = lockAttrs
        self._lockGroups        = lockGroups
        self._parent            = parent
        self._exists            = exists

        #--- vars
        self.group              = None
        self.transform          = None
        self.shape              = None
        self.gimbal             = None
        self.offsets            = list()

        self._gshape            = None

        #--- methods
        self.__create()
    #END __init__()

    def __check_parameters(self):
        #--- side
        assert self._side, check.error(self, 2, `self._side`)
        assert isinstance(self._side, str), check.error(self, 2, `self._side`)
        err = check.error(self, 1, `self._side`, "Valid sides are 'C', 'R', 'L'!")
        assert (self._side == 'C' or self._side == 'R' or self._side == 'L'), err

        #--- name
        assert self._name, check.error(self, 2, `self._name`)
        assert isinstance(self._side, str), check.error(self, 2, `self._name`)
        assert not "_" in self._name, check.error(self, 1, `self._name`, "No '_' please!") 

        #--- rotateOrder
        err = check.error(self, 1, `self._rotateOrder`)
        assert (self._rotateOrder == 'xyz' or self._rotateOrder == 'yzx' or
                self._rotateOrder == 'zxy' or self._rotateOrder == 'xzy' or 
                self._rotateOrder == 'yxz' or self._rotateOrder == 'zyx'), err

        #--- limitTransforms
        for d in self._limitTransforms:
            node = None
            attr = None
            for i in d.items():
                if i[0] == 'node':
                    node = i[1]
                elif i[0] == 'attr':
                    attr = i[1]
                elif i[0] == 'min':
                    pass
                elif i[0] == 'max':
                    pass
                else:
                    raise Exception(check.error(self, 1, i))
            if not node:
                break
            assert attr, check.error(self, 1, `attr`)
            assert not isinstance(attr, list), check.error(self, 3, `attr`)
            if not (node == 'group' or node == 'transform' or node == None):
                var = 0
                for o in range(self._offsetGroups):
                    if 'offset' + `o` in node:
                        var = 1
                assert var, check.error(self, 1, `node`, "Or index out of range!")
            if not (attr == 'tx' or attr == 'ty' or attr == 'tz' or
                    attr == 'rx' or attr == 'ry' or attr == 'rz' or
                    attr == 'sx' or attr == 'sy' or attr == 'sz' or attr == None):
                raise Exception(check.error(self, 1, `attr`))

        #--- lockAttributes
        for d in self._lockAttrs.items():
            if not d[0]:
                break
            assert d[1], check.error(self, 1, `d[1]`)
            if not (d[0] == 'group' or d[0] == 'transform' or d[0] == None):
                var = 0
                for o in range(self._offsetGroups):
                    if 'offset' + `o` in d[0]:
                        var = 1
                assert var, check.error(self, 1, `d[0]`, "Or index out of range!")
            assert isinstance(d[1], list), check.error(self, 3, `d[1]`)

        #--- parent
        if self._parent:
            assert cmds.objExists(self._parent), check.error(self, 0, `self._parent`)
    #END __check_parameters()

    def __check_scene(self):
        #--- check plugin
        plugin_master.PluginSetup(plugin='goe_tools', suffix='py')

        if not self._exists:
            #--- control shape
            composed = self._side + "_" + self._name + "_CTLShape"
            assert not cmds.objExists(composed), check.error(self, 20, `composed`)

        #--- parent
        if self._parent:
            assert cmds.objExists(self._parent), check.error(self, 0, `self._parent`)
    #END __check_scene()

    def __check_existence(self):
        if not self._exists:
            return False
        self.shape = self._side + "_" + self._name + "_CTLShape"
        self.transform = self._side + "_" + self._name + "_CTL"
        self.group = self._side + "_" + self._name + "_GRP"
        if not (cmds.objExists(self.shape) or
                cmds.objExists(self.transform) or
                cmds.objExists(self.group)):
            return False
        if self._offsetGroups:
            #--- check offsetGroups
            for i in range(self._offsetGroups):
                off_name = self._side + "_" + self._name + `i` + "_OFF"
                self.offsets.append(off_name)
                if not cmds.objExists(off_name):
                    return False
        if self._withGimbal:
            #--- check gimbal control
            self.gimbal = self._side + "_" + self._name + "Gimbal_CTL"
            if not cmds.objExists(self.gimbal):
                return False
        return True
    #END __check_existence()

    def __create_control(self):
        composed = self._side + "_" + self._name + "_"
        #--- create top group
        self.group = cmds.createNode('transform', name=composed + "GRP")

        if self._offsetGroups:
            #--- add offsetGroups
            for i in range(self._offsetGroups):
                off_name = self._side + "_" + self._name + `i` + "_OFF"
                off = cmds.createNode('transform', name=off_name)
                self.offsets.append(off)
            for i, off in enumerate(self.offsets):
                j = i + 1
                if not j == len(self.offsets):
                    cmds.parent(self.offsets[i], self.offsets[j])
                else:
                    cmds.parent(off, self.group)
            #--- create control shape and transform with offset groups
            self.transform = cmds.createNode('transform', name=composed + "CTL",
                                             parent=self.offsets[0])
            self.shape = cmds.createNode('goe_locator', name=composed + "CTLShape",
                                         parent=self.transform)
        else:
            #--- create control shape and transform without offset groups
            self.transform = cmds.createNode('transform', name=composed + "CTL",
                                             parent=self.group)
            self.shape = cmds.createNode('goe_locator', name=composed + "CTLShape",
                                         parent=self.transform)

        if self._withGimbal:
            #--- add gimbal control
            gn = self._side + "_" + self._name + "Gimbal_CTL"
            self.gimbal = cmds.createNode('transform', name=gn, parent=self.transform)
            self._gshape = cmds.createNode('goe_locator', name=gn + "Shape",
                                           parent=self.gimbal)
    #END __create_control()

    def __add_attributes(self):
        #--- add CTL tag
        if not cmds.objExists(self.transform + '.CTL'):
            cmds.addAttr(self.transform, longName='CTL', attributeType='bool')
            cmds.setAttr(self.transform + '.CTL', 1, lock=True, keyable=False)

        if self._withGimbal:
            #--- showGimbal
            if not cmds.objExists(self.transform + '.showGimbal'):
                cmds.addAttr(self.transform, longName='showGimbal',
                             attributeType='short', min=0, max=1, defaultValue=0)
                cmds.setAttr(self.transform + '.showGimbal', edit=True,
                             keyable=False, channelBox=True)
    #END __add_attributes()

    def __setup_attributes(self):
        #--- control shape
        cmds.setAttr(self.shape + '.size', self._size)
        cmds.setAttr(self.shape + '.shape', self._shape)
        cmds.setAttr(self.shape + '.orientation', self._orientation)
        cmds.setAttr(self.shape + '.overrideEnabled', 1)
        cmds.setAttr(self.shape + '.overrideColor', self._color)
        for i, axis in enumerate('XYZ'):
            cmds.setAttr(self.shape + '.localPosition' + axis, self._shapeOffset[i])
            cmds.setAttr(self.shape + '.localScale' + axis, self._shapeScale[i])

        #--- position and rotation
        cmds.xform(self.group, translation=self._position, worldSpace=True)
        cmds.xform(self.group, rotation=self._rotation, worldSpace=True)

        #--- rotate order
        value = 0
        if self._rotateOrder == 'yzx':
            value += 1
        elif self._rotateOrder == 'zxy':
            value += 2
        elif self._rotateOrder == 'xzy':
            value += 3
        elif self._rotateOrder == 'yxz':
            value += 4
        elif self._rotateOrder == 'zyx':
            value += 5
        cmds.setAttr(self.transform + '.rotateOrder', value)

        if self._withGimbal:
            #--- gimbal shape
            cmds.setAttr(self._gshape + '.size', self._size / 1.5)
            cmds.setAttr(self._gshape + '.shape', 28)
            cmds.setAttr(self._gshape + '.orientation', self._orientation)
            cmds.connectAttr(self.transform + '.showGimbal', self._gshape + '.v')
    #END __connect_attributes()

    def __parent_setup(self):
        if self._parent:
            #--- parent the top group under the specified parent
            cmds.parent(self.group, self._parent)
    #END __parent_setup()

    def __limit_transforms(self):
        for d in self._limitTransforms:
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

            if not node:
                break

            if node == 'group':
                node = self.group
            elif node == 'transform':
                node = self.transform
            if self._offsetGroups:
                for i in range(self._offsetGroups):
                    if node == 'offset' + `i`:
                        node = self.offsets[i]

            #--- check min and max
            emin, emax = 1, 1
            vmin, vmax = mini, maxi
            if mini == None:
                emin, vmin = 0, -1
                if 'r' in attr:
                    vmin = -45
            if maxi == None:
                emax, vmax = 0, 1
                if 'r' in attr:
                    vmax = 45

            #--- translation
            if attr == 'tx':
                cmds.transformLimits(node, tx=(vmin, vmax), etx=(emin, emax))
            elif attr == 'ty':
                cmds.transformLimits(node, ty=(vmin, vmax), ety=(emin, emax))
            elif attr == 'tz':
                cmds.transformLimits(node, tz=(vmin, vmax), etz=(emin, emax))
            #--- rotation
            elif attr == 'rx':
                cmds.transformLimits(node, rx=(vmin, vmax), erx=(emin, emax))
            elif attr == 'ry':
                cmds.transformLimits(node, ry=(vmin, vmax), ery=(emin, emax))
            elif attr == 'rz':
                cmds.transformLimits(node, rz=(vmin, vmax), erz=(emin, emax))
            #--- scale
            elif attr == 'sx':
                cmds.transformLimits(node, sx=(vmin, vmax), esx=(emin, emax))
            elif attr == 'sy':
                cmds.transformLimits(node, sy=(vmin, vmax), esy=(emin, emax))
            elif attr == 'sz':
                cmds.transformLimits(node, sz=(vmin, vmax), esz=(emin, emax))
    #END __limit_transforms()

    def __lock_attributes(self):
        if not self._lockAttrs:
            return
        for d in self._lockAttrs.items():
            #--- get the proper nodes
            node = None
            if not d[0]:
                break
            if d[0] == 'group':
                node = self.group
            elif d[0] == 'transform':
                node = self.transform
            if self._offsetGroups:
                for i in range(self._offsetGroups):
                    if d[0] == 'offset' + `i`:
                        node = self.offsets[i]
            #--- lock and hide attributes
            for i in d[1]:
                if i == 't' or i == 'r' or i == 's':
                    for axis in 'xyz':
                        cmds.setAttr(node + '.' + i + axis, lock=True, keyable=False)
                else:
                    cmds.setAttr(node + '.' + i, lock=True, keyable=False)
    #END __lock_attributes()

    def __cleanup(self):
        if self._lockGroups:
            attr = ['shearXY', 'shearXZ', 'shearYZ', 'rotateOrder', 'rotateAxisX',
                    'rotateAxisY', 'rotateAxisZ', 'inheritsTransform']
            if self.offsets:
                #--- lock offsets
                for i in self.offsets:
                    attrs = cmds.listAttr(i, keyable=True)
                    if attrs:
                        for j in attr:
                            attrs.append(j)
                        for a in attrs:
                            cmds.setAttr(i + '.' + a, lock=True, keyable=False)
                    attribute.lock_n_hide(i, ['t', 'r'], True)

            #--- lock group
            attrs = cmds.listAttr(self.group, keyable=True)
            for i in attr:
                attrs.append(i)
            if attrs:
                for a in attrs:
                    cmds.setAttr(self.group + '.' + a, lock=True, keyable=False)

            #--- lock transform
            attrs = ['sx', 'sy', 'sz', 'v']
            for i in attr:
                attrs.append(i)
            for a in attrs:
                cmds.setAttr(self.transform + '.' + a, lock=True, keyable=False)
            cmds.setAttr(self.shape + '.ihi', 0)

            #--- lock shape
            attrs = cmds.listAttr(self.shape, channelBox=True)
            if attrs:
                for a in attrs:
                    cmds.setAttr(self.shape + '.' + a, lock=True, keyable=False)
                    cmds.setAttr(self.shape + '.' + a, channelBox=False)
                cmds.setAttr(self.shape + '.ihi', 0)

            if self._withGimbal:
                #--- lock gimbal
                attrs = ['sx', 'sy', 'sz', 'v']
                for i in attr:
                    attrs.append(i)
                for a in attrs:
                    cmds.setAttr(self.gimbal + '.' + a, lock=True, keyable=False)
                cmds.setAttr(self._gshape + '.ihi', 0)

                #--- lock gimbal shape
                attrs = cmds.listAttr(self._gshape, channelBox=True)
                if attrs:
                    for a in attrs:
                        cmds.setAttr(self._gshape + '.' + a, lock=True, keyable=False)
                        cmds.setAttr(self._gshape + '.' + a, channelBox=False)
                    cmds.setAttr(self._gshape + '.ihi', 0)
        cmds.select(clear=True)
    #END __cleanup()

    def __create(self):
        #--- check parameters
        self.__check_parameters()
        #--- check scene
        self.__check_scene()
        #--- check existence
        if self.__check_existence():
            return
        #--- create control
        self.__create_control()
        #--- add attributes
        self.__add_attributes()
        #--- setup attributes
        self.__setup_attributes()
        #--- parent setup
        self.__parent_setup()
        #--- limit transforms
        self.__limit_transforms()
        #--- lock_attributes
        self.__lock_attributes()
        #--- cleanup
        self.__cleanup()
    #END __create()
#END Control()
