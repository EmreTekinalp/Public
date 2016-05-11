'''
Created on 21.11.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: This is the measure class
'''

from maya import cmds
from math import *


class Measure(object):
    '''
    This class deals with everything concerning measures of nodes
    '''

    def __init__(self,
                  objects = None):
        ########################################################################
        #vars
        self.distance = []

        #methods
        self.__create(objects = objects)
    #end def __init__()

    def __measure_distance(self,
                             objects = None):
        #--- this method measures the distance of the objects
        if objects:
            if isinstance(objects, list):
                if len(objects) > 2:
                    #--- measure the distance between each object in the list
                    result = []
                    for i in range(len(objects)):
                        j = i + 1
                        obj_one = cmds.xform(objects[i], 
                                             query = True, 
                                             rotatePivot = True, 
                                             worldSpace = True)
                        if not j == len(objects):
                            obj_two = cmds.xform(objects[j], 
                                                 query = True, 
                                                 rotatePivot = True, 
                                                 worldSpace = True)
                            #--- compute the distance
                            dist = sqrt(pow((obj_two[0] - obj_one[0]), 2) + 
                                        pow((obj_two[1] - obj_one[1]), 2) + 
                                        pow((obj_two[2] - obj_one[2]), 2))
                            result.append(dist)
                    self.distance = sum(result)
                elif len(objects) < 2:
                    #--- give error if list contains less than 2 elements
                    raise Exception('Specified list: ' + str(objects) + 
                                    ' contains just 1 element. Need 2 elements!')
                else:
                    #--- measure the distance between two objects
                    #--- get the position in worldSpace of the objects
                    obj_one = cmds.xform(objects[0], 
                                         query = True, 
                                         rotatePivot = True, 
                                         worldSpace = True)
                    obj_two = cmds.xform(objects[1], 
                                         query = True, 
                                         rotatePivot = True, 
                                         worldSpace = True)
                    #--- compute the distance
                    result = sqrt(pow((obj_two[0] - obj_one[0]), 2) + 
                                  pow((obj_two[1] - obj_one[1]), 2) + 
                                  pow((obj_two[2] - obj_one[2]), 2))
                    self.distance = result
            else:
                raise Exception('A list is needed as objects flag value!')
        else:
            raise Exception('Cannot work with None type objects!')
    #end def __measure_distance()

    def __create(self,
                  objects = None):
        #--- this is the main creation method
        #--- check the specified objects
        self.__measure_distance(objects = objects)
    #end def __create()
#end class Measure()