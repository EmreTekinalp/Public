'''
@author:  etekinalp
@date:    Aug 26, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module setups a plugin
'''


from maya import cmds, mel
from goe_plugins import plugin_master
reload(plugin_master)


class Plug(plugin_master.PluginSetup):
    """
    Subclass PluginSetup and setup the plugin test environment.
    """

    def __init__(self, plugin):
        """
        @param plugin(string): Plugin name without .so or .py suffix
        @param length(uint): Length of curve and mesh cylinder
        """

        super(Plug, self).__init__(plugin, 'so', True, True)

        # args
        self.plugin = plugin

        # methods
        self._setup_plugin()
    # END __init__()

    def _setup_plugin(self):
        initmesh = cmds.polySphere(n="initMesh")[0]
        blendmesh = cmds.polySphere(n="blendMesh")[0]
        plug = cmds.deformer(initmesh, type=self.plugin)[0]
        cmds.connectAttr('%sShape.worldMesh' % blendmesh, '%s.blendMesh' % plug)
    # END _setup_plugin()
# END Plug()

Plug("coloratpoint")
