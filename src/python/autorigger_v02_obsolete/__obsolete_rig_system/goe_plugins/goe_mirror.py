'''
@author:  etekinalp
@date:    Aug 26, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module creates a GOE_mirror node
'''

import math

from maya import OpenMaya
from maya import OpenMayaMPx


#--- PLUGIN NODE DEFINITION
nodeName = 'goe_mirror'
nodeId   = OpenMaya.MTypeId(0x647767)


class GOE_mirror(OpenMayaMPx.MPxNode):
    """ This custom node mirrors the given object in the specified axis """
    #--- ATTRIBUTE DEFINITION
    aInputMatrix = OpenMaya.MObject()
    aMirror      = OpenMaya.MObject()
    aMirrorAxis  = OpenMaya.MObject()

    aOutTranslation = OpenMaya.MObject()
    aOutRotation = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
    #END __init__()

    def compute(self, plug, data):
        #--- get inputs
        mirror = data.inputValue(GOE_mirror.aMirror).asShort()
        mirrorAxis = data.inputValue(GOE_mirror.aMirrorAxis).asShort()

        matrix = data.inputValue(GOE_mirror.aInputMatrix).asMatrix()
        mTransMatrix = OpenMaya.MTransformationMatrix(matrix)

        if (plug == GOE_mirror.aOutTranslation or (plug.isChild() and plug.parent() == GOE_mirror.aOutTranslation) or 
            plug == GOE_mirror.aOutRotation or (plug.isChild() and plug.parent() == GOE_mirror.aOutRotation)):
            #--- get the translation
            translation = mTransMatrix.translation(OpenMaya.MSpace.kWorld)
            #--- get rotation
            euler = mTransMatrix.rotation().asEulerRotation()
            angles = [math.degrees(angle) for angle in (euler.x, euler.y, euler.z)]

            if not mirror:
                return OpenMaya.kUnknownParameter
            #--- calculate the mirrored translation and rotation
            posX, posY, posZ = 0.0, 0.0, 0.0
            rotX, rotY, rotZ = 0.0, 0.0, 0.0
            if mirrorAxis == 0:
                posX, posY, posZ = -1 * translation.x, translation.y, translation.z
                rotX, rotY, rotZ = angles[0], -1 * angles[1], -1 * angles[2]
            elif mirrorAxis == 1:
                posX, posY, posZ = translation.x, -1 * translation.y, translation.z
                rotX, rotY, rotZ = -1 * angles[0], angles[1], -1 * angles[2]
            elif mirrorAxis == 2:
                posX, posY, posZ = translation.x, translation.y, -1 * translation.z
                rotX, rotY, rotZ = -1 * angles[0], -1 * angles[1], angles[2]

            #--- get the outputValues
            hOutTranslation = data.outputValue(GOE_mirror.aOutTranslation)
            hOutRotation = data.outputValue(GOE_mirror.aOutRotation)

            #--- set the outputValues
            hOutTranslation.set3Float(posX, posY, posZ)
            hOutRotation.set3Float(rotX, rotY, rotZ)
            data.setClean(plug)
    #END compute()
#END GOE_mirror()

def nodeCreator():
    return OpenMayaMPx.asMPxPtr(GOE_mirror())
#END nodeCreator()

def nodeInitializer():
    nAttr = OpenMaya.MFnNumericAttribute()
    eAttr = OpenMaya.MFnEnumAttribute()
    mAttr = OpenMaya.MFnMatrixAttribute()

    #--- inputMatrix attribute
    GOE_mirror.aInputMatrix = mAttr.create('inputMatrix', 'im', OpenMaya.MFnMatrixAttribute.kDouble)
    mAttr.setReadable(True)
    mAttr.setWritable(True)

    #--- mirror attribute
    GOE_mirror.aMirror = nAttr.create('mirror', 'mi', OpenMaya.MFnNumericData.kShort)
    nAttr.setMin(0)
    nAttr.setMax(1)
    nAttr.setDefault(1)
    nAttr.setReadable(True)
    nAttr.setStorable(True)
    nAttr.setWritable(True)
    nAttr.setKeyable(True)

    #--- mirrorAxis attribute
    GOE_mirror.aMirrorAxis = eAttr.create('mirrorAxis', 'ma', 0)
    eAttr.addField('yz', 0)
    eAttr.addField('xz', 1)
    eAttr.addField('xy', 2)
    eAttr.setHidden(False)
    eAttr.setKeyable(True)
    eAttr.setStorable(True)

    #--- outTranslation attribute
    GOE_mirror.aOutTranslation = nAttr.createPoint('outTranslation', 'ot')
    nAttr.setReadable(True)
    nAttr.setWritable(False)
    nAttr.setStorable(True)

    #--- outRotation attribute
    GOE_mirror.aOutRotation = nAttr.createPoint('outRotation', 'or')
    nAttr.setReadable(True)
    nAttr.setWritable(False)
    nAttr.setStorable(True)

    #--- add attribute
    GOE_mirror.addAttribute(GOE_mirror.aInputMatrix)
    GOE_mirror.addAttribute(GOE_mirror.aMirror)
    GOE_mirror.addAttribute(GOE_mirror.aMirrorAxis)

    GOE_mirror.addAttribute(GOE_mirror.aOutTranslation)
    GOE_mirror.addAttribute(GOE_mirror.aOutRotation)

    #--- affect attributes
    GOE_mirror.attributeAffects(GOE_mirror.aMirror, GOE_mirror.aOutTranslation)
    GOE_mirror.attributeAffects(GOE_mirror.aMirrorAxis, GOE_mirror.aOutTranslation)
    GOE_mirror.attributeAffects(GOE_mirror.aInputMatrix, GOE_mirror.aOutTranslation)

    GOE_mirror.attributeAffects(GOE_mirror.aMirror, GOE_mirror.aOutRotation)
    GOE_mirror.attributeAffects(GOE_mirror.aMirrorAxis, GOE_mirror.aOutRotation)
    GOE_mirror.attributeAffects(GOE_mirror.aInputMatrix, GOE_mirror.aOutRotation)
#END nodeInitializer()

def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, "GravityOfExplosion", "1.0", "Any")
    try:
        plugin.registerNode(nodeName, nodeId, nodeCreator, nodeInitializer,
                            OpenMayaMPx.MPxNode.kDependNode)
    except:
        raise Exception("Failed to load plugin: " + `nodeName`)
    return
#END initializePlugin()

def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(nodeId)
    except:
        raise Exception("Failed to unload plugin: " + `nodeName`)
    return
#END uninitializePlugin()