import sys
from maya import OpenMaya as om
from maya import OpenMayaMPx as mpx


class ShotFinal(mpx.MPxDeformerNode):
    '''ShotFinal deformer class'''
    nodeName = 'shotFinal'
    nodeId = om.MTypeId(0x002342)

    #--- attributes
    blendValue  = om.MObject()
    input       = mpx.cvar.MPxDeformerNode_input
    inputGeom   = mpx.cvar.MPxDeformerNode_inputGeom
    outputGeom  = mpx.cvar.MPxDeformerNode_outputGeom

    def __init__(self):
        '''constructor'''
        mpx.MPxDeformerNode.__init__(self)
    #end def __init__()

    def deform(self, data, iter, matrix, geomIndex):
        '''deformer'''
        #--- get the data of blendValue
        hBlendValue = data.outputValue(ShotFinal.blendValue)
        blendValue = hBlendValue.asFloat()
        
        #--- get the blendMesh
        hInputArray = data.outputArrayValue(ShotFinal.input)
        hInputArray.jumpToArrayElement(geomIndex)
        oInputGeom = hInputArray.outputValue().child(ShotFinal.inputGeom).asMesh()
        fnInputMesh = om.MFnMesh(oInputGeom)

        blendPoints = om.MPointArray()
        fnInputMesh.getPoints(blendPoints)

        print 'hahahah', iter.position()
        point = om.MPoint()
        while(iter.isDone()):
            index = iter.index()
            point = iter.position()

            print point
            iter.next()
#class ShotFinal()

def creator():
    '''get pointer'''
    return mpx.asMPxPtr(ShotFinal())
#end def creator()

def initialize():
    '''initialize attributes'''
    nAttr = om.MFnNumericAttribute()

    #--- blendWeight
    ShotFinal.blendValue = nAttr.create('blendValue', 'blv', om.MFnNumericData.kFloat)
    nAttr.setArray(True)
    nAttr.setKeyable(True)
    nAttr.setWritable(True)
    nAttr.setReadable(True)
    nAttr.setStorable(True)
    nAttr.setHidden(False)
    ShotFinal.addAttribute(ShotFinal.blendValue)
    ShotFinal.attributeAffects(ShotFinal.blendValue, ShotFinal.outputGeom)
#end def initialize()

def initializePlugin(mobject):
    '''register node'''
    fnPlugin = mpx.MFnPlugin(mobject)
    try:
        fnPlugin.registerNode(ShotFinal.nodeName, 
                              ShotFinal.nodeId, 
                              creator, 
                              initialize, 
                              mpx.MPxNode.kDeformerNode)
    except:
        sys.stderr.write('Failed to load plugin: ' + ShotFinal.nodeName)
#end def initializePlugin()

def uninitializePlugin(mobject):
    '''deregister node'''
    fnPlugin = mpx.MFnPlugin(mobject)
    try:
        fnPlugin.deregisterNode(ShotFinal.nodeId)
    except:
        sys.stderr.write('Failed to unload plugin: ' + ShotFinal.nodeName)
#end def uninitializePlugin()