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
    def __init__(self, plugin="rivetNode"):
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
        obj = cmds.polySphere()
        shape = cmds.listRelatives(obj[0], allDescendents=True)[0]
        cmds.connectAttr(obj[0] + ".worldMatrix", rivet + ".inMatrix")
        cmds.connectAttr(shape + ".worldMesh", rivet + ".inMesh")
        cmds.connectAttr(rivet + ".outTranslate", loc + ".translate")
        cmds.connectAttr(rivet + ".outRotate", loc + ".rotate")
    #END __setup_plugin()

    def __create(self):
        self.__setup_plugin()
    #END __create()
#END RivetNode()

RivetNode()
