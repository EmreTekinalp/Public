import os
import sys
import time
from maya import cmds
from functools import wraps
rig_path = os.path.join('/local_home', os.getenv('USER'), 'workspace', 'rig')
if not os.path.isdir(rig_path):
    rig_path = os.path.join('/local_home', os.getenv('USER'), 'dev', 'rig')
sys.path.append(rig_path)
#from rigFunctions import attribute, name

############################################################################################################################
"""
With the ShotFinalTool you can create sculptMeshes you can deform and modify with the maya provided tools.
You need a scene with an AlembicAssets_GRP containing the cached alembicMeshes inside, which are connected to an alembicNode.
And you also need the referenced Characters. And then you are good to go with that tool.

Here are the steps to do:
   1. scrub to the frame, where the party is
   2. select the mesh, which causes you sleepless nights (it has to be a referenced mesh and just one selection)
   3. run this script
   4. a SHOTFINALING group has been created in the world (look at the outliner) and underneath is a transform node for every selected mesh separated by characters, which contains controls
   5. you have 4 attributes which increases, the more you go through the steps 1-4 above, but that's the cool thing.
   6. the TOOLS group is dynamically adding the blendshape setups, connections and attributes (but it still needs alot of tweaks)
   7. the first attribute is an on/off switch for the visibility of the original selected mesh
   8. the second attribute right underneath is the envelope of all blendShapes
   9. the third attribute called "Sculpt" is the on/off switch for the sculpt mesh, which you work on
  10. the fourth attribute called "BlendValue" is the weight of the blendshape. This attribute shall be keyed of course. :)
  11. the fifth attribute is just the keyframe, where you selected the mesh, just to have a better overview
  12. well, after you are finished, just grab a tasty turkish beer, called EFES and enjoy.


Besides here is the snippet for your shelf including the SF_interface:

from gui.shotFinaling import shotfinalingui
reload(shotfinalingui)

sf = shotfinalingui
sf.main()

Cheerio
turkish engineer
"""
#############################################################################################################################

def undoWrap(method):
    @wraps(method)
    def undoMethod(*args, **kwargs):
        try:
            cmds.undoInfo(openChunk = True)
            return method(*args, **kwargs)
        finally:
            cmds.undoInfo(closeChunk = True)
    return undoMethod


class ShotFinal():
    """
    EXCEPTION for cloudy's jaket has been written!!! Search for @EXCEPTION
    """
    def __init__(self, key = False, version = 2.0):
        #vars
        self.timeStamp          = []
        self.abc                = []
        self.alembicKids        = []
        self.alembicName        = []
        self.alembicCharacter   = []
        self.oldAlembicShapes   = []
        self.newAlembicShapes   = []
        self.oldAlembicMeshes   = []

        self.mesh               = []
        self.meshName           = []
        self.plugNum            = []

        self.charName           = []
        self.charGrp            = []
        self.currentFrame       = []

        self.shader             = []
        self.shaderSet          = []

        self.shotFinalGrp       = []
        self.mainBshpesGrp      = []
        self.negativeBshpesGrp  = []
        self.sculptBshpesGrp    = []
        self.resultBshpesGrp    = []
        self.engineersToolsGrp  = []
        self.doNotTouchGrp      = []

        self.meshBshpeNode      = []
        self.resultBshpeNode    = []

        self.negativeMesh       = []
        self.sculptMesh         = []
        self.resultMesh         = []

        self.eTools             = []
        self.subTools           = []

        #methods
        self.create(key = key, version = version)

    def checkScene(self):
        #check if something is selected
        sel = cmds.ls(selection = 1)
        if sel is None:
            raise Exception("You have to select a mesh, dude!")
        if len(sel) == 1:
            #check if selection is a mesh
            if 0==0:#sel[0][-3:] == "PLY":
                #store the mesh, the elementName of the mesh, the characterName and the characterGroupName
                self.mesh = sel[0]
                self.meshName = sel[0]
                self.charName = sel[0]
                self.charGrp = self.charName + "_GRP"

                #get current time and store it
                self.currentFrame = cmds.currentTime(query = 1)

                #check if royElementInfoNode exists
#                royElementInfo = self.charName + ":" + "RoyElementInfo"
#                if cmds.objExists(royElementInfo + ".element"):
#                    roy = cmds.getAttr(royElementInfo + ".element")
#                    if not roy == self.charName:
#                        raise Exception("Character " + self.charName +  " has no RoyElementInfoNode, dude! Cannot proceed!")
            else:
                raise Exception("The selected object is not a mesh with an alembic or it's not the original mesh, dude! Cannot proceed!")
        else:
            raise Exception("You have to select a mesh, dude!")

    def setupScene(self):
        #--- get the time
        ts = str(time.time())
        self.timeStamp = str(ts.split(".")[0] + ts.split(".")[1])

        #check if the shotFinal groups exist, else create them
        if cmds.objExists("SHOTFINALING"):
            self.engineersToolsGrp = "SHOTFINALING"
        else:
            self.engineersToolsGrp = cmds.createNode("transform", name = "SHOTFINALING")

        if cmds.objExists("BLENDSHAPES"):
            self.doNotTouchGrp = "BLENDSHAPES"
        else:
            self.doNotTouchGrp = cmds.createNode("transform", name = "BLENDSHAPES", parent = self.engineersToolsGrp)

        if cmds.objExists(self.charName + "_SHOTFINAL_GRP"):
            self.shotFinalGrp = self.charName + "_SHOTFINAL_GRP"
        else:
            self.shotFinalGrp = cmds.createNode("transform", name = self.charName + "_SHOTFINAL_GRP", parent = self.doNotTouchGrp)

        if cmds.objExists(self.charName + "_SF_BSHPES_GRP"):
            self.mainBshpesGrp = self.charName + "_SF_BSHPES_GRP"
        else:
            self.mainBshpesGrp = cmds.createNode("transform", name = self.charName + "_SF_BSHPES_GRP", parent = self.shotFinalGrp)

        if cmds.objExists(self.charName + "_SF_NEGATIVES_GRP"):
            self.negativeBshpesGrp = self.charName + "_SF_NEGATIVES_GRP"
        else:
            self.negativeBshpesGrp = cmds.createNode("transform", name = self.charName + "_SF_NEGATIVES_GRP", parent = self.mainBshpesGrp)

        if cmds.objExists(self.charName + "_SF_SCULPTS_GRP"):
            self.sculptBshpesGrp = self.charName + "_SF_SCULPTS_GRP"
        else:
            self.sculptBshpesGrp = cmds.createNode("transform", name = self.charName + "_SF_SCULPTS_GRP", parent = self.mainBshpesGrp)

        if cmds.objExists(self.charName + "_SF_RESULTS_GRP"):
            self.resultBshpesGrp = self.charName + "_SF_RESULTS_GRP"
        else:
            self.resultBshpesGrp = cmds.createNode("transform", name = self.charName + "_SF_RESULTS_GRP", parent = self.mainBshpesGrp)

    def setupBlendshapes(self):
        #create sculpt and negative duplicates from the current selected mesh
        self.sculptMesh = cmds.duplicate(self.mesh)
        cmds.parent(self.sculptMesh, self.sculptBshpesGrp)
        sculptName = cmds.rename(self.sculptMesh, self.charName + "_SF_" + self.meshName + "Sculpt" + self.timeStamp)
        sculptRel  = cmds.listRelatives(sculptName, allDescendents = 1, type = "shape")
        self.sculptMesh = sculptName

        self.negativeMesh = cmds.duplicate(self.mesh)
        cmds.parent(self.negativeMesh, self.negativeBshpesGrp)
        negativeName = cmds.rename(self.negativeMesh, self.charName + "_SF_" + self.meshName + "Negative" + self.timeStamp)
        negativeRel  = cmds.listRelatives(negativeName, allDescendents = 1, type = "shape")
        self.negativeMesh = negativeName

        #get the blendshape node of the selected mesh/alembic mesh
        alembicMesh = self.mesh

        # if not cmds.objExists(alembicMesh):
        #     #--- !!!!!!!!!!!@EXCEPTION!!!!!!!!!!!!!!!!!!!!!!!
        #     if cmds.objExists(alembicMesh.split("jaket_PLY")[0] + "jaketSimulated_PLY"):
        #         alembicMesh = alembicMesh.split("jaket_PLY")[0] + "jaketSimulated_PLY"
        #     #END !!!!!!!!!!!!@EXCEPTION!!!!!!!!!!!!!!!!!!
        # if not "_Alembic_Alembic:" in alembicMesh:
        #     alembicShape = cmds.listRelatives(alembicMesh, children = 1, type = "mesh")
        #     connections = cmds.listConnections(alembicShape, source = 1)
        #     for i in connections:
        #         print i
        #         if "blendShape" in i:
        #             self.meshBshpeNode = i
        #     #disable the envelope of the blendshapeNode to get the default/neutral pose of the selected mesh
        #     #cmds.setAttr(self.meshBshpeNode + ".envelope", 0)

        alembicShape = cmds.listRelatives(alembicMesh, children = 1, type = "mesh")
        connections = cmds.listConnections(alembicShape, source = 1)
        for i in connections:
            if "blendShape" in i:
                self.meshBshpeNode = i

        print  self.meshBshpeNode

        #duplicate the default, neutral mesh
        self.resultMesh = cmds.duplicate(self.mesh)
        cmds.parent(self.resultMesh,  self.resultBshpesGrp)
        resultName = cmds.rename(self.resultMesh, self.charName + "_SF_" + self.meshName + "Result" + self.timeStamp)
        resultRel  = cmds.listRelatives(resultName, allDescendents = 1, type = "shape")
        self.resultMesh = resultName

        #if "_Alembic_Alembic:" in alembicMesh:
            #self.meshBshpeNode = cmds.blendShape(self.resultMesh, self.mesh, name = self.charName + "_SF_" + self.meshName + "_Bshpe")[0]
        #else:
            #self.meshBshpeNode = cmds.blendShape(self.resultMesh, self.mesh, name = self.charName + "_SF_Bshpe")[0]
        #enable the envelope of the blendshapeNode to set the selected mesh to the initial state
        #cmds.setAttr(self.meshBshpeNode + ".envelope", 1)

        #create the sculpt and negative blendshapes and set them up
        self.resultBshpeNode = cmds.blendShape(self.sculptMesh, self.negativeMesh, self.resultMesh, name = self.charName + ":SF_" + self.meshName + "_Bshpe")[0]

        cmds.setAttr(self.resultBshpeNode + "." + self.sculptMesh, 1, lock = 1)
        cmds.setAttr(self.resultBshpeNode + "." + self.negativeMesh, -1, lock = 1)

        #get the targetIndex to create the blendShape
        plugList = []
        #shape = cmds.listRelatives(alembicMesh, fullPath=True, shapes=True)[0]
        #bls = cmds.listConnections(shape + ".inMesh")[0]
        # for i in cmds.listConnections(self.resultBshpeNode + ".inputTarget", plugs = 1):
        #     plugList.append(int(cmds.listConnections(i, d=1, plugs=1)[0].split(".")[2].split("[")[1].split("]")[0]))

        for plug in range(len(plugList)+1):
            if plug not in plugList:
                #--- check free plugs
                self.plugNum = str(plug)
                break
        #cmds.blendShape(self.meshBshpeNode , edit = True, target = (self.mesh, plug, self.resultMesh, 1.0))

    def setupSculptShader(self):
        #list all the shader names
        shaderList = ["sculptShaderGreen", "sculptShaderRed", "sculptShaderBlue", "sculptShaderPink", "sculptShaderYellow", "sculptShaderCyan"]

        meshNameOnly = self.meshName
        #check if shader exists, else create a new one
        for s in range(len(shaderList)):
            if cmds.objExists(shaderList[s]):
                #check which meshName is selected
                if meshNameOnly == "body" or meshNameOnly == "head":
                    self.shader = shaderList[0]
                    self.shaderSet = shaderList[0] + "3SG"
                elif meshNameOnly == "cloth" or meshNameOnly == "dress" or meshNameOnly == "jaket" or meshNameOnly == "jacket" or meshNameOnly == "shirt":
                    self.shader = shaderList[1]
                    self.shaderSet = shaderList[1] + "3SG"
                elif meshNameOnly == "pants" or meshNameOnly == "pant" or meshNameOnly == "mouth":
                    self.shader = shaderList[2]
                    self.shaderSet = shaderList[2] + "3SG"
                elif meshNameOnly == "hat":
                    self.shader = shaderList[3]
                    self.shaderSet = shaderList[3] + "3SG"
                elif meshNameOnly == "shoes" or meshNameOnly == "feet":
                    self.shader = shaderList[4]
                    self.shaderSet = shaderList[4] + "3SG"
                else:
                    self.shader = shaderList[5]
                    self.shaderSet = shaderList[5] + "3SG"
            else:
                if meshNameOnly == "body" or meshNameOnly == "head":
                    #create the lambert shader
                    self.shader    = cmds.shadingNode("lambert", asShader = 1, name = shaderList[0])
                    self.shaderSet = cmds.sets(self.shader, renderable = 1, noSurfaceShader = 1, empty = 1, name = shaderList[0] + "3SG")
                    cmds.connectAttr(self.shader + ".outColor", self.shaderSet + ".surfaceShader", force = 1)
                elif meshNameOnly == "cloth" or meshNameOnly == "dress" or meshNameOnly == "jaket" or meshNameOnly == "jacket" or meshNameOnly == "shirt":
                    #create the lambert shader
                    self.shader    = cmds.shadingNode("lambert", asShader = 1, name = shaderList[1])
                    self.shaderSet = cmds.sets(self.shader, renderable = 1, noSurfaceShader = 1, empty = 1, name = shaderList[1] + "3SG")
                    cmds.connectAttr(self.shader + ".outColor", self.shaderSet + ".surfaceShader", force = 1)
                elif meshNameOnly == "pants" or meshNameOnly == "pant" or meshNameOnly == "mouth":
                    #create the lambert shader
                    self.shader    = cmds.shadingNode("lambert", asShader = 1, name = shaderList[2])
                    self.shaderSet = cmds.sets(self.shader, renderable = 1, noSurfaceShader = 1, empty = 1, name = shaderList[2] + "3SG")
                    cmds.connectAttr(self.shader + ".outColor", self.shaderSet + ".surfaceShader", force = 1)
                elif meshNameOnly == "hat":
                    #create the lambert shader
                    self.shader    = cmds.shadingNode("lambert", asShader = 1, name = shaderList[3])
                    self.shaderSet = cmds.sets(self.shader, renderable = 1, noSurfaceShader = 1, empty = 1, name = shaderList[3] + "3SG")
                    cmds.connectAttr(self.shader + ".outColor", self.shaderSet + ".surfaceShader", force = 1)
                elif meshNameOnly == "shoes" or meshNameOnly == "feet":
                    #create the lambert shader
                    self.shader    = cmds.shadingNode("lambert", asShader = 1, name = shaderList[4])
                    self.shaderSet = cmds.sets(self.shader, renderable = 1, noSurfaceShader = 1, empty = 1, name = shaderList[4] + "3SG")
                    cmds.connectAttr(self.shader + ".outColor", self.shaderSet + ".surfaceShader", force = 1)
                else:
                    #create the lambert shader
                    self.shader    = cmds.shadingNode("lambert", asShader = 1, name = shaderList[5])
                    self.shaderSet = cmds.sets(self.shader, renderable = 1, noSurfaceShader = 1, empty = 1, name = shaderList[5] + "3SG")
                    cmds.connectAttr(self.shader + ".outColor", self.shaderSet + ".surfaceShader", force = 1)

        #get the mesh name
        if meshNameOnly == "body" or meshNameOnly == "head":
            #change the color to green
            cmds.setAttr(self.shader + ".color", 0, 1, 0)
            #assign the shader to the sculptMesh
            cmds.sets(self.sculptMesh, forceElement = self.shaderSet)

        elif meshNameOnly == "cloth" or meshNameOnly == "dress" or meshNameOnly == "jaket" or meshNameOnly == "jacket" or meshNameOnly == "shirt":
            #change the color to red
            cmds.setAttr(self.shader + ".color", 1, 0, 0)
            #assign the shader to the sculptMesh
            cmds.sets(self.sculptMesh, forceElement = self.shaderSet)

        elif meshNameOnly == "pants" or meshNameOnly == "pant" or meshNameOnly == "mouth":
            #change the color
            cmds.setAttr(self.shader + ".color", 0, 0, 1)
            #assign the shader to the sculptMesh
            cmds.sets(self.sculptMesh, forceElement = self.shaderSet)

        elif meshNameOnly == "hat":
            #change the color
            cmds.setAttr(self.shader + ".color", 1, 0, 1)
            #assign the shader to the sculptMesh
            cmds.sets(self.sculptMesh, forceElement = self.shaderSet)

        elif meshNameOnly == "shoes" or meshNameOnly == "feet":
            #change the color
            cmds.setAttr(self.shader + ".color", 1, 1, 0)
            #assign the shader to the sculptMesh
            cmds.sets(self.sculptMesh, forceElement = self.shaderSet)

        else:
            #change the color
            cmds.setAttr(self.shader + ".color", 0, 1, 1)
            #assign the shader to the sculptMesh
            cmds.sets(self.sculptMesh, forceElement = self.shaderSet)

    def setupShotFinalControls(self):
        #check if shotFinaling Tools exists
        if cmds.objExists(self.meshName + "_SHOTFINALING_TOOLS"):
            self.eTools = self.meshName + "_SHOTFINALING_TOOLS"
            if cmds.objExists(self.meshName + "_TOOLS"):
                self.subTools = self.meshName + "_TOOLS"
            else:
                self.subTools = cmds.createNode("transform", name = self.meshName + "_TOOLS", parent = self.eTools)
        else:
            self.eTools   = cmds.createNode("transform", name = self.meshName + "_SHOTFINALING_TOOLS", parent = self.engineersToolsGrp)
            self.subTools = cmds.createNode("transform", name = self.meshName + "_TOOLS", parent = self.eTools)

        #create the sculptTools and parent them under the subTools
        if cmds.objExists(self.meshName + self.plugNum):
            self.sculptTools = cmds.createNode("transform", name = self.meshName + self.plugNum, parent = self.subTools)
            #self.meshName + self.plugNum
        else:
            self.sculptTools = cmds.createNode("transform", name = self.meshName + self.plugNum, parent = self.subTools)

        #remove all unnecessary transform attributes
        for axis in "xyz":
            cmds.setAttr(self.subTools + ".t" + axis, lock = 1, keyable = 0)
            cmds.setAttr(self.subTools + ".r" + axis, lock = 1, keyable = 0)
            cmds.setAttr(self.subTools + ".s" + axis, lock = 1, keyable = 0)
            cmds.setAttr(self.sculptTools + ".t" + axis, lock = 1, keyable = 0)
            cmds.setAttr(self.sculptTools + ".r" + axis, lock = 1, keyable = 0)
            cmds.setAttr(self.sculptTools + ".s" + axis, lock = 1, keyable = 0)
        cmds.setAttr(self.sculptTools + ".v", lock = 1, keyable = 0)
        cmds.setAttr(self.sculptTools + ".v", lock = 1, keyable = 0)

        #create the attributes for the engineersTools group
        if not cmds.objExists(self.subTools + "." + self.meshName):
            cmds.addAttr(self.subTools, longName = self.meshName, shortName = self.meshName, attributeType = "short", min = 0, max = 1, defaultValue = 1, keyable = 1)
            cmds.setAttr(self.subTools + "." + self.meshName, edit = 1, channelBox = 1)

        if not cmds.objExists(self.subTools + "." + self.meshName + "_ENVELOPE"):
            cmds.addAttr(self.subTools, longName = self.meshName + "_ENVELOPE", shortName = self.meshName + "_ENVELOPE", attributeType = "float", min = 0.0, max = 1.0, defaultValue = 1.0, keyable = 1)
            cmds.setAttr(self.subTools + "." + self.meshName + "_ENVELOPE", edit = 1, channelBox = 1)

        cmds.addAttr(self.sculptTools, longName = "sculpt", shortName = "scu", niceName = "sculpt", attributeType = "short", min = 0, max = 1, defaultValue = 1, keyable = 1)
        cmds.addAttr(self.sculptTools, longName = "blendValue", shortName = "bv", niceName = "blendValue", attributeType = "double", min = 0, max = 1, defaultValue = 0, keyable = 1)
        cmds.addAttr(self.sculptTools, longName = "frameNumber", shortName = "fn", niceName = "frameNumber", attributeType = "float")
        cmds.setAttr(self.sculptTools + "." + "frameNumber", self.currentFrame, edit = 1, channelBox = 1, lock = 1)

        #connect the eTool attributes with the bshpe attributes
        if not cmds.isConnected(self.subTools + "." + self.meshName, self.mesh + ".v"):
            cmds.connectAttr(self.subTools + "." + self.meshName, self.mesh + ".v", force = 1)
        cmds.connectAttr(self.sculptTools + "." + "sculpt", self.sculptMesh + ".v")
        #if cmds.objExists(self.meshBshpeNode + "." + self.resultMesh.split(":")[1]):
         #   cmds.connectAttr(self.sculptTools + "." + self.meshName + "_BlendValue", self.meshBshpeNode + "." + self.resultMesh.split(":")[1])

        #check if the envelope of the blendShapes is connected with the sculptTools envelope attribute
        """
        sel = cmds.ls(self.resultBshpeNode.split("Bshpe")[0] + "Bshpe*", type = "blendShape")
        if sel:
            for i in sel:
                if not cmds.isConnected(self.subTools + "." + self.meshName + "_ENVELOPE", i + ".envelope"):
                    #connect the envelope of the blendShapes with the sculptTools envelope attribute
                    cmds.connectAttr(self.subTools + "." + self.meshName + "_ENVELOPE", i + ".envelope")
        """
        #disable the selected mesh's visibility
        cmds.setAttr(self.subTools + "." + self.meshName, 0)
        cmds.setAttr(self.subTools + "." + self.meshName + "_ENVELOPE", 1)

    def setKeyframe(self):
        #get the attributeNumber of the selected sculpt
#        toInt = self.sculptMesh.split("Sculpt")[1]
#        if not toInt:
#            toInt = 0
#        count = int(toInt) + 1

        #get current time
        self.currentFrame

        #set keyFrame at current time
        cmds.setKeyframe(self.sculptTools + "." + "blendValue", value = 1)

    def setKeyframeAtFrame(self):
        #this method sets a keyframe on the current frame with a value of 1
        #and sets on the frames before and after a keyframe with a value of 0
        self.currentFrame
        cmds.setKeyframe(self.sculptTools + "." + "blendValue", value = 1)
        pre = self.currentFrame -1
        cmds.setKeyframe(self.sculptTools + "." + "blendValue", value = 0)
        post = self.currentFrame + 2
        cmds.currentTime(post)
        cmds.setKeyframe(self.sculptTools + "." + "blendValue", value = 0)
        cmds.currentTime(self.currentFrame)

    def cleanup(self, version = 2.0):
        #hide groups and lock attributes
        cmds.setAttr(self.negativeBshpesGrp + ".v", 0)
        cmds.setAttr(self.resultBshpesGrp + ".v", 0)

        for i in cmds.ls(self.eTools, self.engineersToolsGrp, self.doNotTouchGrp, self.shotFinalGrp, self.mainBshpesGrp, self.negativeBshpesGrp, self.sculptBshpesGrp, self.resultBshpesGrp, "*Negative*", "*Sculpt*", "*Result*"):
            try:
                for axis in "xyz":
                    cmds.setAttr(i + ".t" + axis, lock = 1, keyable = 0)
                    cmds.setAttr(i + ".r" + axis, lock = 1, keyable = 0)
                    cmds.setAttr(i + ".s" + axis, lock = 1, keyable = 0)
                cmds.setAttr(i + ".v", keyable = 0)
                cmds.setAttr(i + ".ihi", 0)
            except:
                pass

        #hide isHistoricallyInteresting
        for i in cmds.ls("blendShape*", "tweak*"):
            cmds.setAttr(i + ".ihi", 0)


        #add versionNumber of the SHOTFINAL script
        if not cmds.objExists(self.engineersToolsGrp + ".version"):
            cmds.addAttr(self.engineersToolsGrp, longName = "version", shortName = "version", attributeType = "float", keyable = 1)
            cmds.setAttr(self.engineersToolsGrp + ".version", version, edit  = 1, channelBox = 1, lock = 1)


        #select the engineersTools group
        cmds.select(self.sculptTools)

    @undoWrap
    def create(self, key = False, version = 2.0):
        self.checkScene()
        self.setupScene()
        self.setupBlendshapes()
        self.setupSculptShader()
        self.setupShotFinalControls()
        if key:
            self.setKeyframeAtFrame()
        else:
            self.setKeyframe()
        self.cleanup(version = version)

class RemoveShotFinal():
    """
    EXCEPTION has been written for Cloudy_jaketSimulated to remove it! Search
    for "EXCEPTION"!!!
    """
    def __init__(self):
        #vars

        #methods
        self.__create()

    def removeSculpt(self):
        #store the selected sculpt in a list
        sel = cmds.ls(selection = 1)
        #check if something is selected
        if sel:
            #check if selection is a sculpt mesh
            for i in sel:
                if "Sculpt" in i:
                    #get the attributeNumber of the selected sculpt
#                    toInt = i.split("Sculpt")[1]
#                    if not toInt:
#                        toInt = 0
#                    count = int(toInt) + 1
                    count = i.split("Sculpt")[1]
                    #get the result mesh to get the blendShape node
                    resultMesh = i.split("Sculpt")[0] + "Result" + i.split("Sculpt")[1]
                    #check if result mesh exists
                    if cmds.objExists(resultMesh):
                        #get the shape of the resultMesh
                        resultShape = cmds.listRelatives(resultMesh, allDescendents = 1)
                        #get the blendShape node
                        connections = cmds.listConnections(resultShape)
                        bshape  = []
                        refMesh = []
                        for cnt in connections:
                            if "blendShape" in cnt:
                                bshape.append(cnt)
                                #get the referenced mesh
                                mesh = cmds.listConnections(cnt, type = "mesh")
                                for m in mesh:
                                    if "Alembic" in m:
                                        refMesh.append(m.split("_Alembic")[0] + m.split("_Alembic")[1])

                        #get the sculptTool
                        tool = cmds.listConnections(i)[0]

                        #check if meshes exist and delete them
                        deleteList = [i, i.split("Sculpt")[0] + "Negative" + i.split("Sculpt")[1], resultMesh]
                        for d in deleteList:
                            if cmds.objExists(d):
                                #remove the blendShape Target
                                #@EXCEPTION!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                if refMesh:
                                    #get the target index
                                    index = cmds.blendShape(bshape, query = 1, target = 1).index(resultMesh)
                                    if not cmds.objExists(refMesh[0]):
                                        refMesh = [refMesh[0].split("Simulated_PLY")[0] + "_PLY"]
                                    #@END OF EXCEPTION!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                    cmds.blendShape(bshape[0], edit = 1, topologyCheck = 0, remove = 1, target = ((refMesh[0], index, resultMesh, 1),(refMesh[0], index, refMesh[0], 1)))
                                    #remove the sculpt, negative and result mesh
                                cmds.delete(i, i.split("Sculpt")[0] + "Negative" + i.split("Sculpt")[1], resultMesh)

                        #delete the sculptTool
                        if not cmds.objExists(i):
                            if not "_TOOLS" in tool:
                                cmds.delete(tool)

                        #get the ShotFinal Tool name
                        toolMain = i.split("Sculpt")[0].split("SF_")[1] + "_TOOLS"
                        if cmds.listRelatives(toolMain, children = 1):
                            #get the first attribute (upperCase) of the toolMain and enable its visibility
                            firstAttrName = i.split("Sculpt")[0].split("SF_")[1]
                            cmds.setAttr(toolMain + "." + firstAttrName, 1)
                            #check if there are children inside
                            if not cmds.listRelatives(toolMain, children = 1):
                                toolGrp = cmds.listRelatives(toolMain, parent = 1, type = "transform")
                                #delete the toolMain
                                mainAttr = cmds.listAttr(toolMain, channelBox = 1)
                                if len(mainAttr) > 2:
                                    break
                                else:
                                    cmds.delete(toolMain)
                                #check if there are other tools inside that group
                                toolChild = cmds.listRelatives(toolGrp[0], children = 1)
                                if not toolChild:
                                    #get the blendShape group
                                    bspGrp = tool.split(":")[0] + ":SHOTFINAL_GRP"
                                    #check if there are any meshes inside the group
                                    bspChild = cmds.listRelatives(bspGrp, allDescendents = 1, type = "mesh")
                                    if not bspChild:
                                        cmds.delete(bspGrp)
                                    cmds.delete(toolGrp)
                                    #check if BLENDSHAPES group is empty
                                    if not cmds.listRelatives("BLENDSHAPES", children = 1):
                                        cmds.delete("BLENDSHAPES")
                                    #check if SHOTFINALING group is empty
                                    if not cmds.listRelatives("SHOTFINALING", children = 1):
                                        cmds.delete("SHOTFINALING")
                            else:
                                continue
                        else:
                            if cmds.objExists(i.split("Sculpt")[0].split("SF_")[0] + i.split("Sculpt")[0].split("SF_")[1] + "_ENGINEERSTOOLS"):
                                tool = i.split("Sculpt")[0].split("SF_")[0] + i.split("Sculpt")[0].split("SF_")[1] + "_ENGINEERSTOOLS"
                            elif cmds.objExists(i.split("Sculpt")[0].split("SF_")[0] + i.split("sculpt")[0].split("SF_")[1] + "_TOOLS"):
                                tool = i.split("Sculpt")[0].split("SF_")[0] + i.split("Sculpt")[0].split("SF_")[1] + "_TOOLS"
                                #get all attrs of the tool(except the first attribute), unlock and delete them
                                toolAttrs = []
                                keyable = cmds.listAttr(tool, keyable = 1)
                                locked  = cmds.listAttr(tool, locked = 1, channelBox = 1)
                                if keyable:
                                    for k in keyable:
                                        if "sculpt" + str(count) in k or "blendValue" + str(count) in k:
                                            toolAttrs.append(k)
                                if locked:
                                    for l in locked:
                                        if "frameNumber" + str(count) in l or l.split("_")[0] + str(count) in l:
                                            toolAttrs.append(l)
                                if toolAttrs:
                                    for t in toolAttrs:
                                        if cmds.objExists(tool + "." + t):
                                            cmds.setAttr(tool + "." + t, lock = 0)
                                            cmds.deleteAttr(tool + "." + t)

                                #get the first attribute (upperCase) of the tool and enable its visibility
                                firstAttrName = i.split("sculpt")[0].split("SF_")[1]
                                cmds.setAttr(tool + "." + firstAttrName, 1)

                                #delete the toolBox if there is just the first and second attribute left
                                listToolAttr = cmds.listAttr(tool, channelBox = 1)
                                if len(listToolAttr) == 2:
                                    if listToolAttr[0] == firstAttrName:
                                        #get the parent group of the tool
                                        toolGrp = cmds.listRelatives(tool, parent = 1, type = "transform")
                                        #delete the tool
                                        cmds.delete(tool)
                                        #check if there are other tools inside that group
                                        toolChild = cmds.listRelatives(toolGrp[0], children = 1)
                                        if not toolChild:
                                            #get the blendShape group
                                            bspGrp = tool.split(":")[0] + ":SHOTFINAL_GRP"
                                            #check if there are any meshes inside the group
                                            bspChild = cmds.listRelatives(bspGrp, allDescendents = 1, type = "mesh")
                                            if not bspChild:
                                                cmds.delete(bspGrp)
                                            cmds.delete(toolGrp)
                                            #check if BLENDSHAPES group is empty
                                            if not cmds.listRelatives("BLENDSHAPES", children = 1):
                                                cmds.delete("BLENDSHAPES")
                                            #check if SHOTFINALING group is empty
                                            if not cmds.listRelatives("SHOTFINALING", children = 1):
                                                cmds.delete("SHOTFINALING")
                    else:
                        raise Exception("Result mesh: " + resultMesh + " does not exist!")
                else:
                    raise Exception("Selected mesh: " + i + " is not a sculpt mesh!")
        else:
            raise Exception("Nothing is selected! Please, select a sculpt mesh!")

    def __create(self):
        self.removeSculpt()


class AlembicUpdate():
    """
    DONE
    """
    def __init__(self):
        #vars
        self.abc                = []
        self.abcNode            = []
        self.alembicKids        = []
        self.alembicName        = []
        self.alembicCharacter   = []
        self.alembicPath        = []
        self.latestDir          = []
        self.shot               = []
        self.oldAlembicShapes   = []
        self.newAlembicShapes   = []
        self.oldAlembicMeshes   = []

    def getLatestAlembics(self):
        #check if alembics grp exists
        if cmds.objExists("AlembicAssets_GRP"):
            #get the children of the AlembicAssetsGrp
            self.alembicKids = cmds.listRelatives("AlembicAssets_GRP", children = 1)
            #get the shapes of meshes inside the children groups
            for shape in self.alembicKids:
                #get and store the names of the alembicGroups
                self.alembicName.append(shape.split(":")[1])
                shapes = cmds.listRelatives(shape, allDescendents = 1, type = "shape")
                #store the old alembicShapes
                for shp in shapes:
                    connection = cmds.listConnections(shp, source = 1)
                    for c in connection:
                        if "AlembicNode" in c:
                            mesh = cmds.listRelatives(shp, parent = 1)
                            self.oldAlembicShapes.append(shp)
                            self.oldAlembicMeshes.append(mesh[0])

            #get the main character names inside the alembicAssetGrp
            for i in self.alembicKids:
                self.alembicCharacter.append(i.split("_Alembic")[0])

            #get the current scene name and store it
            currentSceneName = cmds.file(query = 1, sceneName = 1, shortName = 1)

            #get the current full scene path and store it
            currentPath = cmds.file(query = 1, sceneName = 1)

            #filter the current shot number
            currentShot = currentSceneName.split("_sht")[0]

            #get the mainRootPath from the current scene
            mainPath = currentPath.split("//Rocky")[1].split("ShotFinal")[0]

            #get the path to the alembic folder
            alembicPath = mainPath + "Cloth/Release/Alembic"
            self.alembicPath.append(alembicPath)

            #list the directories inside the alembicFolder
            listDir = os.listdir(alembicPath)
            if listDir:
                #get the latest directory inside the alembics folder
                self.latestDir = sorted(listDir)[-1]

                #list the alembic files inside the latest directory
                alembicFiles = os.listdir(alembicPath + "/" + self.latestDir)

                #get and store the alembicFilePaths
                for abc in alembicFiles:
                    self.abc.append("/Rocky" + alembicPath + "/" + self.latestDir + "/" + abc)
            else:
                raise Exception("There is no existing Alembic_cache: " + alembicPath)

        else:
            raise Exception("There is no AlembicAssets_GRP")

    def updateAlembics(self):
        #create a tempGroup to parent the alembics inside
        tmpGrp = cmds.createNode("transform", name = "tmpAlembic_GRP")

        #import the alembics and store the newAlembicShapes
        for abc in self.abc:
            alembics = cmds.AbcImport(abc, reparent = tmpGrp, createIfNotFound = 1, removeIfNoUpdate = 1, mode = "import")

        #check which group is hidden and which is not
        hideList = []
        for i in self.alembicKids:
            getVis = cmds.getAttr(i + ".v")
            if getVis == False:
                hideList.append(i)

        #match the order of the imported alembics with the order of existing ones in the alembicAsset_GRP
        tmpChildren = cmds.listRelatives(tmpGrp, children = 1, type = "transform")
        orderedKids = []
        for kid in self.alembicKids:
            for newKid in tmpChildren:
                if (":" + kid.split(":")[-1]) in ":" + newKid:
                    if kid.split(":")[-1] == newKid:
                        orderedKids.append(newKid)
                    else:
                        for char in hideList:
                            if char.split(":")[-1] in newKid:
                                if ":" in newKid:
                                    sel = cmds.ls(newKid)
                                    for i in sel:
                                        if "tmpAlembic_GRP" in i:
                                            tmp = i
                                    newKid = cmds.rename(tmp, newKid.split(":")[1])
                                orderedKids.append(newKid)

        tmpShapes = []
        bspNodes = []
        #connect the blendshapes with the imported alembics
        for i, j in zip(orderedKids, self.alembicKids):
            #create tmp namespaces based on existing characters
            charName = cmds.namespace(add = j.split("_Alembic")[0] + "_TMP")
            #list all shapes in the alembicAsset_GRP
            oldShapes = cmds.listRelatives(j, allDescendents = 1, type = "shape", fullPath = 1)
            #list all shapes from the imported alembics
            newShapes = cmds.listRelatives(i, allDescendents = 1, type = "shape", fullPath = 1)
            #get the transforms of the new imported alembic shapes and give them the tmp namespace
            for kid, old in zip(newShapes, oldShapes):
                newMeshes = cmds.listRelatives(kid, parent = 1, fullPath = 1)
                if ":" in newMeshes[0]:
                    new = cmds.rename(newMeshes, charName + ":" + newMeshes[0].split(":")[-1])
                else:
                    new = cmds.rename(newMeshes, charName + ":" + newMeshes[0].split("|")[-1])
                #get the blendshapeNode of the old alembic shapes and reconnect with the new ones
                connection = cmds.listConnections(old, source = 1)
                for bsp in connection:
                    if "blendShape" in bsp:
                        shapes = cmds.listRelatives(new, allDescendents = 1, type = "shape", fullPath = 1)
                        if cmds.objExists(new + "Shape"):
#                            shapes = shapes[0].split("|")[-1]
                            shapes = old.split("|")[-1].split("Alembic")[0] + "TMP" + old.split("|")[-1].split("Alembic")[1]
                        else:
                            shapes = cmds.rename(shapes[0], new + "Shape")
                        tmpShapes.append(shapes)
                        bspNodes.append(bsp)
        for tmp, bsp in zip(tmpShapes, bspNodes):
            cmds.connectAttr(tmp + ".worldMesh[0]", bsp + ".inputTarget[0].inputTargetGroup[0].inputTargetItem[6000].inputGeomTarget", force = 1)

        #delete all the content of the alembicAssets_GRP
        cmds.delete(self.alembicKids)

        #reparent the new alembics from the tmpGrp to the alembicAssets_GRP
        cmds.parent(orderedKids, "AlembicAssets_GRP")

        #rename the content groups of the alembicAssets_GRP with the _TMP: namespace
        for i, j in zip(self.alembicKids, orderedKids):
            newAlembics = cmds.rename(j, i)
            listAll = cmds.listRelatives(newAlembics, allDescendents = 1)
            for rnm in listAll:
                if not ":" in rnm:
                    tmpName = newAlembics.split("Alembic")[0] + "TMP:"
                    if not cmds.objExists(tmpName):
                        sel = cmds.ls(rnm + "*", ap = 1)
                        if len(sel) > 1:
                            for s in sel:
                                if "_TMP:" in s:
                                    if "|" in s:
                                        renamed = cmds.rename(s, s.split("|")[0].split(":")[0] + ":" + s.split("|")[-1])
                                elif "|" in s:
                                    mainRoot = cmds.listRelatives(s, allParents = 1)
                                    if ":" in mainRoot[0]:
                                        renamed = cmds.rename(s, mainRoot[0].split(":")[-1] + "_TMP:" + s.split("|")[-1])
                                    else:
                                        if ":" in s:
                                            renamed = cmds.rename(s, s.split("_Alembic:")[0] + "_TMP:" + s.split("|")[-1])
                                        else:
                                            if "|" in s:
                                                if "_" in s.split("|")[0]:
                                                    renamed = cmds.rename(s, mainRoot[0].split("_")[0] + "_TMP:" + s.split("|")[-1])
                                                else:
                                                    renamed = cmds.rename(s, s.split("|")[0] + "_TMP:" + s.split("|")[-1])
                                            elif "_" in mainRoot[0]:
                                                renamed = cmds.rename(s, mainRoot[0].split("_")[0] + "_TMP:" + s.split("|")[-1])
                                            else:
                                                renamed = cmds.rename(s, s.split("|")[0] + "_TMP:" + s.split("|")[-1])
                                else:
                                    mainRoot = cmds.listRelatives(s, allParents = 1)
                                    if ":" in mainRoot[0]:
                                        renamed = cmds.rename(s, mainRoot[0].split(":")[-1] + "_TMP:" + s)
                                    else:
                                        if not cmds.objExists(mainRoot[0].split("_")[0] + "_TMP:" + s):
                                            renamed = cmds.rename(s, mainRoot[0].split("_")[0] + "_TMP:" + s)
                        else:
                            for s in sel:
                                if "|" in s:
                                    relatives = cmds.listRelatives(s, fullPath = 1)
                                    if relatives:
                                        new = cmds.rename(s, tmpName + rnm)
                                else:
                                    new = cmds.rename(s, tmpName + s)
                                if "|" in new:
                                    new = cmds.rename(new, new.split("|")[-2].split("_")[0] + "_TMP" + new.split("|")[-1].split("_TMP")[-1])

        #check the existing namespace
        nSpace = cmds.namespaceInfo(lon = 1)
        nameSpaces = []
        for n in nSpace:
            if "_Alembic" in n:
                nameSpaces.append(n)

        #get all the _TMP: namespace named nodes and rename them
        temp = cmds.ls("*_TMP:*", type = "transform")
        for i in temp:
            newNameSpace = i.split("_TMP")[0] + "_Alembic"
            for n in nameSpaces:
                if n in i.split("_TMP")[0] + "_Alembic" + i.split("_TMP")[1]:
                    newNSpace = n
            cmds.rename(i, newNSpace + i.split("_TMP")[1])
        #delete the tmpGrp
        cmds.delete(tmpGrp)

        #check if _TMP: namespace exists and remove it
        for i in self.alembicCharacter:
            if cmds.namespace(exists = i + "_TMP"):
#                print '>>>>>>>>>>>>>>>>>>>>', i + "_TMP"
                bla = cmds.ls(i + "_TMP", r = 1)
                print bla
                cmds.namespace(removeNamespace = i + "_TMP")

        #hide the groups from the hideList
        for i in hideList:
            cmds.setAttr(i + ".v", 0)

        cmds.select(clear = 1)
        print "Alembic Import: " + self.latestDir + " was successful! Drinks for free!!!"

    def currentAlembicInfo(self):
        #get current alembic info
        self.abcNode = cmds.ls(type = "AlembicNode")
        #current shot info
        self.shot = self.abcNode[0].split("_sim_rls")[0].split("_" + self.abcNode[0].split("_sim_rls")[0].split("_")[-1])[0].split("D_")[1]
        print "shot: " + self.shot + "\n"
        for abc in self.abcNode:
            print "current alembics: " + abc

    def updatedAlembicInfo(self):
        #get latest alembic info
        self.getLatestAlembics()

        latestVersionNumber = self.latestDir.split("_")[-1]
        shotInfo = self.latestDir.split("_sim_rls_")[0].split("7D_")[1]

        print "shot: " + shotInfo + "\n"

        latestVersionNumber = self.latestDir.split("_")[-1]
        shotInfo = self.latestDir.split("_sim_rls_")[0].split("7D_")[1]

        print "alembic version: " + latestVersionNumber + "\n"
        for char in self.alembicCharacter:
            print "alembic character: " + char
        print "\n" + "alembic path: " + self.alembicPath[0] + "\n"

        #compare the updated alembic nodes with the old ones
        updatedAbcNode = cmds.ls(type = "AlembicNode")
        #check len of the old and new abc lists
        abcNode = self.abcNode
        if len(updatedAbcNode) == len(abcNode):
            for new, old in zip(updatedAbcNode, abcNode):
                if not old in new:
                    print "UPDATE: " + new
                else:
                    continue
            print "\n" + "alembic version: " + latestVersionNumber + " is up to date!"
        else:
            #get the new and old alembics and list them
            for new in updatedAbcNode:
                print "newest alembics: " + new
            for old in abcNode:
                print "oldest alembics: " + old

    def update(self):
        self.getLatestAlembics()
        self.updateAlembics()

def followCam(remove = False):
    if remove:
        cmds.delete("C_followCam*_GRP")
        return

    sels = cmds.ls(sl = 1, dag = 1, g = 1, ni = 1)
    faceIndex = 0
    if not sels:
        sels = cmds.ls(sl = 1)

        if not sels:
            raise Exception("Nothing selected")

        if ".f" in sels[0]:
            faceIndex = int(sels[0].split("[")[1].split("]")[0])
            sels[0] = sels[0].split(".")[0]
            sels[0] = cmds.ls(sels[0], dag = 1, g = 1, ni = 1)[0]

    if not sels:
        raise Exception("Nothing selected")

    meshParent = cmds.listRelatives(sels[0], parent = 1)[0]
    mesh = sels[0]
    nameSpace = meshParent.split(":")

    if len(nameSpace) < 2:
        nameSpace[0] = "char"

    uniqueName = "C_followCam" + nameSpace[0] + "_GRP"
    uniqueName = name.uniqueName(uniqueName)

    camGrp = cmds.createNode("transform", n = "C_" + uniqueName + "_GRP")
    camParent = cmds.createNode("transform", n = "C_" + uniqueName + "_TRN", parent = camGrp)
    cam = cmds.createNode("camera", parent = camParent, n = "C_" + uniqueName + "_TRNShape")

    cmds.setAttr(camParent + ".ty", 2)
    cmds.setAttr(camParent + ".rx", -90)
    cmds.setAttr(camParent + ".ry", 90)
    rvt = cmds.createNode("n_meshRivet", n = nameSpace[0] + "_" + uniqueName + "_RVT")
    cmds.setAttr(rvt + ".faceIndex", faceIndex)
    cmds.connectAttr(mesh + ".worldMesh", rvt + ".inMesh")

    cmds.connectAttr(rvt + ".position", camGrp + ".t")
    cmds.connectAttr(rvt + ".outRotation", camGrp + ".r")

    cmds.select(camParent)
    return camParent

def lookThroughLeftShotCam():
    from maya import mel
    cam = cmds.ls("*:*:stereoCameraLeft")
    if not cam:
        raise Exception("No stereo left cam found")

    cam = cam[0]

    #figure out the focused viewport
#    panel = cmds.getPanel(underPointer = 1)
#    if not panel:
#        panel = cmds.getPanel(withFocus = 1)
    panel = cmds.getPanel(withFocus = 1)
    panelType = cmds.getPanel(typeOf = panel)

    if not panelType == "modelPanel":
        raise Exception("No active modelPanel")

    mel.eval("lookThroughModelPanel " + cam +  "Shape " + panel)
