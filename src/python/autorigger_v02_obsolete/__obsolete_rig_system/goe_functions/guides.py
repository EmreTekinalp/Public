'''
@author:  etekinalp
@date:    Sep 1, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module creates the guide controls
'''


from maya import cmds

from goe_functions import check, data


class SetupRoot(object):
    def __init__(self, currentFile):
        """
        @type  currentFile: buildin - type
        @param currentFile: specify only __file__
        """
        #--- args
        self._currentFile = currentFile

        #--- vars
        self.assetInfo = list()
        self.root = None

        #--- methods
        self.__create()
    #END __init__()

    def __check_parameters(self):
        #--- currentFile
        assert self._currentFile, check.error(self, 1, `self._currentFile`)
        #--- assetInfo
        self.assetInfo = data.asset_info(self._currentFile)
        assert self.assetInfo, check.error(self, 1, `self.assetInfo`)
        assert len(self.assetInfo) == 4, check.error(self, 21, `self.assetInfo`)
    #END __check_parameters()

    def __create_root(self):
        #--- create guide root
        self.root = "GUIDE_ROOT"
        if cmds.objExists(self.root):
            return
        self.root = cmds.createNode("transform", name=self.root)
    #END __create_root()

    def __add_root_attributes(self):
        #--- globalScale
        if not cmds.objExists(self.root + ".globalScale"):
            cmds.addAttr(self.root, longName="globalScale",
                         min=0, defaultValue=1, attributeType='float')
            cmds.setAttr(self.root + '.globalScale',
                         edit=True, keyable=False, channelBox=True)
        #--- project
        if not cmds.objExists(self.root + ".project"):
            cmds.addAttr(self.root, longName="project", dataType='string')
            cmds.setAttr(self.root + '.project', self.assetInfo[0],
                         type='string', lock=True)
        #--- assetType
        if not cmds.objExists(self.root + ".assetType"):
            cmds.addAttr(self.root, longName="assetType", dataType='string')
            cmds.setAttr(self.root + '.assetType', self.assetInfo[1],
                         type='string', lock=True)
        #--- assetResolution
        if not cmds.objExists(self.root + ".assetResolution"):
            cmds.addAttr(self.root, longName="assetResolution", dataType='string')
            cmds.setAttr(self.root + '.assetResolution', self.assetInfo[2],
                         type='string', lock=True)
        #--- assetName
        if not cmds.objExists(self.root + ".assetName"):
            cmds.addAttr(self.root, longName="assetName", dataType='string')
            cmds.setAttr(self.root + '.assetName', self.assetInfo[3],
                         type='string', lock=True)
    #END __add_root_attributes()

    def __setup_root(self):
        #--- setup guide root
        attr = ['shearXY', 'shearXZ', 'shearYZ', 'rotateOrder', 'rotateAxisX',
                'rotateAxisY', 'rotateAxisZ', 'inheritsTransform']
        for axis in 'xyz':
            cmds.connectAttr(self.root + ".globalScale", self.root + ".s" + axis)
            cmds.setAttr(self.root + '.t' + axis, lock=True, keyable=False)
            cmds.setAttr(self.root + '.r' + axis, lock=True, keyable=False)
            cmds.setAttr(self.root + '.s' + axis, lock=True, keyable=False)
        cmds.setAttr(self.root + '.v', lock=True, keyable=False)
        for a in attr:
            cmds.setAttr(self.root + '.' + a, lock=True, keyable=False)
    #END __setup_root()

    def __create(self):
        #--- check the parameters
        self.__check_parameters()
        #--- create guide root
        self.__create_root()
        #--- add guide root attributes
        self.__add_root_attributes()
        #--- setup guide root
        self.__setup_root()
    #END __create()
#END SetupRoot()
