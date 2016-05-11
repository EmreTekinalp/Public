'''
!\Maya\src\python\utility
@author: Emre Tekinalp
@date: Dec 14th, 2015
@contact: e.tekinalp@icloud.com
@brief: Reload operating system agnostic maya plug-ins
@requires: Nothing
@version: 1.0.0
'''


import os
import sys
import pymel.core as pm
from maya import cmds


def initialize(plugin):
    """Re-initialize specified plug in.

    @param plugin <string> Specify the plug-in name.
    """
    cmds.file(new=True, force=True)
    repo_path = os.path.abspath(__file__).split('Maya')[0]
    print repo_path
    path = os.path.join(repo_path, 'Maya', 'plug-ins')

    if sys.platform == 'win32' or sys.platform == 'cygwin':
        plugin = '%s.mll' % plugin
    elif sys.platform == 'linux' or sys.platform == 'linux2':
        plugin = '%s.so' % plugin
    elif sys.platform == 'darwin' or sys.platform == 'os2':
        plugin = '%s.dmg' % plugin
    # end if get full plug in name
    if pm.pluginInfo(plugin, query=True, loaded=True):
        pm.unloadPlugin(plugin)
    # end if plug in is loaded unload it
    pm.loadPlugin(os.path.join(path, plugin))
# end def initialize

print __file__
