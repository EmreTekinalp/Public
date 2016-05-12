'''
Created on Oct 28, 2014

@author: Emre
'''

import math

from maya import cmds, OpenMaya


def calculate_polevector(start=[], mid=[], end=[], offset=1):
    """ Calculate the position for the polevector on a ikRotatePlaneSolver """
    vstart = OpenMaya.MVector(start[0], start[1], start[2])
    vmid = OpenMaya.MVector(mid[0], mid[1], mid[2])
    vend = OpenMaya.MVector(end[0], end[1], end[2])

    vstartend = vend - vstart
    vstartmid = vmid - vstart

    vdotprod = vstartend * vstartmid
    proj = float(vdotprod) / float(vstartend.length())
    nstartend = vstartend.normal()

    vproj = nstartend * proj
    varrow = vstartmid - vproj

    varrow *= offset
    vpos = vmid + varrow
    return vpos
#END calculate_polevector()


def distance(objects=None):
    """ Measure the distance of the given objects """
    assert objects, 'Cannot work with None type objects!'
    assert isinstance(objects, list), 'A list is needed as objects flag value!'

    distance = 0
    if len(objects) > 2:
        #--- measure the distance between each object in the list
        result = []
        for i in range(len(objects)):
            j = i + 1
            obj_one = cmds.xform(objects[i],
                                 query=True,
                                 rotatePivot=True,
                                 worldSpace=True)
            if not j == len(objects):
                obj_two = cmds.xform(objects[j],
                                     query=True,
                                     rotatePivot=True,
                                     worldSpace=True)
                #--- compute the distance
                dist = math.sqrt(pow((obj_two[0] - obj_one[0]), 2) +
                                 pow((obj_two[1] - obj_one[1]), 2) +
                                 pow((obj_two[2] - obj_one[2]), 2))
                result.append(dist)
        distance = sum(result)
    elif len(objects) < 2:
        #--- give error if list contains less than 2 elements
        raise Exception('Specified list: ' + str(objects) +
                        ' contains just 1 element. Need 2 elements!')
    else:
        #--- get the position in worldSpace of the objects
        obj_one = cmds.xform(objects[0], query=True,
                             rotatePivot=True, worldSpace=True)
        obj_two = cmds.xform(objects[1], query=True,
                             rotatePivot=True, worldSpace=True)
        #--- compute the distance
        result = math.sqrt(pow((obj_two[0] - obj_one[0]), 2) +
                           pow((obj_two[1] - obj_one[1]), 2) +
                           pow((obj_two[2] - obj_one[2]), 2))
        distance = result
    return distance
#END distance()
