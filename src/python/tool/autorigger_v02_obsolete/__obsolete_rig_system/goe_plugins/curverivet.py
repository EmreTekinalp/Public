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
    def __init__(self, plugin="curveRivetNode"):
        super(RivetNode, self).__init__(plugin=plugin, suffix="so",
                                        update=True, info=True)
        #--- args
        self._plugin = plugin

        #--- methods
        self.__create()
    #END __init__()

    def __setup_plugin(self):
        rivet = cmds.createNode(self._plugin)
        loc = cmds.spaceLocator()[0]
        obj = cmds.curve(point=[[1, 0, 0], [2, 0, 1], [4, 1, 4], [7, 3, 6]])
        shape = cmds.listRelatives(obj, allDescendents=True)[0]
        cmds.connectAttr(obj + ".worldMatrix", rivet + ".inMatrix")
        cmds.connectAttr(shape + ".local", rivet + ".inCurve")
        cmds.connectAttr(rivet + ".outTranslate", loc + ".translate")
        cmds.connectAttr(rivet + ".outRotate", loc + ".rotate")
    #END __setup_plugin()

    def __create(self):
        self.__setup_plugin()
    #END __create()
#END RivetNode()

RivetNode()
