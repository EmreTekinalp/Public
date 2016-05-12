'''
@author:  etekinalp
@date:    Nov 16, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module contains the class to export and import weights
'''

from maya import cmds, OpenMaya, OpenMayaAnim


class Weights(object):
    """ Get the weights of the specified shape """
    def __init__(self, shape=None):
        #--- args
        self.shape = shape

        #--- methods
        self.__create()
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

    def __get_geometry_components(self):
        """ Get the dagpath and the components of the geometry """
        mselmembers = OpenMaya.MSelectionList()
        fnset = OpenMaya.MFnSet(self.fnSkinCluster.deformerSet())
        components = OpenMaya.MObject()
        fnset.getMembers(mselmembers, False)
        dagpath = OpenMaya.MDagPath()
        mselmembers.getDagPath(0, dagpath, components)
        return dagpath, components
    #END __get_geometry_components()

    def __get_current_weights(self, dagpath, components):
        """ Get the current weights """
        weights = OpenMaya.MDoubleArray()
        util = OpenMaya.MScriptUtil()
        util.createFromInt(0)
        puint = util.asUintPtr()
        self.fnSkinCluster.getWeights(dagpath, components, weights, puint)
        return weights
    #END __get_current_weights()

    def __get_influence_weights(self, dagpath, components):
        """ Get the influence weights of the specified skincluster """
        weights = self.__get_current_weights(dagpath, components)

        dagPathArray = OpenMaya.MDagPathArray()
        numInfluences = self.fnSkinCluster.influenceObjects(dagPathArray)
        influencePerComponent = weights.length() / dagPathArray.length()

        for ii in range(dagPathArray.length()):
            joint = dagPathArray[ii].partialPathName()
            value = [weights[jj * numInfluences + ii] for jj in range(influencePerComponent)]
            self.data['weights'][joint] = value
    #END __get_influence_weights()

    def __get_blend_weights(self, dagpath, components):
        """ Get the blend weights of the specified skincluster """
        blendWeights = OpenMaya.MDoubleArray()
        self.fnSkinCluster.getBlendWeights(dagpath, components, blendWeights)
        self.data['blendWeights'] = [blendWeights[i] for i in range(blendWeights.length())]
    #END __get_blend_weights()

    def __set_influence_weights(self, dagpath, components):
        """ Set the influence weights for the specified skincluster """
        weights = self.__get_current_weights(dagpath, components)

        dagPathArray = OpenMaya.MDagPathArray()
        numInfluences = self.fnSkinCluster.influenceObjects(dagPathArray)
        influencePerComponent = weights.length() / numInfluences

        unusedImport = list()
        noMatch = [dagPathArray[ii].partialPathName() for ii in range(dagPathArray.length())]

        for joint, weight in self.data['weights'].items():
            for i in range(dagPathArray.length()):
                influenceName = dagPathArray[i].partialPathName()
                if influenceName == joint:
                    for j in range(influencePerComponent):
                        weights.set(weight[j], j * numInfluences + i)
                    noMatch.remove(influenceName)
                    break
                else:
                    unusedImport.append(joint)

        influencedIndices = OpenMaya.MIntArray(numInfluences)
        for i in range(numInfluences):
            influencedIndices.set(i, i)
        self.fnSkinCluster.setWeights(dagpath, components, influencedIndices, weights, False)
    #END __set_influence_weights()

    def __set_blend_weights(self, dagpath, components):
        """ Set the blend weights for the specified skincluster """
        blendWeights = OpenMaya.MDoubleArray(len(self.data['blendWeights']))
        for i, w in enumerate(self.data['blendWeights']):
            blendWeights.set(w, i)
        self.fnSkinCluster.setBlendWeights(dagpath, components, blendWeights)
    #END __get_blend_weights()

    def get_data(self):
        """ Get the data to export """
        if not self.skincluster:
            return
        msel = OpenMaya.MSelectionList()
        msel.add(self.skincluster)
        mobj = OpenMaya.MObject()
        msel.getDependNode(0, mobj)
        self.fnSkinCluster = OpenMayaAnim.MFnSkinCluster(mobj)

        #--- create data
        self.data = {'weights': {},
                     'blendWeights': [],
                     'skinCluster': self.skincluster}
        for attr in ['skinningMethod',
                     'normalizeWeights',
                     'maintainMaxInfluences',
                     'maxInfluences',
                     'useComponents',
                     'deformUserNormals']:
            self.data[attr] = cmds.getAttr(self.skincluster + '.' + attr)

        #--- get geometry components
        dagpath, components = self.__get_geometry_components()
        #--- get the influence weights
        self.__get_influence_weights(dagpath, components)
        #--- get the blend weights
        self.__get_blend_weights(dagpath, components)

        return self.data
    #END get_data()

    def set_data(self, data):
        """ Set the data from import """
        self.data = data
        if not self.skincluster:
            self.skincluster = cmds.skinCluster(self.data['weights'].keys(),
                                                self.shape, toSelectedBones=True,
                                                normalizeWeights=2,
                                                name=self.data['skinCluster'])[0]
        msel = OpenMaya.MSelectionList()
        msel.add(self.skincluster)
        mobj = OpenMaya.MObject()
        msel.getDependNode(0, mobj)
        self.fnSkinCluster = OpenMayaAnim.MFnSkinCluster(mobj)

        for attr in ['skinningMethod',
                     'normalizeWeights',
                     'maintainMaxInfluences',
                     'maxInfluences',
                     'useComponents',
                     'deformUserNormals']:
            cmds.setAttr(self.skincluster + '.' + attr, self.data[attr])

        #--- set geometry components
        dagpath, components = self.__get_geometry_components()
        #--- set the influence weights
        self.__set_influence_weights(dagpath, components)
        #--- set the blend weights
        self.__set_blend_weights(dagpath, components)
    #END set_data()

    def __create(self):
        """ Call methods by creation time """
        #--- check parameters
        self.__check_parameters()
        #--- get skincluster()
        self.__get_skincluster()
    #END __create()
#END Weights()
