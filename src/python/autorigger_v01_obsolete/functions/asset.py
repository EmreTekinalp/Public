'''
Created on 12.02.2014
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: The asset class to load, import and export assets
'''

import os
from maya import cmds
from fundamentals import system
reload(system)


class Asset(system.AssetSystem):
    """
    This class handles asset functions like loading latest assets, 
    specific asset versions, import, export and saving of assets
    """

    def __init__(self):
        ########################################################################
        super(Asset, self).__init__()
    #END def __init__()

    def load_latest_asset(self, assetPath=None, asset=None, fileType='ma'):
        #--- this method loads the latest asset from the given assetPath
        #--- get the latest asset version
        latest_asset = self.get_latest_version(assetPath, asset)
        #--- get the latest asset path
        final_path = os.path.join(assetPath, latest_asset + '.' + fileType)

        #--- check the fileType
        if fileType == 'ma':
            fileType = 'mayaAscii'
        elif fileType == 'mb':
            fileType = 'mayaBinary'
        else:
            raise Exception('Specified fileType is not valid: ' + fileType)

        #--- open a new file and import the latest asset
        cmds.file(new=True, force=True)
        cmds.file(final_path,
                  i=True,
                  type=fileType,
                  renameAll=False,
                  mergeNamespacesOnClash=False, 
                  preserveReferences=True,
                  loadReferenceDepth='all')
        print ('Successfully loaded asset: ' + final_path)
    #END def load_latest_asset()   
#END class Asset()
