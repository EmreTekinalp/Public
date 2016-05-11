'''
Created on 18.11.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: This is the duplicate class
'''

from maya import cmds


class Duplicate(object):
    '''
    This class deals with everything concerning duplication of nodes
    '''

    def __init__(self,
                  obj = None,
                  replace = [None, None],
                  parent = None,
                  worldSpace = False):
        ########################################################################
        #vars
        self.result = []

        #methods
        self.__create(obj = obj,
                      replace = replace,
                      parent = parent,
                      worldSpace = worldSpace)
    #end def __init__()

    def __duplicate_selection(self,
                                 obj = None,
                                 replace = [None, None]):
        #--- this method duplicates the selection and renames it properly
        if obj:
            if not replace == [None, None]:
                if isinstance(obj, list):
                    for i in obj:
                        dup_result = []
                        duplicate = cmds.duplicate(i, renameChildren = True)
                        for dup in duplicate:
                            result = self.__rename_node(obj = dup,
                                                        replace = replace)
                            dup_result.append(result)
                        self.result.append(dup_result)
                else:
                    duplicate = cmds.duplicate(obj, renameChildren = True)
                    for dup in duplicate:
                        result = self.__rename_node(obj = dup, replace = replace)
                        self.result.append(result)
                cmds.select(clear = True)
                return self.result
            else:
                raise Exception('Replace flag has invalid items : ' + str(replace))
        else:
            raise Exception('Specified obj : ' + str(obj) + ' is not valid!')
    #end def __duplicate_selection()

    def __rename_node(self,
                        obj = None,
                        replace = [None, None]):
        #--- this method replaces and renames the given node properly
        new_name = obj.replace(replace[0], replace[1])[:-1]
        #--- rename the obj
        result = cmds.rename(obj, new_name)
        return result
    #end def __rename_node()

    def __parent_duplicate(self,
                             parent = None,
                             worldSpace = False):
        #--- this method parents the duplicate to the specified parent
        if parent:
            if cmds.listRelatives(self.result[0], children = True)[0] == self.result[1]:
                cmds.parent(self.result[0], parent)
            else:
                cmds.parent(self.result, parent)                
        else:
            if worldSpace:
                if cmds.listRelatives(self.result[0], children = True)[0] == self.result[1]:
                    cmds.parent(self.result[0], world = True)
                else:
                    cmds.parent(self.result, world = True)
    #end  def __parent_duplicate()

    def __create(self,
                  obj = None,
                  replace = [None, None],
                  parent = None,
                  worldSpace = False):
        #--- this method is the main creator
        #--- duplicate the selection
        self.__duplicate_selection(obj = obj,
                                   replace = replace)
        #--- parent the duplicate
        self.__parent_duplicate(parent = parent,
                                worldSpace = worldSpace)
    #end def __create()
#end class Duplicate()
