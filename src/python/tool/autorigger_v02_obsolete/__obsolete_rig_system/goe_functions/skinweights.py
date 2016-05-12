'''
Created on Nov 16, 2014

@author: Emre
'''

from maya import cmds


class SkinWeights(object):
    """ Export and import skinweights using maya's deformerWeights cmds """
    def __init__(self, shape=None):
        #--- args
        self.shape = shape

        #--- vars
        self.skincluster = None

        #--- methods
        self.__check_parameters()
        self.__get_skincluster()
    #END __init__()

    def __check_parameters(self):
        """ Check the given parameters in the creator """
        #--- shape
        assert self.shape, "SkinClusterIO: No shape has been specified!"
        assert cmds.objExists(self.shape), ("SkinClusterIO: Specified shape "
                                            "does not exist in the scene!")
    #END __check_parameters()

    def __get_skincluster(self):
        """ Get the skinCluster out of the shape """
        history = cmds.listHistory(self.shape)
        if not history:
            return
        self.skincluster = [i for i in history if cmds.nodeType(i) == 'skinCluster']
        if not self.skincluster:
            self.skincluster = None
            return
        else:
            self.skincluster = self.skincluster[0]
    #END __get_skincluster()

    def export_weights(self, filename=None, filepath=None):
        """ Export the weights of the given shape """
        if not self.skincluster:
            return
        cmds.deformerWeights(filename, export=True, deformer=self.skincluster,
                             path=filepath)
    #END export_weights()

    def import_weights(self, filename=None, filepath=None):
        """ Import the weights of the given shape """
        joints = cmds.ls(type='joint')
        if not self.skincluster:
            self.skincluster = cmds.skinCluster(joints, self.shape, toSelectedBones=True)[0]
        bla = cmds.deformerWeights(filename, im=True, method="index",
                                   deformer=self.skincluster, path=filepath)
        print bla
#         cmds.skinCluster(self.skincluster, edit=True, joints, forceNormalizeWeights=True, removeUnusedInfluence=True)
#         cmds.skinCluster(self.skincluster, edit=True, joints, )
    #END import_weights()
#END SkinWeights()
