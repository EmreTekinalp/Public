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

    def __init__(self, plugin, name):
        """
        @param plugin(string): Plugin name without .so or .py suffix
        @param name(string): Name of plugin call
        """

        super(Plug, self).__init__(plugin, 'so', True, True)

        # args
        self.plugin = plugin
        self.name = name

        # methods
        self._setup_plugin()
    # END __init__()

    def _setup_plugin(self):
        cmds.createNode(self.name)
    # END _setup_plugin()
# END Plug()

Plug("curveramp", "curveRamp")
