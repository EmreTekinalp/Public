'''
Created on 21.11.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: This is the API class
'''

from maya import cmds , OpenMaya
import math


class API(object):
    '''
    this is the API class
    '''

    def __init__(self):
        ########################################################################
        #vars
        pass
        #methods
    #end def __init__()

    def get_pole_vector(self, 
                          jointChain = None):
        '''
        This method was originally written by Marco Giordano!
        '''
        #--- this method computes the poleVector position and rotation
        if jointChain:
            #--- get the position values of the selection
            start = cmds.xform(jointChain[0], 
                               query = True, 
                               rotatePivot = True, 
                               worldSpace = True)
            mid = cmds.xform(jointChain[1], 
                             query = True, 
                             rotatePivot = True, 
                             worldSpace = True)
            end = cmds.xform(jointChain[2], 
                             query = True, 
                             rotatePivot = True, 
                             worldSpace = True)
    
            #--- create vectors of the positions
            start_vec = OpenMaya.MVector(start[0], start[1], start[2])
            mid_vec   = OpenMaya.MVector(mid[0] ,mid[1],mid[2])
            end_vec   = OpenMaya.MVector(end[0] ,end[1],end[2])
            #--- get the distance between the start and the end
            start_end = end_vec - start_vec
            #--- get the distance between the start and the mid
            start_mid = mid_vec - start_vec
            #--- get the dotProduct of the start mid vector and the start end vector
            dot_product = start_mid * start_end
            #--- divide the dotProduct by the start end vector length
            projection = float(dot_product) / float(start_end.length())
            #--- get the normal of the start end
            start_end_normal = start_end.normal()
            projection_vec = start_end_normal * projection
            arrow_vec = start_mid - projection_vec
            arrow_vec *= 0.5 
            #--- final vector for the position
            final_vec = arrow_vec + mid_vec
    
            #--- get the poper orientation of the poleVector
            #--- create a crossProduct between the start end and start mid vector
            cross1 = start_end ^ start_mid
            cross1.normalize()
            #--- create a crossProduct between the cross1 and the arrow vector
            cross2 = cross1 ^ arrow_vec
            cross2.normalize()
            arrow_vec.normalize()
            #--- create a 4x4 matrix
            matrix_vec = [arrow_vec.x, arrow_vec.y, arrow_vec.z, 0, 
                          cross1.x, cross1.y, cross1.z, 0,
                          cross2.x, cross2.y, cross2.z, 0,
                          0, 0, 0, 1]
            #--- create a MMatrix
            matrix_m = OpenMaya.MMatrix()
            OpenMaya.MScriptUtil.createMatrixFromList(matrix_vec , matrix_m)
            matrix_fn = OpenMaya.MTransformationMatrix(matrix_m)
            #--- change matrix into eulerRotation
            rot = matrix_fn.eulerRotation()
            #--- store the position and rotation values
            position = [final_vec.x, final_vec.y, final_vec.z]
            rotation = [rot.x/math.pi*180.0, 
                        rot.y/math.pi*180.0, 
                        rot.z/math.pi*180.0]
            return [position, rotation]
        else:
            raise Exception('Nothing specified, cannot proceed!')
    #end def get_pole_vector()
#end class API()