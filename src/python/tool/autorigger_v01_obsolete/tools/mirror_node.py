import sys
import math
from maya import cmds
from maya import OpenMaya as om
from maya import OpenMayaMPx as mpx


class MirrorSwitch(mpx.MPxNode):
    '''This custom node mirrors the given object in x'''
    nodeName = 'mirrorSwitch'
    nodeId   = om.MTypeId(0x000505)

    aInputMatrix = om.MObject()
    aMirror      = om.MObject()
    aMirrorAxis  = om.MObject()

    aOutPosition = om.MObject()
    aOutPosX     = om.MObject()
    aOutPosY     = om.MObject()
    aOutPosZ     = om.MObject()

    aOutRotation = om.MObject()
    aOutRotX     = om.MObject()
    aOutRotY     = om.MObject()
    aOutRotZ     = om.MObject()

    def __init__(self):
        '''constructor'''
        mpx.MPxNode.__init__(self)
    #end def __init__()

    def compute(self, plug, data):
        '''compute function'''

        #--- get mirror input
        mirror = data.inputValue(MirrorSwitch.aMirror).asShort()

        #--- get mirrorAxis input
        mirrorAxis = data.inputValue(MirrorSwitch.aMirrorAxis).asShort()

        #--- get inputMatrix input
        matrix = data.inputValue(MirrorSwitch.aInputMatrix).asMatrix()
        mTransMatrix = om.MTransformationMatrix(matrix)

        if ((plug == MirrorSwitch.aOutPosX) or 
            (plug == MirrorSwitch.aOutPosY) or 
            (plug == MirrorSwitch.aOutPosZ)):
            #--- get the translation
            translation = mTransMatrix.translation(om.MSpace.kWorld)

            if mirror:
                #--- calculate the mirrored translation
                posX = 0.0
                posY = 0.0
                posZ = 0.0
                if mirrorAxis == 0:
                    posX = -1 * translation.x
                    posY = translation.y
                    posZ = translation.z
                elif mirrorAxis == 1:
                    posX = translation.x
                    posY = -1 * translation.y
                    posZ = translation.z
                elif mirrorAxis == 2:
                    posX = translation.x
                    posY = translation.y
                    posZ = -1 * translation.z
    
                #--- get the outputValues
                hOutPosX = data.outputValue(MirrorSwitch.aOutPosX)
                hOutPosY = data.outputValue(MirrorSwitch.aOutPosY)
                hOutPosZ = data.outputValue(MirrorSwitch.aOutPosZ)

                #--- set the outputValues
                hOutPosX.setFloat(posX)
                hOutPosY.setFloat(posY)
                hOutPosZ.setFloat(posZ)

                data.setClean(plug)
            else:
                return om.kUnknownParameter

        elif ((plug == MirrorSwitch.aOutRotX) or 
              (plug == MirrorSwitch.aOutRotY) or 
              (plug == MirrorSwitch.aOutRotZ)):
            #--- get the euler rotation values
            euler = mTransMatrix.rotation().asEulerRotation()
            #--- find degrees
            angles = [math.degrees(angle) for angle in (euler.x, euler.y, euler.z)]

            if mirror:
                #--- calculate the mirrored rotation
                rotX = 0.0
                rotY = 0.0
                rotZ = 0.0
                if mirrorAxis == 0:
                    rotX = angles[0]
                    rotY = -1 * angles[1]
                    rotZ = -1 * angles[2]
                elif mirrorAxis == 1:
                    rotX = -1 * angles[0]
                    rotY = angles[1]
                    rotZ = -1 * angles[2]
                elif mirrorAxis == 2:
                    rotX = -1 * angles[0]
                    rotY = -1 * angles[1]
                    rotZ = angles[2]

                #--- get the outputValues
                hOutRotX = data.outputValue(MirrorSwitch.aOutRotX)
                hOutRotY = data.outputValue(MirrorSwitch.aOutRotY)
                hOutRotZ = data.outputValue(MirrorSwitch.aOutRotZ)

                #--- set the outputValues
                hOutRotX.setFloat(rotX)
                hOutRotY.setFloat(rotY)
                hOutRotZ.setFloat(rotZ)

                data.setClean(plug)
            else:
                return om.kUnknownParameter
        else:
            return om.kUnknownParameter
    #end def compute()
#end class MirrorSwitch()

def creator():
    '''get the pointer'''
    return mpx.asMPxPtr(MirrorSwitch())
#end def creator()

def initialize():
    '''initialize attributes'''
    cAttr = om.MFnCompoundAttribute()
    nAttr = om.MFnNumericAttribute()
    eAttr = om.MFnEnumAttribute()
    mAttr = om.MFnMatrixAttribute()

    #--- inputMatrix attribute
    MirrorSwitch.aInputMatrix = mAttr.create('inputMatrix', 'im', om.MFnMatrixAttribute.kDouble)
    mAttr.setReadable(True)
    mAttr.setStorable(True)
    mAttr.setWritable(True)

    #--- mirror attribute
    MirrorSwitch.aMirror = nAttr.create('mirror', 'mi', om.MFnNumericData.kShort)
    nAttr.setMin(0)
    nAttr.setMax(1)
    nAttr.setDefault(1)
    nAttr.setReadable(True)
    nAttr.setStorable(True)
    nAttr.setWritable(True)
    nAttr.setKeyable(True)

    #--- mirrorAxis attribute
    MirrorSwitch.aMirrorAxis = eAttr.create('mirrorAxis', 'ma', 0)
    eAttr.addField('yz', 0)
    eAttr.addField('xz', 1)
    eAttr.addField('xy', 2)
    eAttr.setHidden(False)
    eAttr.setKeyable(True)
    eAttr.setStorable(True)

    #--- outPosX attribute
    MirrorSwitch.aOutPosX = nAttr.create('outPosX', 'opx', om.MFnNumericData.kFloat)
    nAttr.setReadable(True)
    nAttr.setStorable(False)
    nAttr.setWritable(False)
    nAttr.setKeyable(False)

    #--- outPosY attribute
    MirrorSwitch.aOutPosY = nAttr.create('outPosY', 'opy', om.MFnNumericData.kFloat)
    nAttr.setReadable(True)
    nAttr.setStorable(False)
    nAttr.setWritable(False)
    nAttr.setKeyable(False)

    #--- outPosZ attribute
    MirrorSwitch.aOutPosZ = nAttr.create('outPosZ', 'opz', om.MFnNumericData.kFloat)
    nAttr.setReadable(True)
    nAttr.setStorable(False)
    nAttr.setWritable(False)
    nAttr.setKeyable(False)

    #--- outPosition attribute
    MirrorSwitch.aOutPosition = cAttr.create('outPosition', 'op')
    cAttr.addChild(MirrorSwitch.aOutPosX)
    cAttr.addChild(MirrorSwitch.aOutPosY)
    cAttr.addChild(MirrorSwitch.aOutPosZ)

    #--- outRotX attribute
    MirrorSwitch.aOutRotX = nAttr.create('outRotX', 'orx', om.MFnNumericData.kFloat)
    nAttr.setReadable(True)
    nAttr.setStorable(False)
    nAttr.setWritable(False)
    nAttr.setKeyable(False)

    #--- outRotY attribute
    MirrorSwitch.aOutRotY = nAttr.create('outRotY', 'ory', om.MFnNumericData.kFloat)
    nAttr.setReadable(True)
    nAttr.setStorable(False)
    nAttr.setWritable(False)
    nAttr.setKeyable(False)

    #--- outRotZ attribute
    MirrorSwitch.aOutRotZ = nAttr.create('outRotZ', 'orz', om.MFnNumericData.kFloat)
    nAttr.setReadable(True)
    nAttr.setStorable(False)
    nAttr.setWritable(False)
    nAttr.setKeyable(False)

    #--- outRotation attribute
    MirrorSwitch.aOutRotation = cAttr.create('outRotation', 'or')
    cAttr.addChild(MirrorSwitch.aOutRotX)
    cAttr.addChild(MirrorSwitch.aOutRotY)
    cAttr.addChild(MirrorSwitch.aOutRotZ)

    #--- add attribute
    MirrorSwitch.addAttribute(MirrorSwitch.aInputMatrix) 
    MirrorSwitch.addAttribute(MirrorSwitch.aMirror)
    MirrorSwitch.addAttribute(MirrorSwitch.aMirrorAxis)
    MirrorSwitch.addAttribute(MirrorSwitch.aOutPosition)    
    MirrorSwitch.addAttribute(MirrorSwitch.aOutRotation)

    #--- affect attributes
    #--- outPosition
    MirrorSwitch.attributeAffects(MirrorSwitch.aMirror, MirrorSwitch.aOutPosition)    
    MirrorSwitch.attributeAffects(MirrorSwitch.aMirror, MirrorSwitch.aOutPosX)
    MirrorSwitch.attributeAffects(MirrorSwitch.aMirror, MirrorSwitch.aOutPosY)
    MirrorSwitch.attributeAffects(MirrorSwitch.aMirror, MirrorSwitch.aOutPosZ)

    MirrorSwitch.attributeAffects(MirrorSwitch.aMirrorAxis, MirrorSwitch.aOutPosition)
    MirrorSwitch.attributeAffects(MirrorSwitch.aMirrorAxis, MirrorSwitch.aOutPosX)
    MirrorSwitch.attributeAffects(MirrorSwitch.aMirrorAxis, MirrorSwitch.aOutPosY)
    MirrorSwitch.attributeAffects(MirrorSwitch.aMirrorAxis, MirrorSwitch.aOutPosZ)

    MirrorSwitch.attributeAffects(MirrorSwitch.aInputMatrix, MirrorSwitch.aOutPosition)
    MirrorSwitch.attributeAffects(MirrorSwitch.aInputMatrix, MirrorSwitch.aOutPosX)
    MirrorSwitch.attributeAffects(MirrorSwitch.aInputMatrix, MirrorSwitch.aOutPosY)
    MirrorSwitch.attributeAffects(MirrorSwitch.aInputMatrix, MirrorSwitch.aOutPosZ)

    #--- outRotation
    MirrorSwitch.attributeAffects(MirrorSwitch.aMirror, MirrorSwitch.aOutRotation)
    MirrorSwitch.attributeAffects(MirrorSwitch.aMirror, MirrorSwitch.aOutRotX)
    MirrorSwitch.attributeAffects(MirrorSwitch.aMirror, MirrorSwitch.aOutRotY)
    MirrorSwitch.attributeAffects(MirrorSwitch.aMirror, MirrorSwitch.aOutRotZ)

    MirrorSwitch.attributeAffects(MirrorSwitch.aMirrorAxis, MirrorSwitch.aOutRotation)
    MirrorSwitch.attributeAffects(MirrorSwitch.aMirrorAxis, MirrorSwitch.aOutRotX)
    MirrorSwitch.attributeAffects(MirrorSwitch.aMirrorAxis, MirrorSwitch.aOutRotY)
    MirrorSwitch.attributeAffects(MirrorSwitch.aMirrorAxis, MirrorSwitch.aOutRotZ)

    MirrorSwitch.attributeAffects(MirrorSwitch.aInputMatrix, MirrorSwitch.aOutRotation)
    MirrorSwitch.attributeAffects(MirrorSwitch.aInputMatrix, MirrorSwitch.aOutRotX)
    MirrorSwitch.attributeAffects(MirrorSwitch.aInputMatrix, MirrorSwitch.aOutRotY)
    MirrorSwitch.attributeAffects(MirrorSwitch.aInputMatrix, MirrorSwitch.aOutRotZ)
#end def initialize()

def initializePlugin(mobject):
    '''register node'''
    fnPlugin = mpx.MFnPlugin(mobject)
    try:
        fnPlugin.registerNode(MirrorSwitch.nodeName, 
                              MirrorSwitch.nodeId, 
                              creator, 
                              initialize, 
                              mpx.MPxNode.kDependNode)
    except:
        sys.stderr.write('Failed to load plugin: ' + MirrorSwitch.nodeName)
#end def initializePlugin()

def uninitializePlugin(mobject):
    '''deregister node'''
    fnPlugin = mpx.MFnPlugin(mobject)
    try:
        fnPlugin.deregisterNode(MirrorSwitch.nodeId)
    except:
        sys.stderr.write('Failed to unload plugin: ' + MirrorSwitch.nodeName)
#end def uninitializePlugin()


