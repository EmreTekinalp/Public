'''
@author:  etekinalp
@date:    Aug 26, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module creates a GOE_mirror node
'''


from maya import cmds
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
        points = [[n, 0, 0] for n in range(self.length)]
        crv = cmds.curve(n='C_test_CRV', p=points)
        shp = cmds.rename(cmds.listRelatives(crv, ad=True)[0], '%sShape' % crv)
#         geo = cmds.polyCylinder(n='C_test_GEO', ax=[1, 0, 0], h=points[-1][0],
#                                 sy=self.length * 2, sz=1, ch=False)[0]
        geo = cmds.polySphere(n='C_test_GEO', ch=False)[0]
        cmds.setAttr('%s.tx' % crv, - (points[-1][0] / 2.0))
        wire = cmds.deformer(geo, type=self.plugin)[0]
        cmds.connectAttr('%s.worldMatrix' % shp, '%s.inCurveMatrix' % wire)
        cmds.connectAttr('%s.worldSpace' % shp, '%s.inCurve' % wire)
    # END _setup_plugin()
# END Plug()

Plug("etWireDeformer", 10)
