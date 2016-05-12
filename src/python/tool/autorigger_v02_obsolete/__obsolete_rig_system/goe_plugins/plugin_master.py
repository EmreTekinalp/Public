'''
@author:  etekinalp
@date:    Aug 28, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This is the plugin setup master module
'''

from maya import cmds
from goe_functions import check
reload(check)


class PluginSetup(object):
    """
    DESCRIPTION:    This class setups a plugin and should be subclassed.
    REQUIRES:       arguments
    RETURNS:        Nothing
    """
    def __init__(self, plugin=None, suffix=None, update=False, info=False):
        """
        @param plugin: specify the plugin name
        @type  plugin: string

        @param suffix: specify the suffix, ie. 'so' or 'py'
        @type  suffix: string

        @param update: define to update the plugin or not
        @type  update: bool

        @param info:   show status reports printed in the script editor
        @type  info:   bool
        """
        # args
        self.plugin = plugin
        self.suffix = suffix
        self.update = update
        self.info = info

        # vars
        self.base_path = None

        # methods
        self.__create()
    #END __init__()

    def __check_parameters(self):
        #--- plugin
        assert self.plugin, check.error(self, 2, `self.plugin`)
        assert isinstance(self.plugin, str), check.error(self, 2, `self.plugin`)

        #--- suffix
        assert self.suffix, check.error(self, 2, `self.suffix`)
        assert isinstance(self.suffix, str), check.error(self, 2, `self.suffix`)
    #END __check_parameters()

    def __check_path(self):
        """ this method check the path """
        if self.suffix == 'so':
            self.base_path = '/home/Emre/git/PandorasBox/Plugins/'
        else:
            self.suffix = 'py'
            self.base_path = '/home/Emre/Documents/workspace/PandorasBox/goe_plugins/'
    #END __check_path()

    def __update_plugin(self):
        """ this method updates the plugin """
        #--- open a new file
        cmds.file(new=True, force=True)
        #--- check if the plugin was specified
        assert self.plugin, check.error(self, 10)
        #--- compose the plugin path
        path = None
        if self.suffix == 'so':
            path = self.base_path + self.plugin + '/' + self.plugin + '.so'
        else:
            path = self.base_path + self.plugin + '.py'
        #--- reload plugin
        if cmds.pluginInfo(self.plugin + '.' + self.suffix, query=True, loaded=True):
            cmds.unloadPlugin(self.plugin + '.' + self.suffix)
        cmds.loadPlugin(path)
        if self.info:
            print 'Successfully reloaded plugin: ' + self.plugin + '.' + self.suffix
    #END __update_plugin()

    def __check_plugin(self):
        """ this method check the plugin """
        comp = self.plugin + '.' + self.suffix
        if not cmds.pluginInfo(comp, query=True, loaded=True):
            #--- check if the plugin was specified
            assert self.plugin, check.error(self, 10)
            #--- compose the plugin path
            path = None
            if self.suffix == 'so':
                path = self.base_path + self.plugin + '/' + self.plugin + '.so'
            else:
                path = self.base_path + self.plugin + '.py'
            cmds.loadPlugin(path)
            if self.info:
                print 'Successfully loaded plugin: ' + self.plugin + '.' + self.suffix
        else:
            if self.info:
                print 'Plugin already loaded: ' + self.plugin + '.' + self.suffix
    #END __check_plugin()

    def __create(self):
        """ this method is the main create method """
        #--- check parameters
        self.__check_parameters()
        #--- check the path
        self.__check_path()

        if self.update:
            #--- update the plugin
            self.__update_plugin()

        #--- check the plugin
        self.__check_plugin()
    #END __create()
#END PluginSetup()
