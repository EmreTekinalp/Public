'''
@author:  etekinalp
@date:    Aug 26, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module creates a GOE_mirror node
'''


from maya import cmds, mel
from goe_plugins import plugin_master
reload(plugin_master)


class Plug(plugin_master.PluginSetup):
    """
    Subclass PluginSetup and setup the plugin test environment.
    """

    def __init__(self, plugin, length):
        """
        @param plugin(string): Plugin name without .so or .py suffix
        @param length(uint): Length of curve and mesh cylinder
        """

        super(Plug, self).__init__(plugin, 'so', True, True)

        # args
        self.plugin = plugin
        self.length = length

        # methods
        self._setup_plugin()
    # END __init__()

    def _setup_plugin(self):
        # circle setup
        # mesh = cmds.polyTorus()[0]
        # crv = cmds.circle(nr=[0, 1, 0])[0]

        # curve setup
        mesh = cmds.polyCylinder(r=1, h=12, sh=50, sx=10)[0]
        cmds.setAttr('%s.rz' % mesh, 90)
        cmds.setAttr('%s.tx' % mesh, 6)
        mel.eval('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1;')
        mel.eval('DeleteHistory')
        points = [[n, 0, 0] for n in range(self.length)]
        crv = cmds.curve(n='C_driven_CRV', p=points, d=3)
        plug = cmds.deformer(crv, type=self.plugin)[0]
        driver = cmds.duplicate(crv, n='C_dirver_CRV')[0]
        bsp = cmds.blendShape(driver, crv, weight=[0, 1], foc=True, origin='world')
        #cmds.connectAttr('%s.worldSpace' % driver, '%s.inCurve' % plug)
        #cmds.connectAttr('%s.worldMatrix' % driver, '%s.inCurveMatrix' % plug)
    # END _setup_plugin()
# END Plug()

Plug("ecurve", 13)
