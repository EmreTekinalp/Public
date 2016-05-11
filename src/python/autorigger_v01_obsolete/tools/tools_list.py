from maya import cmds

def groupMeshes():
    sel = cmds.ls(selection = 1, type = 'transform')        
    for i in sel:
        grpSel = cmds.listRelatives(i, parent = 1)
        grp = cmds.createNode('transform')
        grpName = i.replace("_PLY", "_OFF")
        grpNew = cmds.rename(grp, grpName)
        cmds.parent(i, grpNew)
        cmds.parent(grpName, grpSel)    
groupMeshes()    


from maya import cmds

sel = cmds.ls(sl = 1, fl = 1)
print sel
for i in sel:
    child = cmds.listRelatives(i, allDescendents = 1)
    xPos = cmds.xform(i, q = 1, ws = 1, rp = 1)
    xRot = cmds.xform(i, q = 1, ws = 1, ro = 1)
    #xOrd = cmds.xform(i, q = 1, ws = 1, roo = 1) 
    #cSize = cmds.getAttr(child[0] +'.size')
    #cDraw = cmds.getAttr(child[0] +'.drawStyle')
    #cOrie = cmds.getAttr(child[0] +'.orientation')    
    #print xPos
    print xRot   
    #print xOrd
    #print cSize
    #print cDraw
    #print cOrie



from maya import cmds


def set_vertex_position(getVtxPosOfFrame = 101):
    '''
    This method sets the vertex positions 
    of the mesh by the vertex positions at the 
    specified frameNumber 
    '''

    #Cloudy:SF_C_hatSculpt138918980693
    #Cloudy:C_hat_PLY

    #--- get the selected object
    sel = cmds.ls(selection = True)
    #--- get the current frame
    current_frame = cmds.currentTime(query = True)
    #--- jump to the specified frame
    cmds.currentTime(getVtxPosOfFrame)

    #--- get the vertex positions of the selected mesh
    for i in sel:
        #--- get the original mesh, verts and vert positions
        original_mesh = i.split('SF')[0] + i.split('SF_')[-1].split('Sculpt')[0] + '_PLY' 
        original_vert = cmds.ls(original_mesh + '.vtx[*]', flatten = True)
        original_pos = []
        for v in original_vert:
            pos = cmds.xform(v, query = True, translation = True, worldSpace = True)
            original_pos.append(pos)

        #--- go to the initial frame
        cmds.currentTime(current_frame)
        #--- set the vertex positions of the sculpt mesh
        sculpt_vert = cmds.ls(i + '.vtx[*]', flatten = True)
        for v, pos in zip(sculpt_vert, original_pos):
            cmds.xform(v, translation = pos, worldSpace = True)
#end def set_vertex_position()
set_vertex_position(getVtxPosOfFrame = 166)    






def bls():
    asset.loadLatestAsset(project = "7thDwarf_243111", 
                          department = "Blendshape", 
                          objectType = "Props", 
                          object = "IcebedRose", 
                          release= "Library", 
                          resolution= "hi", 
                          extension= ".ma", 
                          loadType = "import")
    cnBlendshape.blendshape(deleteShape = False)

    #--- single blendShapes
    cmds.connectAttr('C_bedMid_CTL.growA', 'C_iceBed_BSP.C_iceBed_growA_PLY')
    cmds.connectAttr('C_bedMid_CTL.growB', 'C_iceBed_BSP.C_iceBed_growB_PLY')
    cmds.connectAttr('C_bedMid_CTL.growC', 'C_iceBed_BSP.C_iceBed_growC_PLY')
    cmds.connectAttr('C_bedMid_CTL.noise', 'C_iceBed_BSP.C_iceBed_noise_PLY')
    cmds.connectAttr('C_bedMid_CTL.invert', 'C_iceBed_BSP.C_iceBed_invert_PLY')
    cmds.connectAttr('C_bedMid_CTL.waterA', 'C_iceBed_BSP.C_iceBed_waterA_PLY')
    cmds.connectAttr('C_bedMid_CTL.waterB', 'C_iceBed_BSP.C_iceBed_waterB_PLY')

    #--- multi blendShapes
    setup_multiple_blendshapes(control = 'C_bedMid_CTL', 
                               side = 'C', 
                               attr = 'rise', 
                               blendShapeNode = 'C_iceBed_BSP', 
                               blendShapes = ['C_iceBed_riseA_PLY',
                                              'C_iceBed_riseB_PLY',
                                              'C_iceBed_riseC_PLY'])
    setup_multiple_blendshapes(control = 'C_bedMid_CTL', 
                               side = 'C', 
                               attr = 'wobble', 
                               blendShapeNode = 'C_iceBed_BSP', 
                               blendShapes = ['C_iceBed_wobbleA_PLY',
                                              'C_iceBed_wobbleB_PLY',
                                              'C_iceBed_wobbleC_PLY',
                                              'C_iceBed_wobbleD_PLY'])
    #--- twist deformer
    setup_blendshape_deformer(control = 'C_bedMid_CTL', 
                              side = 'C',
                              blendShapeNode = 'C_iceBed_BSP',
                              blendShape = 'C_iceBed_twist_PLY',
                              deformerType = 'twist',
                              connectAttr = [['twistTop', 'endAngle'],
                                             ['twistBottom', 'startAngle']],
                              translation = [0,4.69359,0],
                              rotation = [0,0,0],
                              scale = [10.7415,3.54505,10.7415])
    #--- flare deformer
    setup_blendshape_deformer(control = 'C_bedMid_CTL', 
                              side = 'C',
                              blendShapeNode = 'C_iceBed_BSP',
                              blendShape = 'C_iceBed_flare_PLY',
                              deformerType = 'flare',
                              connectAttr = [['taperLength', 'endFlareX'],
                                             ['taperWidth', 'endFlareZ'],
                                             ['bulge', 'curve']],
                              translation = [0,4.03806,0],
                              rotation = [0,0,0],
                              scale = [10.7415,4.18685,10.7415])
    #--- lattice deformer
    cmds.setAttr('C_iceBed_BSP.C_iceBed_lattice_PLY', 1)
    setup_blendshape_lattice(side = 'C', 
                             blendShape = 'C_iceBed_lattice_PLY', 
                             divisions = [3,3,2], 
                             ldv = [2,2,2],
                             parent = 'C_bedMid_CTL')

    #--- set default values
    cmds.setAttr('C_bedMid_CTL.rise', 3)
    cmds.setAttr('C_bedMid_CTL.wobble', 4)
# def bls()

def add_blendShape_attributes(control = None):
    #--- this method adds blendShape attributes
    #--- blendShape separator
    cmds.addAttr(control, 
                 longName = "blendShapes", 
                 shortName = "blendShapes", 
                 attributeType = 'short',
                 min = 0,
                 max = 0)
    cmds.setAttr(control + '.blendShapes', 
                 edit = True, 
                 keyable = False, 
                 channelBox = True)
    #--- rise
    cmds.addAttr(control, 
                 longName = "rise", 
                 shortName = "rise", 
                 attributeType = 'float', 
                 min = 0, 
                 max = 3, 
                 defaultValue = 0, 
                 keyable = 1)
    #--- wobble
    cmds.addAttr(control, 
                 longName = "wobble", 
                 shortName = "wobble", 
                 attributeType = 'float', 
                 min = 0, 
                 max = 4, 
                 defaultValue = 0, 
                 keyable = 1)
    #--- growA
    cmds.addAttr(control, 
                 longName = "growA", 
                 shortName = "growA", 
                 attributeType = 'float', 
                 min = 0, 
                 max = 1, 
                 defaultValue = 0, 
                 keyable = 1)
    #--- growB
    cmds.addAttr(control, 
                 longName = "growB", 
                 shortName = "growB", 
                 attributeType = 'float', 
                 min = 0, 
                 max = 1, 
                 defaultValue = 0, 
                 keyable = 1)
    #--- growC
    cmds.addAttr(control, 
                 longName = "growC", 
                 shortName = "growC", 
                 attributeType = 'float', 
                 min = 0, 
                 max = 1, 
                 defaultValue = 0, 
                 keyable = 1)
    #--- noise
    cmds.addAttr(control, 
                 longName = "noise", 
                 shortName = "noise", 
                 attributeType = 'float', 
                 min = 0, 
                 max = 1, 
                 defaultValue = 0, 
                 keyable = 1)
    #--- invert
    cmds.addAttr(control, 
                 longName = "invert",
                 shortName = "invert",
                 attributeType = 'float',
                 min = 0, 
                 max = 1, 
                 defaultValue = 0, 
                 keyable = 1)
    #--- waterA
    cmds.addAttr(control, 
                 longName = "waterA",
                 shortName = "waterA",
                 attributeType = 'float', 
                 min = 0, 
                 max = 1, 
                 defaultValue = 0, 
                 keyable = 1)
    #--- waterB
    cmds.addAttr(control, 
                 longName = "waterB", 
                 shortName = "waterB", 
                 attributeType = 'float', 
                 min = 0, 
                 max = 1, 
                 defaultValue = 0, 
                 keyable = 1)

    #--- deformer separator
    cmds.addAttr(control, 
                 longName = "deformers", 
                 shortName = "deformers", 
                 attributeType = 'short',
                 min = 0,
                 max = 0)
    cmds.setAttr(control + '.deformers', 
                 edit = True, 
                 keyable = False, 
                 channelBox = True)
    #--- twistTop
    cmds.addAttr(control,
                 longName = "twistTop", 
                 shortName = "twistTop", 
                 attributeType = 'float', 
                 defaultValue = 0, 
                 keyable = 1)
    #--- twistBottom
    cmds.addAttr(control,
                 longName = "twistBottom", 
                 shortName = "twistBottom", 
                 attributeType = 'float',  
                 defaultValue = 0, 
                 keyable = 1)
    #--- taperLength
    cmds.addAttr(control, 
                 longName = "taperLength", 
                 shortName = "taperLength", 
                 attributeType = 'float', 
                 defaultValue = 1, 
                 keyable = 1)
    #--- taperWidth
    cmds.addAttr(control, 
                 longName = "taperWidth", 
                 shortName = "taperWidth", 
                 attributeType = 'float', 
                 defaultValue = 1, 
                 keyable = 1)
    #--- bulge
    cmds.addAttr(control, 
                 longName = "bulge", 
                 shortName = "bulge", 
                 attributeType = 'float', 
                 defaultValue = 0, 
                 keyable = 1)
    #--- lattice
    cmds.addAttr(control, 
                 longName = "latticeControls", 
                 shortName = "latticeControls", 
                 attributeType = 'short', 
                 min = 0,
                 max = 1,
                 defaultValue = 1, 
                 keyable = 1)
#end def add_blendShape_attributes()

def setup_multiple_blendshapes(control = None, 
                               side = None, 
                               attr = None, 
                               blendShapeNode = None, 
                               blendShapes = None):
    #--- this method setups multiple blendShapes
    nd = node.node()
    if not control:
        raise Exception('No control specified!')
    if not side:
        raise Exception('No side specified!')
    if not attr:
        raise Exception('No attribute specified!')
    if not blendShapeNode:
        raise Exception('No blendShapeNode specified!')
    if not blendShapes:
        raise Exception('No blendShapes specified!')

    #--- create utility nodes
    initial_rev = nd.create('reverse', side, 'initial' + blendShapes[0])
    initial_rmv = nd.create('remapValue', side, 'init' + blendShapes[0])

    #---create connections
    cmds.connectAttr(control + '.' + attr, initial_rev + '.inputX')
    cmds.connectAttr(initial_rev + '.outputX', initial_rmv + '.inputValue')
    cmds.connectAttr(initial_rmv + '.outValue', blendShapeNode + '.' + blendShapes[0])

    #--- iter through the blendShapes
    for shape in range(len(blendShapes[1:])):
        min = 0
        max = 1
        forward_rmv = nd.create('remapValue', side, 'forward' + blendShapes[1:][shape])
        backward_rmv = nd.create('remapValue', side, 'backward' + blendShapes[1:][shape])

        #---create connections
        cmds.connectAttr(control + '.' + attr, forward_rmv + '.inputValue')
        cmds.connectAttr(control + '.' + attr, backward_rmv + '.inputValue')
        cmds.connectAttr(forward_rmv + '.outValue', backward_rmv + '.outputMin')
        cmds.connectAttr(backward_rmv + '.outValue', blendShapeNode + '.' + blendShapes[1:][shape])
        cmds.setAttr(backward_rmv + '.outputMax', 0)
        cmds.setAttr(forward_rmv + '.inputMin', min + shape)
        cmds.setAttr(forward_rmv + '.inputMax', max + shape)
        cmds.setAttr(backward_rmv + '.inputMin', 1 + shape)
        cmds.setAttr(backward_rmv + '.inputMax', 2 + shape)
        min += 1
        max += 1
#end def setup_multiple_blendshapes()

def setup_blendshape_deformer(control = None, 
                              side = None,
                              blendShapeNode = None,
                              blendShape = None,
                              deformerType = None,
                              connectAttr = [None, None],
                              translation = [0,0,0],
                              rotation = [0,0,0],
                              scale = [1,1,1]):
    #--- this method setups the blendshape deformer
    if not control:
        raise Exception('No control specified!')
    if not side:
        raise Exception('No side specified!')
    if not blendShapeNode:
        raise Exception('No blendShapeNode specified!')
    if not blendShape:
        raise Exception('No blendShape specified!')
    if not deformerType:
        raise Exception('No deformerType specified!')
    if not connectAttr:
        raise Exception('No connectAttr specified!')

    cmds.setAttr(blendShapeNode + '.' + blendShape, 1)

    deformer = cmds.nonLinear(blendShape, type = deformerType, name = side + '_' + deformerType + '_DEF')
    cmds.xform(deformer[1], translation = translation, worldSpace = True)
    cmds.xform(deformer[1], rotation = rotation, worldSpace = True)
    cmds.xform(deformer[1], scale = scale, worldSpace = True)

    if isinstance(connectAttr, list):
        if isinstance(connectAttr[0], list):
            for cnt in connectAttr:
                cmds.connectAttr(control + '.' + cnt[0], deformer[0] + '.' + cnt[1])
    cmds.parent(deformer[1], 'Shapes')
    cmds.setAttr(deformer[1] + '.v', 0)
#end def setup_blendshape_deformer

def setup_blendshape_lattice(side = None, 
                             blendShape = None, 
                             divisions = [2,5,2], 
                             ldv = [2,2,2],
                             parent = None):
    #--- this method setups the lattice deformer
    lat = cmds.lattice(blendShape, 
                       divisions = divisions, 
                       objectCentered = True, 
                       ldv = ldv)
    cmds.setAttr(lat[1] + '.v', 0)
    cmds.parent(lat, 'Shapes')

    points = cmds.ls(lat[1] + '.pt[*]', flatten = True)
    for point in range(len(points)):
        pos = cmds.xform(points[point], query = True, translation = True, worldSpace = True)
        cPoint = node.nControl(position = pos, 
                               color = 17, 
                               size = 1, 
                               shape = 1, 
                               side = side, 
                               description = "latPoint" + str(point), 
                               parent = parent, 
                               rotateOrder = 2)
        cmds.setAttr(cPoint.control['transform'] + '.v', lock = False)
        cmds.connectAttr('C_bedMid_CTL.latticeControls', cPoint.control['transform'] + '.v')
        cls = cmds.cluster(points[point], name = side + '_latCluster' + str(point) + '_CLS')
        for axis in 'xyz':
            cmds.connectAttr(cPoint.control['transform'] + '.t' + axis, cls[1] + '.t' + axis)
        cmds.parent(cls[1], 'Shapes')
        cmds.setAttr(cls[1] + '.v', 0)
#end def setup_blendshape_lattice()



























from maya import cmds
from defCmds import defGuideCmds

"""
This is the faceRigTool_v003 from the great sausageScript family!
With the autoGuidePosition method you are able to position the guides 
by selecting the components and by writing the side and guidename:
Here is an example:

1. Select the verts to create the L_uplid  guides

2. Run this snippet: 

    from tmp import faceTools
    reload(faceTools)
    
    faceTools.autoGuidePosition(side = "L", guideName = "uplid", changeDirection = 0)

3. Check the guides and grab a beer. :)

Here is a list of the names which should be used:

guideName        side        info
    
uplid            L           
lowlid           L           here, the blink Guides will be created automatically 
eyeBrow          L
sepEyeBrow       L
midBrow          L
cheek            L

upLip            C           every guides except the side "C" ones will be mirrored automatically
lowLip           C
upperSticky      C
lowerSticky      C

If there are any questions or issues, please let me know. :)

Cheerio
the turkish engineer
if
"""

def autoGuidePosition(side = None, guideName = None, changeDirection = False):
#    check if the guides are loaded
    if cmds.objExists("C_faceRigGuides_TRN"):
        pass
    else:
        defGuideCmds.defGuideIO().loadGuides()
        
#    if changeDirection == True:
#        autoCheekGuidePosition(side = side, guideName = guideName)
#        return        
    
    if  (guideName == "cheek") or (guideName == "midbrow"):
        autoCheekGuidePosition(side = side, guideName = guideName, changeDirection = changeDirection)
        return
    
    elif (guideName == "eyeBrow") or (guideName == "sepEyeBrow"):
        autoEyebrowGuidePosition(side = side, guideName = guideName)
        return

    else:
#        store the selected verts
        objectName = side + "_" + guideName
        
#        store the selected verts           
        vtx = orderedSelection()
        
        if changeDirection == True:
            vtx.reverse()
        
#        store the verts' position
        pos = [] 
        for i in vtx:
            p = cmds.xform(i, query = 1, translation = 1, worldSpace = 1)
            pos.append(p)
        
#        check if vertices are selected and run code
        if vtx:
            if cmds.objExists(objectName + "_TRN"):
                cmds.delete(objectName + "_TRN")             
            
#            create the guides
            guides = defGuideCmds.defGuideCrv()
            length = len(vtx) - 1
            guides.__init__(nSpans = len(vtx)-1, curveDegree = 1, offset =.2, offsetVector = [1,0,0], side = side, name = guideName, startPosition = [0,0,0], ctlSize = 10)
            cmds.delete("C_curve_TRN") 
            
#            list all the guides inside the guideName group except the curve
            loc = cmds.listRelatives(objectName + "_TRN", allDescendents = 1, type = "transform")[:-1]
    
#            reposition the guides at the vertices place
            for i, p in zip(loc, pos):
                cmds.xform(i, translation = p, worldSpace = 1) 
            
#            check if guides have to be mirrored or not
            if side == "C":
                pass
            else:
                cmds.select(loc)
                guides.createMirror()
    
#            add the blink guides to the same spot as the lowlid guides
            if guideName == "lowlid":
                cmds.select(vtx)
                autoGuidePosition(side = side, guideName = "blink")
            
        else:
            cmds.warning("select edges dude!!!")


def autoCheekGuidePosition(side = None, guideName = None, changeDirection = False):
    objectName = side + "_" + guideName
    
    if guideName == "midbrow":
        vtx = cmds.ls(selection = 1, flatten = 1)

#    store the selected verts    
    if guideName != "midbrow":
        vtx = orderedSelection()
    
    if changeDirection == True:
        vtx.reverse()
    
#    store the verts' position
    pos = []
    for i in vtx:
        p = cmds.xform(i, query = 1, translation = 1, worldSpace = 1)
        pos.append(p)
    
#    check if vertices are selected and run code
    if vtx:
        if cmds.objExists(objectName + "_TRN"):
            cmds.delete(objectName + "_TRN")             
        
#        create the guides
        guides = defGuideCmds.defGuideCrv()
        length = len(vtx) - 1
        guides.__init__(nSpans = len(vtx)-1, curveDegree = 1, offset =.2, offsetVector = [1,0,0], side = side, name = guideName, startPosition = [0,0,0], ctlSize = 10)
        cmds.delete("C_curve_TRN") 
        
#        list all the guides inside the guideName group except the curve
        loc = cmds.listRelatives(objectName + "_TRN", allDescendents = 1, type = "transform")[:-1]

#        reposition the guides at the vertices place
        for i, p in zip(loc, pos):
            cmds.xform(i, translation = p, worldSpace = 1) 

#        check if guides have to be mirrored or not
        if side == "C":
            pass
        else:       
            cmds.select(loc)
            guides.createMirror()


def autoEyebrowGuidePosition(side = None, guideName = None):
    objectName = side + "_" + guideName
    sel = cmds.ls(os = 1, flatten = 1)
    
    pos = []
    cluster = []
    
#    check which type of component is selected and store the position
    for t in sel:
        i = t
        selType = t.split(".")[1][0]

        if selType == "e":
            vtx = cmds.polyListComponentConversion(i, fe = 1, tv = 1)
            cmds.select(vtx)
            cls = cmds.cluster()
            
            clsPos = cmds.xform(cls, query = 1, rotatePivot = 1, worldSpace = 1)
            pos.append(clsPos)
            cluster.append(cls)

        elif selType == "f":
            vtx = cmds.polyListComponentConversion(i, ff = 1, tv = 1)
            cmds.select(vtx)
            cls = cmds.cluster()
            
            clsPos = cmds.xform(cls, query = 1, rotatePivot = 1, worldSpace = 1)
            pos.append(clsPos)
            cluster.append(cls)

        elif selType == "v":
            cmds.warning("Select in another component mode! We are out of verts dude!!!")
            
        else:
            cmds.warning("No components selected dude!!!")
    
#    check if guide group exists     
    if cluster:
        if cmds.objExists(objectName + "_TRN"):
            cmds.delete(objectName + "_TRN")   
    
#        create the guides
        guides = defGuideCmds.defGuideCrv()
        guides.__init__(nSpans = len(cluster)-1, curveDegree = 1, offset =.2, offsetVector = [1,0,0], side = side, name = guideName, startPosition = [0,0,0], ctlSize = 10)
        cmds.delete("C_curve_TRN")
        
#        delete the cluster     
        for c in cluster:
            cmds.delete(c)
    
#        list all the guides inside the guideName group except the curve
        loc = cmds.listRelatives(objectName + "_TRN", allDescendents = 1, type = "transform")[:-1]
    
#        reposition the guides at the vertices place
        for i, p in zip(loc, pos):
            cmds.xform(i, translation = p, worldSpace = 1) 
        
#        mirror the guides
        cmds.select(loc)
        guides.createMirror()                


def orderedSelection():
    selection = cmds.ls(sl = 1)
    result = []
    if selection != None:
        sel = cmds.polyListComponentConversion(toEdge = True, internal = True)
        edges = cmds.ls(sel, flatten = True)
        
        edgeVerts = []
        for edge in edges:
            edgeVtx = cmds.ls(cmds.polyListComponentConversion(edge, fromEdge = True, toVertex = True), flatten = True)
            vtx = [int(edgeVtx[0].split("[")[1].split("]")[0]), int(edgeVtx[1].split("[")[1].split("]")[0])]
            edgeVerts.append(vtx)
        
        vertList = edgeVerts[0]
        edgeVerts.remove(edgeVerts[0])                
        
        for i in range(len(sel)*2):
            for edVert in edgeVerts:
                if edVert[0] in vertList:
                    if vertList.index(edVert[0]) == 0:
                        vertList.insert(0, edVert[1])
                    else:
                        vertList.append(edVert[1])
                    edgeVerts.remove(edVert)
                    break
                
                if edVert[1] in vertList:
                    if vertList.index(edVert[1]) == 0:
                        vertList.insert(0, edVert[0])
                    else:
                        vertList.append(edVert[0])
                    edgeVerts.remove(edVert)
                    break
                
        for vert in vertList:
            vtx = edgeVtx[0].split("[")[0]
            result.append(vtx + "[" + str(vert) + "]")
    else:
        cmds.warning("select edges dude!!!")
    return result

#autoGuidePosition(side = "C", guideName = "lowLip", changeDirection = 0)




























from maya import cmds
 
def createFollicle (pos=[0, 0, 0], nurbs_surface=None, poly_surface=None):
 
    if (nurbs_surface==None and poly_surface==None):
        cmds.error("Function createFollicle() needs a nurbs surface or poly surface")
        return
 
    transform_node = cmds.createNode("transform")
    cmds.setAttr((transform_node +".tx"), pos[0])
    cmds.setAttr((transform_node +".ty"), pos[1])
    cmds.setAttr((transform_node +".tz"), pos[2])
 
    #make vector product nodes to get correct rotation of the transform node
    vector_product = cmds.createNode("vectorProduct")
    cmds.setAttr((vector_product+".operation"), 4)
    cmds.connectAttr( (transform_node+".worldMatrix"), (vector_product+".matrix"), f=1)
    cmds.connectAttr( (transform_node+".rotatePivot"), (vector_product+".input1"), f=1)
 
    #connect the correct position to a closest point on surface node created
    if nurbs_surface:
        closest_position = cmds.createNode("closestPointOnSurface", n=(transform_node+"_CPOS"))
        cmds.connectAttr( (nurbs_surface+".ws"), (closest_position+".is"), f=1)
        cmds.connectAttr( (vector_product+".output"), (closest_position+".inPosition"), f=1)
 
    if poly_surface:
        closest_position = cmds.createNode("closestPointOnMesh", n=(transform_node+"_CPOS"))
        cmds.connectAttr( (poly_surface+".outMesh"), (closest_position+".im"), f=1)
        cmds.connectAttr( (vector_product+".output"), (closest_position+".inPosition"), f=1)
 
    #create a follicle node and connect it
    follicle_transform = cmds.createNode("transform", n=(transform_node+"follicle"))
    follicle = cmds.createNode("follicle", n=(transform_node+"follicleShape"), p=follicle_transform)
    cmds.connectAttr((follicle+".outTranslate"), (follicle_transform+".translate"), f=1)
    cmds.connectAttr((follicle+".outRotate"), (follicle_transform+".rotate"), f=1)
    if nurbs_surface:
        cmds.connectAttr((nurbs_surface+".local"), (follicle+".is"), f=1)
        cmds.connectAttr((nurbs_surface+".worldMatrix[0]"), (follicle+".inputWorldMatrix"), f=1)
    if poly_surface:
        cmds.connectAttr((poly_surface+".outMesh"), (follicle+".inm"), f=1)
        cmds.connectAttr((poly_surface+".worldMatrix[0]"), (follicle+".inputWorldMatrix"), f=1)
 
    cmds.setAttr((follicle+".parameterU"), cmds.getAttr (closest_position+".parameterU"))
    cmds.setAttr((follicle+".parameterV"), cmds.getAttr (closest_position+".parameterV"))
 
    #return strings
    cmds.delete(transform_node)
    return [follicle_transform, follicle, closest_position]
 
def createFollicles (follicle_positions=[[0,0,0]], nurbs_surface=None, poly_surface=None):
 
    out_follicles=list()
 
    if (nurbs_surface==None and poly_surface==None):
        cmds.error("Function createFollicles() needs a nurbs surface or poly surface")
        return
 
    for pos in follicle_positions:
        lst = createFollicle(pos, nurbs_surface, poly_surface)
        out_follicles.append(lst)
    return out_follicles



























class AlembicAsset(object):
    '''This class setups the imported alembic assets'''
    def __init__(self, project=None, release=None, objectType=None, 
                 object=None, department=None, proxy=True, version=None):
        #args
        self.project = project
        self.release = release
        self.objectType = objectType
        self.object = object
        self.department = department
        self.proxy = proxy
        self.version = version

        #vars
        self.versions = None
        self.cache_link = None
        self.cache_info = None
        self.geo = None

        #methods
        self.__create()
    #END def __init__()

    def __load_alembic_asset(self):
        '''
        This method loads the actual alembic asset if version is set to None, 
        else this method loads the desired abc asset version if it exists
        '''
        self.release = 'library'
        self.department = 'model'
        self.versions = 'versions'

        if self.proxy:
            self.cache_link = 'cache_low.abc'
            self.cache_info = 'cache_low.abc.info'
        else:
            self.cache_link = 'cache.abc'
            self.cache_info = 'cache.abc.info'

        obj_type_token = ''
        if self.objectType == "Face":
            obj_type_token = "_fac"
        elif self.objectType == "Body":
            obj_type_token = "_bod"

        #--- check composite path
        try:
            composite_path = path.join(basePath, 
                                       self.project, 
                                       self.release, 
                                       self.objectType, 
                                       self.object, 
                                       self.department)+"/"
            if not path.isdir(composite_path):
                raise RuntimeError('Cannot find the path, with given informations,' 
                                   ' please check the names. No Directory!')
        except:
            composite_path = path.join(corkyPath, 
                                       self.project, 
                                       self.release, 
                                       self.objectType, 
                                       self.object, 
                                       self.department)+"/"
            print composite_path
            if not path.isdir(composite_path):
                raise RuntimeError('Cannot find the path, with given informations,' 
                                   ' please check the names. No Directory!')

        if not self.version:
            #--- get the actual alembic version from the symlink and import it
            sym_link = composite_path + self.cache_link
            abc_info = composite_path + self.cache_info
            abc = cmds.AbcImport(sym_link, mode = 'import')
            self.__prepare_alembic_asset(abc_info, sym_link)
        else:
            #--- check if version flag is a number
            if not self.version.isdigit():
                raise Exception('Version flag has to be a number, for example: 001')
            #--- get all the files in the versions folder
            get_all_files = self.__find_alembics(composite_path + self.versions)
            v = 'v' + self.version
            for file in get_all_files:
                if v in file:
                    version_abc = composite_path + self.versions + '/' + file
                    version_abc_info = version_abc + '.info'
                    abc = cmds.AbcImport(version_abc, mode = 'import')
                    self.__prepare_alembic_asset(version_abc_info, version_abc)
    #END def __load_alembic_asset()

    def __find_alembics(self, absoluteDirectory):
        '''
        search the absolute directory for all files with the given extension
        return a list of all file names, excluding the file extension
        '''
        all_files = listdir(absoluteDirectory)

        #--- refine all files, listing only of specified file extension
        return_files = list()
        for f in all_files:
            if not '.info' in f:
                if not '.log' in f:
                    return_files.append(f)
        return return_files
    #END def __find_alembics()

    def __prepare_alembic_asset(self, abcInfoPath = None, abcFile = None):
        #--- this method prepares the abc assets properly, abc.info path required
        abc_class = None
        if abcInfoPath:
            file = open(abcInfoPath, 'r')
            abc_class = yaml.load(file)
        else:
            raise Exception('No valid abc.info path given: ' + abcInfoPath)
        #--- create root group and add the proper information
        root = cmds.createNode('transform', name = abc_class.get_name())
        if self.proxy:
            geo = 'C_geo_proxyExport_GRP'
        else:
            geo = 'C_geoExport_GRP'
        if cmds.objExists(geo):
            cmds.parent(geo, root)
        self.geo = geo

        #--- setup the alembics
        self.__alembic_setup(abcFile)

        #--- create root attributes
        if not cmds.objExists(root + '.assetId'):
            cmds.addAttr(root, longName='assetId', 
                         shortName='assetId', 
                         dataType='string')
        if not cmds.objExists(root + '.assetType'):
            cmds.addAttr(root, longName='assetType', 
                         shortName='assetType', 
                         dataType='string')
        if not cmds.objExists(root + '.type'):
            cmds.addAttr(root, longName='type', 
                         shortName='type', 
                         attributeType='enum',
                         enumName='static:dynamic:assembly')
        if not cmds.objExists(root + '.pref'):
            cmds.addAttr(root, longName='pref', 
                         shortName='pref', 
                         attributeType='bool')

        #--- set root attributes
        cmds.setAttr(root + '.assetId', abc_class.get_name(), 
                     type='string', lock=True)
        cmds.setAttr(root + '.assetType', abc_class.get_assettype(), 
                     type='string', lock=True)
        enum = 0
        for i in range(len(abc_class.get_types())):
            if abc_class.get_types()[i] == abc_class.get_type():
                enum = i
        cmds.setAttr(root + '.type', enum, lock=True)
        try:
            cmds.setAttr(root + '.pref', abc_class.get_pref(), lock = True)
        except:
            cmds.setAttr(root + '.pref', lock = True)
    #END def __prepare_alembic_asset()

    def __alembic_setup(self, abcFile = None):
        #--- this method setups the alembic node
        if not cmds.objExists(self.geo + '.abcFile'):
            cmds.addAttr(self.geo, 
                         longName = 'abcFile', 
                         shortName ='abcFile',
                         dataType = 'string')
            cmds.setAttr(self.geo + '.abcFile', abcFile, 
                         type = 'string', lock = True)
    #END def __alembic_setup()

    def __resetup_proxy_hires(self):
        #--- this method setups the proxy and hires geo groups
        if cmds.objExists(self.object):
            geo = cmds.ls(self.object + '*')
            for grp in geo:
                if not grp == self.object:
                    child = cmds.listRelatives(grp,children=True)[0]
                    cmds.parent(child, self.object)
                    cmds.delete(grp)
    #END def __resetup_proxy_hires()

    def __create(self):
        #--- this method is the main create method
        self.__load_alembic_asset()
        self.__resetup_proxy_hires()
    #END def __create()
#END class AlembicAsset()
    
