'''
@author:  etekinalp
@date:    Aug 26, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module creates a GOE_mirror node
'''


from maya import cmds, mel
from goe_plugins import plugin_master
reload(plugin_master)


class Curve(plugin_master.PluginSetup):
    def __init__(self, plugin="curve", length=10):
        super(Curve, self).__init__(plugin=plugin, suffix="so",
                                    update=True, info=True)
        # args
        self._plugin = plugin
        self.length = length

        # methods
        self.__create()
    # END __init__()

    def __setup_plugin(self):
        # circle setup
        """
        mesh = cmds.polyTorus()[0]
        crv = cmds.circle(nr=[0, 1, 0])[0]
        shape = cmds.listRelatives(crv, allDescendents=True)[0]
        """

        # curve setup
        mesh = cmds.polyCylinder(r=1, h=9, sh=10, sx=10)[0]
        cmds.setAttr('%s.rx' % mesh, 90)
        cmds.setAttr('%s.tz' % mesh, 4.5)
        mel.eval('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1;')
        mel.eval('DeleteHistory')
        plug = cmds.deformer(mesh, type='etcurve')[0]
        points = [[0, 0, p] for p in range(self.length)]
        crv = cmds.curve(point=points, d=3)
        shape = cmds.listRelatives(crv, allDescendents=True)[0]

        cmds.connectAttr(mesh + ".worldMatrix", plug + ".inMatrix")
        cmds.connectAttr(crv + ".worldMatrix", plug + ".inCurveMatrix")
        cmds.connectAttr(shape + ".worldSpace", plug + ".inCurve")
        for i in range(self.length):
            cmds.select(clear=True)
            jnt = cmds.joint()
            cmds.connectAttr(plug + ".outTranslate[" + str(i) + "]",
                             jnt + ".translate")
            cmds.connectAttr(plug + ".outRotate[" + str(i) + "]",
                             jnt + ".rotate")
        cmds.setAttr('%s.initUpVecX' % plug, -1)
    # END __setup_plugin()

    def __create(self):
        self.__setup_plugin()
    # END __create()
# END Curve()

Curve(length=10)
