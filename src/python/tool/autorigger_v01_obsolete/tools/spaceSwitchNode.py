import sys
import math
from maya import cmds
from maya import OpenMaya as om
from maya import OpenMayaMPx as mpx
from maya import OpenMayaAnim as oma


class SpaceSwitch(mpx.MPxNode):
    nodeName = 'spaceSwitch'
    nodeId   = om.MTypeId(0x000505)

    aDriver        = om.MObject()
    aDriven        = om.MObject()
    aLocatorToDrv  = om.MObject()
    aLocatorToDrvn = om.MObject()
    aConstraint    = om.MObject()
    aSwitch        = om.MObject()
    aOutput        = om.MObject()

    def __init__(self):
        '''constructor'''
        mpx.MPxNode.__init__(self)
    #end def __init__()

    def compute(self, plug, data):
        '''compute function'''
        if plug != SpaceSwitch.aSwitch:
            print 'nooooooo'
            return om.kUnknownParameter

        #--- get inputValue of the switch attr
        switchValue = data.inputValue(SpaceSwitch.aSwitch).asInt()

        if switchValue:
            #--- get the connected locatorToDriver node
            locToDrv = self.__get_connected_node(SpaceSwitch.aLocatorToDrv)

            #--- get the connected driven control node
            driven = self.__get_connected_node(SpaceSwitch.aDriven)
            print driven

            #--- get the transform values
            locWorld = self.__get_worldSpace_values(locToDrv)
            position = locWorld[0]
            rotation = locWorld[1]

            print position
            print rotation

            #--- set the transform values to the driven control
#            cmds.xform(driven, translation = position, worldSpace = True)
#            cmds.xform(driven, rotation = rotation, worldSpace = True)
        else:
            return
            #--- set the current frame back
            currentFrame = self.__current_keyframe(True, keyOff)

            #--- get the nodes of the message attributes (driver)
            driver = self.__get_connected_node(SpaceSwitch.aDriver)


            #--- get the nodes of the message attributes (locator)
            locator = self.__get_connected_node(SpaceSwitch.aLocator)

            #--- get the transform values
            locatorTransform = self.__get_worldSpace_values(locator)
            position = locatorTransform[0]
            rotation = locatorTransform[1]

            #--- set the transform values to the driver
            cmds.xform(driver, translation = position, worldSpace = True)

            #--- go back to initial frame
            currentFrame = self.__current_keyframe(False, keyOff)

#        output = data.outputValue(SpaceSwitch.aOutput)
#        output.setInt(switchValue)
        data.setClean(plug)
    #end def compute()

    def __get_connected_node(self, attribute):
        '''get the node connected to the given attribute'''
        plug = om.MPlug(self.thisMObject(), attribute)
        plugArray = om.MPlugArray()
        plug.connectedTo(plugArray, True, False)

        nodePath = None
        if (plugArray.length() > 0):
            node = plugArray[0].node()
            fnDagNode = om.MFnDagNode(node)
            dagPath = om.MDagPath()
            path = fnDagNode.getPath(dagPath)
            nodePath = fnDagNode.fullPathName()
        return nodePath
    #end def __get_connected_node()

    def __get_worldSpace_values(self, node):
        '''this method gets the worldSpace values of a node, wether it is parented or not.'''
        #--- get the current selection
        mSel = om.MSelectionList()
        mSel.add(node)

        dagPath = om.MDagPath()
        mObj = om.MObject()    
        mSel.getDagPath(0, dagPath)
        mSel.getDependNode(0, mObj)    
        dgNode = om.MFnDagNode(dagPath)

        #--- get the worldMatrix
        plug = dgNode.findPlug('worldMatrix')
        elem = plug.elementByLogicalIndex(0).asMObject()    
        worldMatrix = om.MFnMatrixData(elem).matrix()    
        mTransMtx = om.MTransformationMatrix(worldMatrix)

        #--- get the rotation and translation
        euler = mTransMtx.eulerRotation()    
        rotation = [math.degrees(angle) for angle in (euler.x, euler.y, euler.z)]
        trans = mTransMtx.translation(om.MSpace.kWorld)
        translation = [trans.x, trans.y, trans.z]
        return [translation, rotation]
    #end def get_worldSpace_values()

    def __current_keyframe(self, backward = True, keyframeOffset = 1.0):
        '''get the current keyframe by the given flags'''
        #--- current time
        omac = oma.MAnimControl()
        currentFrame = omac.currentTime()
        #--- go back in frame
        if backward:
            currentFrame = currentFrame - keyframeOffset
        return currentFrame.value()
    #end def __current_keyframe()

    def __get_attribute(self, node, attribute):
        '''get the atttributes'''
        mSel = om.MSelectionList()
        mSel.add(node)

        dagPath = om.MDagPath()
        mObj = om.MObject()    
        mSel.getDagPath(0, dagPath)
        mSel.getDependNode(0, mObj)    
        dgNode = om.MFnDagNode(dagPath)
        
        #--- get the attribute
        attr = dgNode.findPlug(attribute)
        return attr.name()
    #end def __get_attribute()
#end class SpaceSwitch()

def creator():
    '''get the pointer'''
    return mpx.asMPxPtr(SpaceSwitch())
#end def creator()

def initialize():
    '''initialize attributes'''
    nAttr = om.MFnNumericAttribute()
    msgAttr = om.MFnMessageAttribute()

    #--- output attribute
    SpaceSwitch.aOutput = nAttr.create('output', 'out', om.MFnNumericData.kInt)
    nAttr.setReadable(True)
    nAttr.setStorable(False)
    nAttr.setWritable(False)
    nAttr.setKeyable(False)
    SpaceSwitch.addAttribute(SpaceSwitch.aOutput)

    #--- driver attribute
    SpaceSwitch.aDriver = msgAttr.create('driver', 'drv')
    SpaceSwitch.addAttribute(SpaceSwitch.aDriver) 

    #--- driven attribute
    SpaceSwitch.aDriven = msgAttr.create('driven', 'drvn')
    SpaceSwitch.addAttribute(SpaceSwitch.aDriven)

    #--- locatorToDriver attribute
    SpaceSwitch.aLocatorToDrv = msgAttr.create('locatorToDriver', 'locDrv')
    SpaceSwitch.addAttribute(SpaceSwitch.aLocatorToDrv) 

    #--- aLocatorToDrvn attribute
    SpaceSwitch.aLocatorToDrvn = msgAttr.create('locatorToDriven', 'locDrvn')
    SpaceSwitch.addAttribute(SpaceSwitch.aLocatorToDrvn)   

    #--- aConstraint attribute
    SpaceSwitch.aConstraint = msgAttr.create('constraint', 'cns')
    SpaceSwitch.addAttribute(SpaceSwitch.aConstraint)

    #--- switch attribute
    SpaceSwitch.aSwitch = nAttr.create('switch', 'swi', om.MFnNumericData.kInt)
    nAttr.setKeyable(True)
    nAttr.setReadable(True)    
    nAttr.setWritable(True)    
    nAttr.setStorable(True)    
    nAttr.setMin(0)
    nAttr.setMax(1)
    SpaceSwitch.addAttribute(SpaceSwitch.aSwitch)
    SpaceSwitch.attributeAffects(SpaceSwitch.aSwitch, SpaceSwitch.aOutput)
#end def initialize()

def initializePlugin(mobject):
    '''register node'''
    fnPlugin = mpx.MFnPlugin(mobject)
    try:
        fnPlugin.registerNode(SpaceSwitch.nodeName, 
                              SpaceSwitch.nodeId, 
                              creator, 
                              initialize, 
                              mpx.MPxNode.kDependNode)
    except:
        sys.stderr.write('Failed to load plugin: ' + SpaceSwitch.nodeName)
#end def initializePlugin()

def uninitializePlugin(mobject):
    '''deregister node'''
    fnPlugin = mpx.MFnPlugin(mobject)
    try:
        fnPlugin.deregisterNode(SpaceSwitch.nodeId)
    except:
        sys.stderr.write('Failed to unload plugin: ' + SpaceSwitch.nodeName)
#end def uninitializePlugin()


