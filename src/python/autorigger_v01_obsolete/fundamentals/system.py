'''
Created on 12.02.2014
@author: Emre Tekinalp
@e-mail: e.tekinalp@icloud.com
@website: www.gravityofexplosion.com
@brief: That's the system class, which gets asset and other data paths
'''

import os, json


class AssetSystem(object):
    '''
    This class finds the necessary information of the file system to use assets
    '''

    def __init__(self):
        ########################################################################
        pass
    #END def __init__()

    def get_latest_version(self, path=None, asset=None):
        #--- this method gets the latest asset version
        if not path:
            raise Exception('No path specified!')
        if not asset:
            raise Exception('No asset specified!')
        asset_list = os.listdir(path)
        assets = list()
        for obj in asset_list:
            if asset in obj:
                if '.mb' in obj:
                    obj = obj.split('.')[0]
                elif '.ma' in obj:
                    obj = obj.split('.ma')[0]                    
                assets.append(obj)
        #--- sort the assets from small to large
        assets.sort()
        #--- return the latest asset
        if len(assets)>1:
            return assets[-1]
        else:
            return assets[0]
    #END def get_latest_version()
#END class AssetSystem()


class DataSystem(object):
    '''
    This class finds the necessary information and paths for the data module
    '''

    def __init__(self):
        ########################################################################
        #vars
        self.root = os.path.dirname(os.path.dirname(__file__))
    #END def __init__()

    def new_data_folder(self, folder=None, dirName=None):
        #--- this method creates a new folder
        if not folder:
            raise Exception('No folder name specified!')
        if not dirName:
            raise Exception('No directory name specified!')
        if not os.path.isdir(os.path.join(self.root, folder, str(dirName))):
           os.mkdir(os.path.join(self.root, folder, str(dirName)))
    #END def new_data_folder()

    def write_data(self, dirName=None, folder=None, fileName=None, obj=None):
        #--- this method writes down the data to a json file
        if not dirName:
            raise Exception('No directory name specified!')
        if not folder:
            raise Exception('No folder name specified!')
        if not fileName:
            raise Exception('No file name specified!')
        if not obj:
            raise Exception('No object name specified!')
        self.new_data_folder(folder=folder, dirName=dirName)
        path = os.path.abspath(os.path.join(self.root, folder, str(dirName)))
        #--- write down the data and store it in a json file
        output = open(path + '/' + fileName + '.json', 'w')
        json.dump(obj, output, indent = 2, sort_keys = True)
    #END def write_data()

    def read_data(self, dirName=None, folder=None, fileName=None):
        #--- this method reads the data
        if not dirName:
            raise Exception('No directory name specified!')
        if not folder:
            raise Exception('No folder name specified!')
        if not fileName:        
            raise Exception('No file name specified!')
        path = os.path.abspath(os.path.join(self.root, folder, str(dirName)))
        #--- open and load data
        data = open(path + '/' + fileName + '.json', 'r')
        output = json.load(data)
        return output
    #END def read_data()
#END class DataSystem()