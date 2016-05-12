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
        collider1 = cmds.spaceLocator()[0]
        collider2 = cmds.spaceLocator()[0]
        plug = cmds.createNode(self.plugin)
        cmds.connectAttr('%s.worldMatrix' % collider1, '%s.inCollider[0]' % plug)
        cmds.connectAttr('%s.worldMatrix' % collider2, '%s.inCollider[1]' % plug)
        for num in range(3):
            volume = cmds.listRelatives(cmds.createNode('implicitSphere'), p=True)[0]
            obj = cmds.polySphere()[0]
            cmds.connectAttr('%s.worldInverseMatrix' % volume, '%s.inVolume[%s]' % (plug, num))
            cmds.connectAttr('%s.output[%s]' % (plug, num), '%s.ty' % obj)
    # END _setup_plugin()
# END Plug()

Plug("volumePushCollider")
