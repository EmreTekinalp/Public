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
        plg = cmds.createNode(self.name)
        for i in range(10):
            obja = cmds.polyCube()[0]
            objb = cmds.polySphere()[0]
            cmds.connectAttr('%s.worldMatrix' % obja,
                             '%s.input[%d].inMatrix' % (plg, i))
            cmds.connectAttr('%s.output[%d].outTranslate' % (plg, i),
                             '%s.t' % objb)
            cmds.connectAttr('%s.output[%d].outRotate' % (plg, i),
                             '%s.r' % objb)
            #cmds.connectAttr('%s.output[0].outScale' % plg, '%s.s' % objb)
            cmds.setAttr('%s.input[%d].constraint' % (plg, i), 2)
    # END _setup_plugin()
# END Plug()

Plug("multiconstraint", "multiConstraint")
