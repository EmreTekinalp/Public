'''
@author:  Emre
@date:    Sun 23 Nov 2014 19:04:00 PM PDT
@mail:    e.tekinalp@icloud.com
@brief:   This module contains a duplicate class
'''


from maya import cmds

from goe_functions import check


class Duplicate(object):
    """ This class deals with everything concerning duplication of nodes """
    def __init__(self,
                 obj=None,
                 replace=[None, None],
                 parent=None,
                 world=False):
        """
        @type  obj: string, list
        @param obj: specify the objectName or a list of objects to duplicate

        @type  replace: strings in a list
        @param replace: specify the first element and replace it with the second

        @type  parent: string
        @param parent: specify the parent node.

        @type  world: bool
        @param world: Specify if objects should be parented to the world.
        """
        #--- args
        self._obj = obj
        self._replace = replace
        self._parent = parent
        self._world = world

        #--- vars
        self.result = list()

        #--- methods
        self.__create()
    #END __init__()

    def __check_parameters(self):
        """ Check the given parameters for validation """
        #--- obj
        assert self._obj, check.error(self, 1, `self._obj`)

        #--- replace
        assert self._replace, check.error(self, 1, `self._replace`)
    #END __check_parameters()

    def __duplicate_selection(self):
        """ Duplicate the selected objects properly """
        if isinstance(self._obj, list):
            for i in self._obj:
                duplicate = cmds.duplicate(i, renameChildren=True, parentOnly=True)
                dup_result = [self.__rename_node(obj=dup) for dup in duplicate]
                self.result.append(dup_result)
        else:
            duplicate = cmds.duplicate(self._obj, renameChildren=True)
            self.result = [self.__rename_node(obj=dup) for dup in duplicate]
        cmds.select(clear=True)
        return self.result
    #END __duplicate_selection()

    def __rename_node(self, obj=None):
        """ Replace and rename the given node properly """
        new_name = obj.replace(self._replace[0], self._replace[1])[:-1]
        result = cmds.rename(obj, new_name)
        return result
    #END __rename_node()

    def __parent_duplicate(self):
        """ Parent the duplicate to the specified node """
        if self._parent:
            child = cmds.listRelatives(self.result[0], children=True)[0]
            if child == self.result[1]:
                cmds.parent(self.result[0], self._parent)
            else:
                cmds.parent(self.result, self._parent)
        else:
            if not self._world:
                return
            child = cmds.listRelatives(self.result[0], children=True)[0]
            if child == self.result[1]:
                cmds.parent(self.result[0], world=True)
            else:
                cmds.parent(self.result, world=True)
    #END __parent_duplicate()

    def __create(self):
        """ Call the methods in the proper order """
        #--- check parameters
        self.__check_parameters()
        #--- duplicate the selection
        self.__duplicate_selection()
        #--- parent the duplicate
        self.__parent_duplicate()
    #END __create()
#END Duplicate()
