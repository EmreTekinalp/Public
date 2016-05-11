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

    def __init__(self, plugin, name):
        """
        @param plugin(string): Plugin name without .so or .py suffix
        @param length(uint): Length of curve and mesh cylinder
        """

        super(Plug, self).__init__(plugin, 'so', True, True)

        # args
        self.name = name

        # methods
        self._setup_plugin()
    # END __init__()

    def _setup_plugin(self):
        collider = cmds.polySphere()[0]
        target = cmds.polySphere(subdivisionsAxis=20,
                                 subdivisionsHeight=20)[0]
#         target = cmds.polyCube()
        plugin = cmds.deformer(target, type=self.name)[0]
        cmds.connectAttr('%s.worldInverseMatrix' % collider,
                         '%s.volumeInverseMatrix' % plugin)
    # END _setup_plugin()
# END Plug()

Plug("volumenode", 'volume')
