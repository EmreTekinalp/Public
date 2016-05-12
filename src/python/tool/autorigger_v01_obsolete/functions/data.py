'''
Created on 16.09.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: The data class for the guides and shapes
'''

import os, json
from maya import cmds
from fundamentals import attribute, system
from functions import skinweight
reload(attribute)
reload(skinweight)
reload(system)


class Data(system.DataSystem):
    """
    This class handles all the data which will be created to use the autoRigger.
    It contains saving and loading data. You can also choose between json and
    xml files.
    """

    def __init__(self):
        ########################################################################
        super(Data, self).__init__()
    #END def __init__()

    def save(self, dirName = None, assetName = None, dataType = None):        
        #--- this method saves the data
        attr = attribute.Attribute()
        sel = cmds.ls('*_GCTL', type = 'transform')
        data = list()
        shape = list()
        locator = list()
        if dataType == 'guides':
            #--- save the guides
            for i in sel:
                list_attr = cmds.listAttr(i, keyable = True, visible = True)
                value_list = []
                for attrs in list_attr:
                    value = attr.getAttr(node = i, attribute = attrs)
                    result = (str(i) + '.' + str(attrs), str(value))
                    value_list.append(result)
                data.append(value_list)
            self.write_data(dirName = dirName,                             
                            folder = 'data', 
                            fileName = assetName,
                            obj = data)
            print 'GuideData saved!'

        elif dataType == 'weights':
            #--- get the skinClusters, meshes and shapes            
            w = skinweight.Weights()
            skins = w.get_skin_weights()
            folder = os.path.join('data', dirName)
            #--- create a new character folder if it does not exist
            self.new_data_folder(folder=folder, dirName=assetName)
            for mesh, shape, skin in zip(skins[0], skins[1], skins[2]):
                data_path = os.path.join(self.root, 'data', dirName, assetName)
                file_name = mesh + '.xml'
                cmds.deformerWeights(file_name, path=data_path, shape=shape, 
                                     export=True, deformer=skin)
            print 'WeightData saved'

        elif dataType == 'locators':
            #--- save all the information provided by the custom locators
            sel = cmds.ls('*_*CTLShape')
            for i in sel:
                obj_type = cmds.nodeType(i)
                if obj_type == 'eLocator':
                    attrs = cmds.listAttr(i, locked=True, unlocked=True)
                    for attr in attrs:
                        if not 'localScale' in attr:
                            if (attr == 'size' or attr == 'shape' or 
                                attr == 'orientation' or attr =='width' or
                                attr == 'localPositionX' or 
                                attr == 'localPositionY' or
                                attr == 'localPositionZ'):
                                value = cmds.getAttr(i + '.' + attr)
                                result = [i, attr, value]
                                locator.append(result)                        
                else:
                    raise Exception('There is no eLocator shape of this node!')
            self.write_data(dirName = dirName,            
                            folder = 'data', 
                            fileName = assetName,
                            obj = locator)
            print 'LocatorData saved!'

        elif dataType == 'shapes':
            #--- save all curve shape information
            for i in sel:
                shape_type = cmds.listRelatives(i, allDescendents = True, 
                                                shapes = True)
                obj_type = cmds.objectType(shape_type)
                if obj_type == 'nurbsCurve' or obj_type == 'nurbsSurface':
                    curve = cmds.ls(i + '.cv[*]', flatten = True)
                    for cv in curve:
                        pos = cmds.xform(cv, query = True, 
                                         translation = True, 
                                         worldSpace = True)
                        result = [i, pos]
                        shape.append(result)
                elif obj_type == 'mesh':
                    vertices = cmds.ls(i + '.vtx[*]', flatten = True)
                    for vtx in vertices:
                        pos = cmds.xform(vtx, query = True, 
                                         translation = True, 
                                         worldSpace = True)
                        result = [i, pos]
                        shape.append(result)
                else:
                    raise Exception('There is no component mode of this node!')
            self.write_data(dirName = dirName,                             
                            folder = 'data', 
                            fileName = assetName,
                            obj = shape)                
            print 'ShapeData saved!'
    #END def save()

    def load(self, dirName='locatorData', assetName=None, dataType='locator'):        
        #--- this method loads the data
        attr = attribute.Attribute()
        if dataType == 'attribute':
            result = self.read_data(dirName = dirName, 
                                    folder = 'data', 
                                    fileName = assetName)
            for i in result:
                if cmds.objExists(i.split(',')[0]):
                   attr.setAttr(node = i.split(',')[0].split('.')[0], 
                                attribute = i.split(',')[0].split('.')[1], 
                                value = i.split(', ')[1])

        elif dataType == 'locator':
            if assetName:
                result = self.read_data(dirName = dirName, 
                                        folder = 'data', 
                                        fileName = assetName)
                if result:
                    for obj in result:
                        ctl = obj[0]
                        attr = obj[1]
                        value = obj[2]
                        #--- set locatorData
                        if cmds.objExists(ctl + '.' + str(attr)):
                            cmds.setAttr(ctl + '.' + str(attr), lock=False)
                            cmds.setAttr(ctl + '.' + str(attr), value, 
                                         lock=True, keyable=False, channelBox=False)
                else:
                    raise Exception('There is no locator data!')
            else:
                raise Exception('There is no locator data of ' + assetName + '!')
            print 'LocatorData loaded!'

        elif dataType == 'weights':
            #--- get the data path
            data_path = os.path.join(self.root, 'data', dirName, assetName)
            if os.path.exists(data_path):
                #--- get the skinClusters, meshes and shapes            
                w = skinweight.Weights()
                skins = w.get_skin_weights()
                skin_weights = list()
                for mesh in skins[0]:
                    #--- skin the meshes
                    skin = cmds.skinCluster(mesh,skins[3], toSelectedBones=True)
                    skin_weights.append(skin[0])
                #--- list all xml files in this folder
                files = os.listdir(data_path)
                for file in files:
                    mesh_name = file.split('.')[0]
                    for mesh, shape, skin in zip(skins[0], skins[1], skin_weights):
                        if mesh_name == mesh:
                            try:
                                #--- import the new weights
                                cmds.deformerWeights(file, im=True, method='index',
                                                     deformer=skin,
                                                     path=data_path,
                                                     shape=shape)
                                cmds.skinCluster(skin, edit=True, 
                                                 forceNormalizeWeights=True)
                            except:
                                pass
                print 'WeightData loaded!'
    #END def load()

    def load_guide(self, dirName = None, assetName = None):        
        #--- this method loads the guide data
        attr = attribute.Attribute()
        dirName = 'guideData'
        if assetName:
            result = self.read_data(dirName = dirName, 
                                    folder = 'data', 
                                    fileName = assetName)
            if result:
                for obj in result:
                    for i in obj:
                        ctl = i[0].split('.')[0]
                        att = i[0].split('.')[-1]
                        val = i[1]
                        if 'translate' in att:
                            if cmds.objExists(ctl):
                                if cmds.objExists(i[0]):
                                    attr.setAttr(node = ctl, 
                                                 attribute = att, 
                                                 value = val)
                        elif 'rotate' in att:
                            if cmds.objExists(ctl):
                                if cmds.objExists(i[0]):
                                    attr.setAttr(node = ctl, 
                                                 attribute = att, 
                                                 value = val)
            else:
                raise Exception('There is no guide data!')
        else:
            raise Exception('There is no guide data of ' + assetName + '!')
        print 'Guides loaded!'
    #END def load_guide()
#END class Data()

#Data().save(dirName = 'guideData', assetName = 'ACHILLES', dataType = 'guides')
#Data().save(dirName = 'shapes', assetName = 'ctl_shape16_foot', dataType = 'shape')
#Data().load_guide(dirName = 'guideData', assetName = 'ACHILLES')