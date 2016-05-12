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

    def __init__(self, plugin, name, length):
        """
        @param plugin(string): Plugin name without .so or .py suffix
        @param length(uint): Length of curve and mesh cylinder
        """

        super(Plug, self).__init__(plugin, 'so', True, True)

        # args
        self.plugin = plugin
        self.name = name
        self.length = length

        # methods
        self._setup_plugin()
    # END __init__()

    def _setup_plugin(self):
        plug = cmds.createNode(self.name)
        for num in range(self.length):
            trn = 'C_shirtVol%s_TRN' % num
            cmds.connectAttr('%s.outTranslate[%s]' % (plug, num), '%s.s' % trn)
        # end for
    # END _setup_plugin()
# END Plug()

# Plug("rampoffset", "rampOffset", 48)

plug = cmds.createNode('rampOffset')
for num in range(48):
    trn = 'C_shirtVol%s_TRN' % num
    cmds.connectAttr('%s.outTranslate[%s]' % (plug, num), '%s.s' % trn)
# end for
