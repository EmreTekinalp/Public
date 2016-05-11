'''
@author:  etekinalp
@date:    Aug 26, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module creates a GOE_mirror node
'''


from maya import cmds
from goe_plugins import plugin_master
reload(plugin_master)


class RivetNode(plugin_master.PluginSetup):
    def __init__(self, plugin="nurbsRivetNode"):
        super(RivetNode, self).__init__(plugin=plugin, suffix="so",
                                        update=True, info=True)
        #--- args
        self._plugin = plugin

        #--- methods
        self.__create()
    #END __init__()

    def __setup_plugin(self):
        rivet = cmds.createNode(self._plugin)
        obj = cmds.sphere()[0]
        shape = cmds.listRelatives(obj, allDescendents=True)[0]
        cmds.connectAttr(shape + ".local", rivet + ".inSurface")
        cmds.connectAttr(obj + ".worldMatrix", rivet + ".inMatrix")
        for num in range(12):
            loc = cmds.spaceLocator()[0]
            cmds.setAttr(rivet + ".parameterUV[%s].parameterU" % num, 0.5)
            cmds.setAttr(rivet + ".parameterUV[%s].parameterV" % num, 0.0)
            cmds.connectAttr(rivet + ".outTranslate[%s]" % num, loc + ".translate")
            cmds.connectAttr(rivet + ".outRotate[%s]" % num, loc + ".rotate")
    #END __setup_plugin()

    def __create(self):
        self.__setup_plugin()
    #END __create()
#END RivetNode()

RivetNode()
