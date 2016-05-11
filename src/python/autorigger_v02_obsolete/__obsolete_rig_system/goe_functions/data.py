'''
@author:  etekinalp
@date:    Sep 4, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module deals with data handling
'''


import os
import json

from maya import cmds
from goe_functions import check, generator, weights

reload(weights)
reload(generator)


def asset_info(currentFile=None):
    assert currentFile, "asset_info: Please specify __file__ as currentFile!"
    #--- get paths
    current_path = os.path.realpath(currentFile)
    build_path = os.path.dirname(current_path)
    asset_path = os.path.dirname(build_path)
    type_path = os.path.dirname(asset_path)
    project_path = os.path.dirname(type_path)

    #--- filter the basenames
    asset_res = os.path.basename(build_path).split('build_')[1]
    asset_name = os.path.basename(asset_path)
    asset_type = os.path.basename(type_path)
    project = os.path.basename(project_path)

    return [project, asset_type, asset_res, asset_name]
#END asset_info()


class Data(object):
    def __init__(self,
                 project=None,
                 assetType=None,
                 assetRes=None,
                 assetName=None):
        """
        @type  project: string
        @param project: specify a project name, it will be created by non-existence.

        @type  assetType: string
        @param assetType: valid types are 'characters', 'props' or 'sets'.

        @type  assetRes: string
        @param assetmethodsRes: specify the resolution of the asset.

        @type  assetName: string
        @param assetName: specify the name of the asset.
        """

        #--- args
        self._project = project
        self._assetType = assetType
        self._assetRes = assetRes
        self._assetName = assetName

        #--- vars
        self.path = None
        self.build_path = None
        self.project_path = None
        self.asset_type_path = None
        self.asset_name_path = None

        #--- methods
        self.__create()
    #END __init__()

    def __check_parameters(self):
        #--- project
        assert self._project, check.error(self, 1, `self._project`)
        #--- assetName
        assert self._assetName, check.error(self, 1, `self._assetName`)
        #--- assetRes
        assert self._assetRes, check.error(self, 1, `self._assetRes`)
        #--- assetType
        assert self._assetType, check.error(self, 1, `self._assetType`)

        #--- check path
        path = os.getenv('MAYA_PLUG_IN_PATH')
        envs = path.split(':')
        for i in envs:
            if 'PandorasBox' in i:
                self.path = i
        assert os.path.exists(self.path), check.error(self, 22, `self.path`)
        path_to_build = os.path.join(self.path, 'goe_builds')
        assert os.path.exists(path_to_build), check.error(self, 22, `path_to_build`)
    #END __check_parameters()

    def __setup_path(self):
        #--- build path
        self.build_path = os.path.join(self.path, "goe_builds")
        #--- project path
        self.project_path = os.path.join(self.build_path, self._project)
        #--- assetType path
        self.asset_type_path = os.path.join(self.project_path, self._assetType)
        #--- assetName path
        self.asset_name_path = os.path.join(self.asset_type_path, self._assetName)
        #--- assetBuild path
        self.asset_build_path = os.path.join(self.asset_name_path, "build_" + self._assetRes)
        #--- assetData path
        self.asset_data_path = os.path.join(self.asset_build_path, "data")
        #--- assetMisc path
        self.asset_misc_path = os.path.join(self.asset_data_path, "misc")
        #--- assetWeights path
        self.asset_weights_path = os.path.join(self.asset_data_path, "weights")
    #END __setup_path()

    def __create(self):
        #--- check parameters
        self.__check_parameters()
        #--- setup path
        self.__setup_path()
    #END __create()
#END Data()


class GuideIO(Data):
    def __init__(self):
        info = self.__check_scene()
        super(GuideIO, self).__init__(info[0], info[1], info[2], info[3])
    #END __init__()

    def __check_scene(self):
        assert cmds.objExists('GUIDE_ROOT'), check.error(self, 0, 'GUIDE_ROOT')
        project = cmds.getAttr('GUIDE_ROOT.project')
        asset_type = cmds.getAttr('GUIDE_ROOT.assetType')
        asset_res = cmds.getAttr('GUIDE_ROOT.assetResolution')
        asset_name = cmds.getAttr('GUIDE_ROOT.assetName')
        assert project, check.error(self, 0, `project`)
        assert asset_type, check.error(self, 0, `asset_type`)
        assert asset_res, check.error(self, 0, `asset_res`)
        assert asset_name, check.error(self, 0, `asset_name`)
        return [project, asset_type, asset_res, asset_name]
    #END __check_scene()

    def get_data(self):
        data = list()
        gr = 'GUIDE_ROOT'
        grgs = gr + '.globalScale'
        assert cmds.objExists(gr), check.error(self, 0, gr)
        assert cmds.objExists(grgs), check.error(self, 0, grgs)
        gs = cmds.getAttr(grgs)
        root = [gr, gs]
        data.append(root)

        sel = cmds.ls(type='goe_locator')
        for i in sel:
            trn = cmds.listRelatives(i, parent=True, type='transform')
            if not trn:
                break
            if not cmds.objExists(trn[0] + '.CTL'):
                break
            ctl = trn[0]
            assert cmds.objExists(ctl + '.side'), check.error(self, 0, `trn[0]`)
            assert cmds.objExists(ctl + '.name'), check.error(self, 0, `trn[0]`)
            assert cmds.objExists(ctl + '.index'), check.error(self, 0, `trn[0]`)
            #--- check if control is a mirror and asymmetrical
            if cmds.objExists(trn[0] + '.MIRROR'):
                if not cmds.objExists(trn[0] + '.ASYM'):
                    pass
            #--- get the attribute values
            side = cmds.getAttr(ctl + '.side')
            name = cmds.getAttr(ctl + '.name')
            index = cmds.getAttr(ctl + '.index')
            compose = side + '_' + name + 'Guide' + index + '_CTL'
            #--- get the position and rotation
            position = cmds.xform(ctl, query=True, translation=True)
            rotation = cmds.xform(ctl, query=True, rotation=True)
            result = [compose, position, rotation]
            data.append(result)
        return data
    #END get_data()

    def apply_data(self, data, path):
        """ Apply the guide data """
        for i, d in enumerate(data):
            if not i:
                if d[0]:
                    cmds.setAttr(d[0] + '.globalScale', d[1])
            else:
                if cmds.objExists(d[0]):
                    for n, axis in enumerate('xyz'):
                        if not cmds.getAttr(d[0] + '.t' + axis, lock=True):
                            cmds.setAttr(d[0] + '.t' + axis, d[1][n])
                        if not cmds.getAttr(d[0] + '.r' + axis, lock=True):
                            cmds.setAttr(d[0] + '.r' + axis, d[2][n])
                else:
                    cmds.warning("--- Couldn't apply guideData, because couldn't "
                                 "find the following guide in the scene: " + d[0])
    #END __apply_data()
#END GuideIO()


def save_guides(rigData, showInfo=True):
    gd = GuideIO()
    data = gd.get_data()

    result = list()
    #--- guides build
    gdata = rigData
    for i in gdata:
        result.append(i.rigdata)
    filepath = os.path.join(gd.asset_misc_path, 'guides_build.json')
    with open(filepath, 'w') as json_file:
        json.dump(result, json_file, sort_keys=True, indent=2, ensure_ascii=False)
    if showInfo:
        print ("+++ Successfully saved guides to following location: " + filepath)

    #--- guides data
    filepath = os.path.join(gd.asset_misc_path, 'guides_data.json')
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=2, ensure_ascii=False)
    if showInfo:
        print ("+++ Successfully saved guides to following location: " + filepath)
#END save_guides()


def load_guide_builds(path):
    data = list()
    if os.path.exists(path):
        with open(path) as json_file:
            json_data = json.load(json_file)
        data = json_data
    return data
#END load_guide_builds()


def load_guides(showInfo=True):
    gd = GuideIO()
    filepath = os.path.join(gd.asset_misc_path, 'guides_data.json')
    if os.path.exists(filepath):
        with open(filepath) as json_file:
            json_data = json.load(json_file)
        gd.apply_data(json_data, filepath)
    if showInfo:
        print ("+++ Successfully loaded guides from following location: " + filepath)
#END load_guides()


class ShapesIO(Data):
    def __init__(self):
        info = self.__check_scene()
        super(ShapesIO, self).__init__(info[0], info[1], info[2], info[3])
    #END __init__()

    def __check_scene(self):
        asset = cmds.ls(type='transform')
        project = None
        asset_type = None
        asset_res = None
        asset_name = None
        for i in asset:
            if cmds.objExists(i + '.project'):
                project = cmds.getAttr(i + '.project')
            if cmds.objExists(i + '.assetType'):
                asset_type = cmds.getAttr(i + '.assetType')
            if cmds.objExists(i + '.assetResolution'):
                asset_res = cmds.getAttr(i + '.assetResolution')
            if cmds.objExists(i + '.assetName'):
                asset_name = cmds.getAttr(i + '.assetName')
        assert project, check.error(self, 0, `project`)
        assert asset_type, check.error(self, 0, `asset_type`)
        assert asset_res, check.error(self, 0, `asset_res`)
        assert asset_name, check.error(self, 0, `asset_name`)
        return [project, asset_type, asset_res, asset_name]
    #END __check_scene()

    def get_data(self):
        data = list()
        sel = cmds.ls(type='goe_locator')
        assert sel, check.error(self, 0, str(sel))
        for i in sel:
            #--- get the localPosition and localScale
            lpos = list(cmds.getAttr(i + '.localPosition')[0])
            lsca = list(cmds.getAttr(i + '.localScale')[0])
            #--- get the shape info
            siz = cmds.getAttr(i + '.size')
            shp = cmds.getAttr(i + '.shape')
            ori = cmds.getAttr(i + '.orientation')
            col = cmds.getAttr(i + '.overrideColor')
            result = [i, lpos, lsca, siz, shp, ori, col]
            data.append(result)
        return data
    #END get_data()

    def apply_data(self, data):
        if not data:
            return
        for d in data:
            if not cmds.objExists(d[0]):
                continue
            #--- unlock the attributes
            cmds.setAttr(d[0] + '.localPosition', lock=False)
            cmds.setAttr(d[0] + '.localPosition.localPositionX', lock=False)
            cmds.setAttr(d[0] + '.localPosition.localPositionY', lock=False)
            cmds.setAttr(d[0] + '.localPosition.localPositionZ', lock=False)
            cmds.setAttr(d[0] + '.localScale', lock=False)
            cmds.setAttr(d[0] + '.localScale.localScaleX', lock=False)
            cmds.setAttr(d[0] + '.localScale.localScaleY', lock=False)
            cmds.setAttr(d[0] + '.localScale.localScaleZ', lock=False)
            cmds.setAttr(d[0] + '.size', lock=False)
            cmds.setAttr(d[0] + '.shape', lock=False)
            cmds.setAttr(d[0] + '.orientation', lock=False)
            cmds.setAttr(d[0] + '.overrideEnabled', lock=False)
            cmds.setAttr(d[0] + '.overrideColor', lock=False)

            #--- set the attributes
            cmds.setAttr(d[0] + '.localPosition', d[1][0], d[1][1], d[1][2], lock=True)
            cmds.setAttr(d[0] + '.localScale', d[2][0], d[2][1], d[2][2], lock=True)
            cmds.setAttr(d[0] + '.size', d[3], lock=True)
            cmds.setAttr(d[0] + '.shape', d[4], lock=True)
            cmds.setAttr(d[0] + '.orientation', d[5], lock=True)
            cmds.setAttr(d[0] + '.overrideEnabled', 1, lock=True)
            cmds.setAttr(d[0] + '.overrideColor', d[6])
    #END __apply_data()
#END ShapesIO()


def save_shapes(showInfo=True):
    sd = ShapesIO()
    data = sd.get_data()

    #--- save shapes
    filepath = os.path.join(sd.asset_misc_path, 'shapes.json')
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=2, ensure_ascii=False)
    if showInfo:
        print ("+++ Successfully saved control shapes to following location: " + filepath)
#END save_shapes()


def load_shapes(showInfo=True):
    sd = ShapesIO()

    #--- load shapes
    filepath = os.path.join(sd.asset_misc_path, 'shapes.json')
    if os.path.exists(filepath):
        with open(filepath) as json_file:
            json_data = json.load(json_file)
        sd.apply_data(json_data)
        if showInfo:
            print ("+++ Successfully loaded control shapes from following location: " + filepath)
#END load_shapes()


def generate_objects(rigdata):
    sd = ShapesIO()

    #--- load objects
    objpath = os.path.join(sd.asset_data_path, 'obj.py')
    generator.obj_builder(filepath=objpath, data=rigdata)
#END generate_objects()


class InfoPropCmds(object):
    """This class should be instantiated to get back infos for propCmds"""
    def __init__(self, grp=None, trn=None, shp=None, gmb=None, off=None, jnt=None):
        self.group = grp
        self.transform = trn
        self.shape = shp
        self.gimbal = gmb
        self.offsets = off
        self.joint = jnt
    #END __init__()
#END InfoPropCmds()


def save_cmds_data(data={}):
    """
    @type  data: dict
    @param data: specify all the flags, defaults, values and widgets of
                 the commands class.

                 Valid widgets are:
                 - combobox = create a combobox which adds a list
                 - lineEdit = create lineEdit which has no validator
                 - int = create lineEdit which has a integer validator
                 - double = create lineEdit which has a double validator

                 Here are two examples of how to setup:
                 {commandName:[{flagA: {'default: 'C', value: [...], widget: 'combobox'}},
                               {flagB: {'default: 'bla', value: 'bla, widget: 'lineEdit'}},
                               {flagC: {'default: 1, value: 1, widget: 'int'}}]}

                 {'propCmds': [{'side': {'default': 'C', 'value': ['C', 'L', 'R'], 'widget': 'combobox'}},
                               {'moduleName': {'default': None, 'value': None, 'widget': 'lineEdit'}}]}
    """
    #--- check path
    main = None
    path = os.getenv('MAYA_PLUG_IN_PATH')
    envs = path.split(':')
    for i in envs:
        if 'PandorasBox' in i:
            main = i
    data_path = os.path.join(main, 'goe_data')

    command = data.keys()[0]
    filepath = os.path.join(data_path, command + '.json')
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=2, ensure_ascii=False)
#END save_cmds_data()


def load_cmds_data():
    #--- check path
    main = None
    path = os.getenv('MAYA_PLUG_IN_PATH')
    envs = path.split(':')
    for i in envs:
        if 'PandorasBox' in i:
            main = i
    data_path = os.path.join(main, 'goe_data')

    files = os.listdir(data_path)
    datas = list()
    names = list()
    for i in files:
        name = None
        if '.json' in i:
            name = i.split('.json')[0]
            filepath = os.path.join(data_path, name + '.json')
            if os.path.exists(filepath):
                with open(filepath) as json_file:
                    json_data = json.load(json_file)
                    names.append(name)
                    datas.append(json_data)
    return [names, datas]
#END load_cmds_data()


class WeightsIO(Data):
    def __init__(self):
        info = self.__check_scene()
        super(WeightsIO, self).__init__(info[0], info[1], info[2], info[3])
    #END __init__()

    def __check_scene(self):
        asset = cmds.ls(type='transform')
        project = None
        asset_type = None
        asset_res = None
        asset_name = None
        for i in asset:
            if cmds.objExists(i + '.project'):
                project = cmds.getAttr(i + '.project')
            if cmds.objExists(i + '.assetType'):
                asset_type = cmds.getAttr(i + '.assetType')
            if cmds.objExists(i + '.assetResolution'):
                asset_res = cmds.getAttr(i + '.assetResolution')
            if cmds.objExists(i + '.assetName'):
                asset_name = cmds.getAttr(i + '.assetName')
        assert project, check.error(self, 0, `project`)
        assert asset_type, check.error(self, 0, `asset_type`)
        assert asset_res, check.error(self, 0, `asset_res`)
        assert asset_name, check.error(self, 0, `asset_name`)
        return [project, asset_type, asset_res, asset_name]
    #END __check_scene()
#END WeightsIO()


def save_weights(showInfo=True):
    """ This method saves the weights """
    w = WeightsIO()
    sel = cmds.ls(type="mesh")
    assert sel, "save_skincluster: No meshes in the scene!"
    for i in sel:
        if cmds.getAttr(i + '.intermediateObject'):
            continue
        skin = weights.Weights(i)
        data = skin.get_data()
        if not data:
            continue
        trn = cmds.listRelatives(i, parent=True)[0]
        #--- weights data
        filepath = os.path.join(w.asset_weights_path, trn + '.json')
        with open(filepath, 'w') as json_file:
            json.dump(data, json_file, sort_keys=True, indent=2, ensure_ascii=False)
        if showInfo:
            print ("+++ Successfully saved weights to following location: " + filepath)
#END save_weights()


def load_weights(showInfo=True):
    """ This method saves the skinclusters """
    w = WeightsIO()
    weights_path = w.asset_weights_path

    files = os.listdir(weights_path)
    for i in files:
        obj = None
        if '.json' in i:
            obj = i.split('.json')[0]
            if not cmds.objExists(obj):
                continue
            filepath = os.path.join(weights_path, obj + '.json')
            if not os.path.exists(filepath):
                continue
            with open(filepath) as json_file:
                json_data = json.load(json_file)
                shapes = cmds.listRelatives(obj, allDescendents=True)
                shape = [shp for shp in shapes if not cmds.getAttr(shp + '.intermediateObject')][0]
                skin = weights.Weights(shape)
                skin.set_data(json_data)
            if showInfo:
                print("+++ Successfully loaded the weights from following location: " + filepath)
#END load_weights()
