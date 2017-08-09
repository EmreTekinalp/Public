'''
Created on 25.11.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: This is the shotFinaling Tool
'''
import time
from maya import cmds

class ShotFinalCore(object):
    '''
    This is the ShotFinal Tool 2.0 Core Class which will be inherited for the
    other operations to create the proper ShotFinal setup
    '''
    def __init__(self):
        ########################################################################
        #vars
        self.character       = None
        self.mesh            = None
        self.mesh_abc        = None
        self.mesh_bsp        = None
        self.current_frame   = None
        self.time_stamp      = None
        self.shotfinaling    = None
        self.sf_originals    = None
        self.sf_abc_grp      = None
        self.sf_blendshapes  = None
        self.sf_bsp_grp      = None
        self.sf_sculpts      = None
        self.sf_negatives    = None
        self.sf_results      = None
        self.sf_controls     = None
        self.sf_char_ctl_grp = None
        self.sf_mesh_ctl_grp = None

        #methods
        self.__create()
    #end def __init__()

    def __check_scene(self):
        #--- this method checks the scene for alembic meshes and proper renaming
        sel = cmds.ls(selection = True)
        if sel:
            #--- store the selected mesh
            self.mesh = sel[0]
            #--- check if selection is a valid mesh
            for shape in cmds.listRelatives(self.mesh,
                                            children = True,
                                            fullPath = True):
                mesh = cmds.nodeType(shape)
                if not mesh == 'mesh':
                    raise Exception('Selection is not a valid polyMesh!')
                break
            #--- get the character name
            if self.__root_of(node = self.mesh):
                #--- use the highest parent node as the character name
                self.character = self.__root_of(node = self.mesh)
            else:
                self.character = 'CHAR'
        else:
            raise Exception('Select a polyMesh object!')
    #end def __check_scene()

    def __root_of(self,
                   node = None):
        #--- this method gets the highest top parent node of the selection
        result = []
        #--- get first parent
        var = cmds.listRelatives(node, parent = True, fullPath = True)
        if var:
            #--- loop all parents
            while(len(var) > 0):
                result = var
                var = cmds.listRelatives(var, parent = True, fullPath = True)
                if not var:
                    break
        if result:
            if '|' in result[0]:
                result = result[0].split('|')[-1]
            if isinstance(result, list):
                result = result[0]
        return result
    #end def __root_of()

    def __get_time_frame(self):
        #--- this method gets the timeStamp and Frame information
        #--- get current frame
        self.current_frame = cmds.currentTime(query = True)
        #--- get timeStamp
        ts = str(time.time())
        self.time_stamp = str(ts.split('.')[0] + ts.split('.')[1])
    #end def __get_time_frame()

    def __setup_groups(self):
        #--- this method setups the shotFinaling groups properly
        cmds.select(clear = True)
        #--- SHOTFINALING
        if cmds.objExists('SHOTFINALING'):
            self.shotfinaling = 'SHOTFINALING'
        else:
            self.shotfinaling = cmds.createNode('transform',
                                                name = 'SHOTFINALING')
        #--- SF_ORIGINALS
        if cmds.objExists('SF_ORIGINALS'):
            self.sf_originals = 'SF_ORIGINALS'
        else:
            self.sf_originals = cmds.createNode('transform',
                                                name = 'SF_ORIGINALS',
                                                parent = self.shotfinaling)
        #--- SF_BLENDSHAPES
        if cmds.objExists('SF_BLENDSHAPES'):
            self.sf_blendshapes = 'SF_BLENDSHAPES'
        else:
            self.sf_blendshapes = cmds.createNode('transform',
                                                  name = 'SF_BLENDSHAPES',
                                                  parent = self.shotfinaling)
        #--- SF_CONTROLS
        if cmds.objExists('SF_CONTROLS'):
            self.sf_controls = 'SF_CONTROLS'
        else:
            self.sf_controls = cmds.createNode('transform',
                                               name = 'SF_CONTROLS',
                                               parent = self.shotfinaling)
        #--- SF_CHARACTER_ABC_GRP
        if cmds.objExists('SF_' + self.character + '_ABC_GRP'):
            self.sf_abc_grp = 'SF_' + self.character + '_ABC_GRP'
        else:
            self.sf_abc_grp = cmds.createNode('transform',
                                               name = ('SF_' + self.character +
                                                       '_ABC_GRP'),
                                               parent = self.sf_originals)
        #--- SF_CHARACTER_BSP_GRP
        if cmds.objExists('SF_' + self.character + '_BSP_GRP'):
            self.sf_bsp_grp = 'SF_' + self.character + '_BSP_GRP'
        else:
            self.sf_bsp_grp = cmds.createNode('transform',
                                               name = ('SF_' + self.character +
                                                       '_BSP_GRP'),
                                               parent = self.sf_blendshapes)
        #--- SF_CHARACTER_CTL_GRP
        if cmds.objExists('SF_' + self.character + '_CTL_GRP'):
            self.sf_char_ctl_grp = 'SF_' + self.character + '_CTL_GRP'
        else:
            self.sf_char_ctl_grp = cmds.createNode('transform',
                                               name = ('SF_' + self.character +
                                                       '_CTL_GRP'),
                                               parent = self.sf_controls)
        #--- SF_CHARACTER_MESH_CTL_GRP
        if '|' in self.mesh:
            if cmds.objExists('SF_' + self.character + '_' +
                              self.mesh.split('|')[-1] + '_CTL_GRP'):
                self.sf_mesh_ctl_grp = ('SF_' + self.character + '_'
                                        + self.mesh.split('|')[-1]
                                        + '_CTL_GRP')
            else:
                self.sf_mesh_ctl_grp = cmds.createNode('transform',
                                                       name = ('SF_' + self.character +
                                                               '_' + self.mesh.split('|')[-1] +
                                                               '_CTL_GRP'),
                                                       parent = self.sf_char_ctl_grp)
        else:
            if cmds.objExists('SF_' + self.character + '_' + self.mesh + '_CTL_GRP'):
                self.sf_mesh_ctl_grp = ('SF_' + self.character + '_'
                                        + self.mesh + '_CTL_GRP')
            else:
                self.sf_mesh_ctl_grp = cmds.createNode('transform',
                                                       name = ('SF_' + self.character +
                                                               '_' + self.mesh +
                                                               '_CTL_GRP'),
                                                       parent = self.sf_char_ctl_grp)
        #--- SF_CHARACTER_SCULPTS
        if cmds.objExists('SF_' + self.character + '_SCULPTS'):
            self.sf_sculpts = 'SF_' + self.character + '_SCULPTS'
        else:
            self.sf_sculpts = cmds.createNode('transform',
                                             name = ('SF_' + self.character +
                                                     '_SCULPTS'),
                                             parent = self.sf_bsp_grp)
        #--- SF_CHARACTER_NEGATIVES
        if cmds.objExists('SF_' + self.character + '_NEGATIVES'):
            self.sf_negatives = 'SF_' + self.character + '_NEGATIVES'
        else:
            self.sf_negatives = cmds.createNode('transform',
                                                name = ('SF_' + self.character +
                                                        '_NEGATIVES'),
                                                parent = self.sf_bsp_grp)
        #--- SF_CHARACTER_RESULTS
        if cmds.objExists('SF_' + self.character + '_RESULTS'):
            self.sf_results = 'SF_' + self.character + '_RESULTS'
        else:
            self.sf_results = cmds.createNode('transform',
                                              name = ('SF_' + self.character +
                                                      '_RESULTS'),
                                              parent = self.sf_bsp_grp)
    #end def __setup_groups()

    def __setup_meshes(self):
        #--- this method creates the original and final meshes setup
        if '|' in self.mesh:
            if not cmds.objExists(self.character + '_' +
                                  self.mesh.split('|')[-1] + '_ABC'):
                #--- create a duplicate of the selection
                dup = cmds.duplicate(self.mesh, renameChildren = True)
                #--- rename the original mesh
                if '|' in self.mesh:
                    self.mesh_abc = cmds.rename(self.mesh, self.character + '_' +  
                                                self.mesh.split('|')[-1] + '_ABC')
                else:                
                    self.mesh_abc = cmds.rename(self.mesh, self.character
                                                + '_' + self.mesh + '_ABC')
                #--- parent this renamed original mesh into the proper sf_abc_grp
                cmds.parent(self.mesh_abc, self.sf_abc_grp)
                #--- rename the duplicated one like the original one
                if '|' in self.mesh:
                    self.mesh = cmds.rename(dup, self.mesh.split('|')[-1])
                    #--- create a message connection between old and new mesh
                    self.__message_connection(target = self.mesh_abc,
                                              source = self.mesh)
                else:
                    self.mesh = cmds.rename(dup, self.mesh)
                    #--- create a message connection between old and new mesh
                    self.__message_connection(target = self.mesh_abc, 
                                              source = self.mesh)
                #--- create the main blendShape setup
                if '|' in self.mesh:
                    self.mesh_bsp = cmds.blendShape(self.mesh_abc,
                                                    self.mesh,
                                                    name = (self.character + '_' +
                                                            self.mesh.split('|')[-1]
                                                            + '_BSP'),
                                                    weight = (0,1))[0]
                else:
                    self.mesh_bsp = cmds.blendShape(self.mesh_abc,
                                                    self.mesh,
                                                    name = (self.character + '_' +
                                                            self.mesh + '_BSP'),
                                                    weight = (0,1))[0]
            else:
                if '|' in self.mesh:                
                    mesh = self.mesh.split('|')[-1]
                    self.mesh_abc = mesh + '_ABC'
                    #--- check if the mesh blendShape node also exists
                    if not cmds.objExists(self.character + '_' + mesh + '_BSP'):
                        self.mesh_bsp = cmds.blendShape(self.mesh_abc,
                                                        mesh,
                                                        name = (self.character + '_' +
                                                                mesh + '_BSP'),
                                                        weight = (0,1))[0]
                    else:
                        self.mesh_bsp = self.character + '_' + mesh + '_BSP'
                else:
                    #--- check if the mesh blendShape node also exists
                    if not cmds.objExists(self.character + '_' + self.mesh + '_BSP'):
                        self.mesh_bsp = cmds.blendShape(self.mesh_abc,
                                                        self.mesh,
                                                        name = (self.character + '_' +
                                                                self.mesh + '_BSP'),
                                                        weight = (0,1))[0]
                    else:
                        self.mesh_bsp = self.character + '_' + self.mesh + '_BSP'                    
        else:
            if ':' in self.mesh:
                if not cmds.objExists(self.mesh.split(':')[0] + ':' + 
                                      self.mesh.split(':')[-1] + '_ABC'):       
                    #--- create a duplicate of the selection
                    dup = cmds.duplicate(self.mesh, renameChildren = True)
                    #--- rename the original mesh
                    self.mesh_abc = cmds.rename(self.mesh, self.mesh.split(':')[0] 
                                                + ':' + self.mesh.split(':')[-1] 
                                                + '_ABC')
                    #--- parent this renamed original mesh into the proper sf_abc_grp
                    cmds.parent(self.mesh_abc, self.sf_abc_grp)
                    #--- rename the duplicated one like the original one
                    self.mesh = cmds.rename(dup, self.mesh)
                    #--- create a message connection between old and new mesh
                    self.__message_connection(target = self.mesh_abc, source = self.mesh)
                    #--- create the main blendShape setup
                    self.mesh_bsp = cmds.blendShape(self.mesh_abc,
                                                    self.mesh,
                                                    name = (self.mesh.split(':')[0] + ':' + 
                                                            self.mesh.split(':')[-1] + '_BSP'),
                                                    weight = (0,1))[0]
                else:
                    self.mesh_abc = self.mesh + '_ABC'
                    #--- check if the mesh blendShape node also exists
                    if not cmds.objExists(self.mesh.split(':')[0] + ':' + 
                                          self.mesh.split(':')[-1] + '_BSP'):
                        self.mesh_bsp = cmds.blendShape(self.mesh_abc,
                                                        self.mesh,
                                                        name = (self.mesh.split(':')[0] + ':' + 
                                                                self.mesh.split(':')[-1] + '_BSP'),
                                                        weight = (0,1))[0]
                    else:
                        self.mesh_bsp = (self.mesh.split(':')[0] + ':' + 
                                         self.mesh.split(':')[-1] + '_BSP')
            else:
                if not cmds.objExists(self.character + '_' + self.mesh + '_ABC'):       
                    #--- create a duplicate of the selection
                    dup = cmds.duplicate(self.mesh, renameChildren = True)
                    #--- rename the original mesh
                    self.mesh_abc = cmds.rename(self.mesh, self.character
                                                + '_' + self.mesh + '_ABC')
                    #--- parent this renamed original mesh into the proper sf_abc_grp
                    cmds.parent(self.mesh_abc, self.sf_abc_grp)
                    #--- rename the duplicated one like the original one
                    self.mesh = cmds.rename(dup, self.mesh)
                    #--- create a message connection between old and new mesh
                    self.__message_connection(target = self.mesh_abc, source = self.mesh)
                    #--- create the main blendShape setup
                    self.mesh_bsp = cmds.blendShape(self.mesh_abc,
                                                    self.mesh,
                                                    name = (self.character + '_' +
                                                            self.mesh + '_BSP'),
                                                    weight = (0,1))[0]
                else:
                    self.mesh_abc = self.mesh + '_ABC'
                    #--- check if the mesh blendShape node also exists
                    if not cmds.objExists(self.character + '_' + self.mesh + '_BSP'):
                        self.mesh_bsp = cmds.blendShape(self.mesh_abc,
                                                        self.mesh,
                                                        name = (self.character + '_' +
                                                                self.mesh + '_BSP'),
                                                        weight = (0,1))[0]
                    else:
                        self.mesh_bsp = self.character + '_' + self.mesh + '_BSP'
        cmds.select(self.mesh)
    #end def __setup_meshes()

    def __message_connection(self,
                               target = None,
                               source = None):
        #--- this method creates a message between the target and source mesh
        #--- create a message attribute on source
        if target:
            if not isinstance(target, list):
                if source:
                    if not isinstance(source, list):
                        cmds.addAttr(source,
                                     longName = 'original',
                                     attributeType = 'message')
                        #--- connect the target message with source original attr
                        if '|' in target:
                            target = target.split('|')[-1]
                        cmds.connectAttr(target + '.message', source + '.original')
                    else:
                        raise Exception('You have to specify a string as a source!')
                else:
                    raise Exception('You have to specify a source object!')
            else:
                raise Exception('You have to specify a string as a target!')
        else:
            raise Exception('You have to specify a target object!')
    #end def __message_connection()

    def __cleanup(self):
        #--- this method cleans up the nodes
        #--- hide SF groups
        to_hide = [self.sf_originals, self.sf_negatives, self.sf_results,]
        for obj in to_hide:
            if not cmds.getAttr(obj + '.v', lock = True):
                if cmds.getAttr(obj + '.v', keyable = True):
                    cmds.setAttr(obj + '.v', 0)
        #--- lock SF groups
        to_lock = [self.shotfinaling, self.sf_originals,
                   self.sf_abc_grp, self.sf_blendshapes,
                   self.sf_bsp_grp, self.sf_sculpts,
                   self.sf_negatives, self.sf_results,
                   self.sf_controls, self.sf_char_ctl_grp,
                   self.sf_mesh_ctl_grp]
        for obj in to_lock:
            for attr in 'trs':
                for axis in 'xyz':
                    if not cmds.getAttr(obj + '.' + attr + axis, lock = True):
                        if cmds.getAttr(obj + '.' + attr + axis, keyable = True):
                            cmds.setAttr(obj + '.' + attr + axis,
                                         lock = True, keyable = False)
                            cmds.setAttr(obj + '.' + attr + axis,
                                         lock = True, keyable = False)
                            cmds.setAttr(obj + '.' + attr + axis,
                                         lock = True, keyable = False)
            if not cmds.getAttr(obj + '.v', lock = True):
                if cmds.getAttr(obj + '.v', keyable = True):
                    cmds.setAttr(obj + '.v', lock = True, keyable = False)
    #end def __setup_info()

    def __create(self):
        #--- this is the main create method
        #--- check the scene
        self.__check_scene()
        #--- get time and frame
        self.__get_time_frame()
        #--- setup the groups
        self.__setup_groups()
        #--- setup the meshes
        self.__setup_meshes()
        #--- cleanup the mess
        self.__cleanup()
    #end def __create()
#end class ShotFinalCore()


class ShotFinalMain(ShotFinalCore):
    '''
    This is the main shotFinal class, which creates the tool
    '''
    def __init__(self,
                 tripleKey = False,
                 tripleKeyOffset = 1):
        #--- inherit the ShotFinalCore class
        super(ShotFinalMain, self).__init__()

        #args
        self.character       = self.character
        self.tripleKey       = tripleKey
        self.tripleKeyOffset = tripleKeyOffset

        #vars
        self.mesh_sculpt   = None
        self.mesh_negative = None
        self.mesh_result   = None
        self.sculpt_bsp    = None
        self.target_index  = None

        #methods
        self.__create()
    #end def __init__()

    def __create_blendshape_meshes(self):
        #--- this method creates the blendShape meshes
        #--- duplicate the selected mesh, rename and store as sculpt
        dup_sculpt = cmds.duplicate(self.mesh, renameChildren = True)
        cmds.parent(dup_sculpt, self.sf_sculpts)
        #--- duplicate the selected mesh, rename and store as negative
        dup_negative = cmds.duplicate(self.mesh, renameChildren = True)
        cmds.parent(dup_negative, self.sf_negatives)
        #--- set the envelope of the mesh blendShape to 0 and duplicate as result
        cmds.setAttr(self.mesh_bsp + '.envelope', 0)
        dup_result = cmds.duplicate(self.mesh, renameChildren = True)
        cmds.parent(dup_result, self.sf_results)
        #--- rename the meshes
        if '|' in self.mesh:
            self.mesh_sculpt = cmds.rename(dup_sculpt, self.mesh.split('|')[-1] +
                                           '_SCULPT' + self.time_stamp)
            self.mesh_negative = cmds.rename(dup_negative, self.mesh.split('|')[-1] +
                                             '_NEGATIVE' + self.time_stamp)
            self.mesh_result = cmds.rename(dup_result, self.mesh.split('|')[-1] +
                                           '_RESULT' + self.time_stamp)
        else:
            if ':' in self.mesh:
                self.mesh_sculpt = cmds.rename(dup_sculpt, self.mesh.split(':')[-1] +
                                               '_SCULPT' + self.time_stamp)
                self.mesh_negative = cmds.rename(dup_negative, self.mesh.split(':')[-1] +
                                                 '_NEGATIVE' + self.time_stamp)
                self.mesh_result = cmds.rename(dup_result, self.mesh.split(':')[-1] +
                                               '_RESULT' + self.time_stamp)
            else:
                self.mesh_sculpt = cmds.rename(dup_sculpt, self.mesh +
                                               '_SCULPT' + self.time_stamp)
                self.mesh_negative = cmds.rename(dup_negative, self.mesh +
                                                 '_NEGATIVE' + self.time_stamp)
                self.mesh_result = cmds.rename(dup_result, self.mesh +
                                               '_RESULT' + self.time_stamp)
        cmds.setAttr(self.mesh_bsp + '.envelope', 1)
    #end def __create_blendshape_meshes()

    def __setup_blendshape_meshes(self):
        #--- this method setups the blendShape meshes
        #--- create a blendShape between the sculpt, negative and the result
        self.sculpt_bsp = cmds.blendShape(self.mesh_sculpt,
                                          self.mesh_negative,
                                          self.mesh_result,
                                          weight = [(0,1),(1,-1)])[0]
        #--- get the target index
        self.__get_blendshape_target_index()
        #--- add the result mesh to the mesh blendShape
        cmds.blendShape(self.mesh_bsp,
                        edit = True,
                        target = (self.mesh, self.target_index, self.mesh_result, 1.0),
                        weight = (self.target_index, 1))
        #--- connect the message attribute of the mesh bsp to the result mesh
        cmds.connectAttr(self.mesh_bsp + '.message', 
                         self.mesh_result + '.original', force = True)
    #end def __setup_sculpt()

    def __get_blendshape_target_index(self):
        #--- this method gets a free target_index for the blendShape
        if self.mesh_bsp:
            if cmds.objExists(self.mesh_bsp):
                world_mesh = cmds.listConnections(self.mesh_bsp + '.inputTarget',
                                                  plugs = True)
                cnt = cmds.listConnections(world_mesh,
                                           plugs = True,
                                           destination = True)[-1].split('.')[2].split('[')[1].split(']')[0]
                plug = int(cnt) + 1
                plug_list = []
                for i in world_mesh:
                    cnt_list = cmds.listConnections(i, plugs = True,
                                                    destination = True)
                    for cnt in cnt_list:
                        if 'inputTargetItem[6000].inputGeomTarget' in cnt:
                            plug_list.append(int(cnt.split('.')[2].split('[')[1].split(']')[0]))
                for plug in range(len(plug_list) + 1):
                    if plug not in plug_list:
                        #--- check free plugs
                        self.target_index = plug
                        break
                self.target_index = plug
        else:
            raise Exception('The final mesh blendShape is missing!')
    #end def __get_blendshape_target_index()

    def __create_sculpt_control(self):
        #--- this method creates the sculpt control
        if '|' in self.mesh:
            self.sf_mesh_ctl = cmds.createNode('transform',
                                               name = ('SF_' +
                                                       self.character + '_' +
                                                       self.mesh.split('|')[-1] +
                                                       str(self.target_index)
                                                       + '_CTL'),
                                               parent = self.sf_mesh_ctl_grp)
        else:
            self.sf_mesh_ctl = cmds.createNode('transform',
                                               name = ('SF_' +
                                                       self.character + '_' +
                                                       self.mesh +
                                                       str(self.target_index)
                                                       + '_CTL'),
                                               parent = self.sf_mesh_ctl_grp)
    #end def __create_sculpt_control()

    def __add_sculpt_control_attributes(self):
        #--- this method adds attributes to the sculpt group and control
        if '|' in self.mesh:
            mesh = self.mesh.split('|')[-1]
            #--- sculpt_group.mesh
            if not cmds.objExists(self.sf_mesh_ctl_grp + '.' + mesh):
                cmds.addAttr(self.sf_mesh_ctl_grp,
                             longName = mesh,
                             shortName = mesh,
                             attributeType = 'short',
                             min = 0,
                             max = 1,
                             defaultValue = 1,
                             keyable = True)
                cmds.setAttr(self.sf_mesh_ctl_grp + '.' + mesh,
                             edit = True,
                             channelBox = True)
        else:
            #--- sculpt_group.mesh
            if ':' in self.mesh:            
                if not cmds.objExists(self.sf_mesh_ctl_grp + '.' + 
                                      self.mesh.split(':')[-1]):
                        cmds.addAttr(self.sf_mesh_ctl_grp,
                                     longName = self.mesh.split(':')[-1],
                                     shortName = self.mesh.split(':')[-1],
                                     attributeType = 'short',
                                     min = 0,
                                     max = 1,
                                     defaultValue = 1,
                                     keyable = True)
                        cmds.setAttr(self.sf_mesh_ctl_grp + '.' + 
                                     self.mesh.split(':')[-1],
                                     edit = True,
                                     channelBox = True)
            else:
                if not cmds.objExists(self.sf_mesh_ctl_grp + '.' + self.mesh):
                    cmds.addAttr(self.sf_mesh_ctl_grp,
                                 longName = self.mesh,
                                 shortName = self.mesh,
                                 attributeType = 'short',
                                 min = 0,
                                 max = 1,
                                 defaultValue = 1,
                                 keyable = True)
                    cmds.setAttr(self.sf_mesh_ctl_grp + '.' + self.mesh,
                                 edit = True,
                                 channelBox = True)                    
        #--- sculpt_group.envelope
        if not cmds.objExists(self.sf_mesh_ctl_grp + '.ENVELOPE'):
            cmds.addAttr(self.sf_mesh_ctl_grp,
                         longName = 'ENVELOPE',
                         shortName = 'ENVELOPE',
                         attributeType = 'float',
                         min = 0.0,
                         max = 1.0,
                         defaultValue = 1.0,
                         keyable = True)
            cmds.setAttr(self.sf_mesh_ctl_grp + '.ENVELOPE',
                         edit = True,
                         channelBox = True)
        #--- sculpt_control.sculpt
        cmds.addAttr(self.sf_mesh_ctl,
                     longName = 'sculpt',
                     shortName = 'sculpt',
                     attributeType = 'short',
                     min = 0,
                     max = 1,
                     defaultValue = 1,
                     keyable = True)
        #--- sculpt_control.blendValue
        cmds.addAttr(self.sf_mesh_ctl,
                     longName = 'blendValue',
                     shortName ='blendValue',
                     attributeType = 'double',
                     min = 0.00,
                     max = 1.00,
                     defaultValue = 0.00,
                     keyable = True)
        #--- sculpt_control.frameNumber
        cmds.addAttr(self.sf_mesh_ctl,
                     longName = 'frameNumber',
                     shortName = 'frameNumber',
                     attributeType = 'float')
        cmds.setAttr(self.sf_mesh_ctl + '.frameNumber',
                     self.current_frame,
                     edit = True,
                     channelBox = True,
                     lock = True)
    #end def __add_sculpt_control_attributes()

    def __connect_sculpt_control(self):      
        #--- this method connects the attributes of the sculpt group and control
        #--- sculpt group
        if '|' in self.mesh:
            if not cmds.isConnected(self.sf_mesh_ctl_grp + '.' +
                                    self.mesh.split('|')[-1],
                                    self.mesh + '.v'):
                cmds.connectAttr(self.sf_mesh_ctl_grp + '.' +
                                 self.mesh.split('|')[-1],
                                 self.mesh + '.v', force = True)
        else:
            if ':' in self.mesh:
                if not cmds.isConnected(self.sf_mesh_ctl_grp + '.' + 
                                        self.mesh.split(':')[-1],
                                        self.mesh + '.v'):
                    cmds.connectAttr(self.sf_mesh_ctl_grp + '.' + 
                                     self.mesh.split(':')[-1],
                                     self.mesh + '.v', force = True)
            else:
                if not cmds.isConnected(self.sf_mesh_ctl_grp + '.' + self.mesh,
                                        self.mesh + '.v'):
                    cmds.connectAttr(self.sf_mesh_ctl_grp + '.' + self.mesh,
                                     self.mesh + '.v', force = True)
        #--- sculpt control
        cmds.connectAttr(self.sf_mesh_ctl + '.sculpt',
                         self.mesh_sculpt + '.v')
        if cmds.objExists(self.mesh_bsp + '.' + self.mesh_result):
            cmds.connectAttr(self.sf_mesh_ctl + '.blendValue',
                             self.mesh_bsp + '.' + self.mesh_result)
        #--- check if the envelope of the blendShapes is connected
        #--- with the sculpt_tool envelope attribute
        if not cmds.isConnected(self.sf_mesh_ctl_grp + '.ENVELOPE',
                                self.sculpt_bsp + '.envelope'):
            #--- connect the envelope of the blendShapes
            #--- with the sf_mesh_ctl envelope attribute
            cmds.connectAttr(self.sf_mesh_ctl_grp + '.ENVELOPE',
                             self.sculpt_bsp + '.envelope')
        if '|' in self.mesh:
            cmds.setAttr(self.sf_mesh_ctl_grp + '.' + self.mesh.split('|')[-1], 0)
        else:
            if ':' in self.mesh:
                cmds.setAttr(self.sf_mesh_ctl_grp + '.' + 
                             self.mesh.split(':')[-1], 0)
            else:
                cmds.setAttr(self.sf_mesh_ctl_grp + '.' + self.mesh, 0)
        cmds.setAttr(self.sf_mesh_ctl_grp + '.ENVELOPE', 1)
    #end def __connect_sculpt_control

    def __setup_sculpt_shader(self):
        #--- this method setups the sculpt shader color
        #--- list all the shader names
        shader_list = 'sculptShaderCyan'
        #--- check if shader exists, else create a new one
        for s in range(len(shader_list)):
            if cmds.objExists(shader_list[s]):
                #--- check which mesh is selected
                shader = shader_list
                shader_set = shader_list + '3SG'
            else:
                #--- create the lambert shader
                shader = cmds.shadingNode('lambert',
                                          asShader = True,
                                          name = shader_list)
                shader_set = cmds.sets(shader,
                                       renderable = True,
                                       noSurfaceShader = True,
                                       empty = True,
                                       name = shader_list + '3SG')
                cmds.connectAttr(shader + '.outColor',
                                 shader_set + '.surfaceShader',
                                 force = True)
        #--- change the color
        cmds.setAttr(shader + '.color', 0, 1, 1)
        #--- assign the shader to the sculpt_mesh
        cmds.sets(self.mesh_sculpt, forceElement = shader_set)
    #end def __setup_sculpt_shader()

    def __set_key(self):
        #--- this method sets automatically a keyFrame at the currentFrame
        #--- set currentFrame
        cmds.currentTime(self.current_frame)
        #--- set a keyFrame at current time
        cmds.setKeyframe(self.sf_mesh_ctl + '.blendValue', value = 1)
    #end def __set_key()

    def __set_triple_key(self, offset = 1):
        #--- this method sets 3 keys on the current(1), pre(0) and post(0) frame
        if offset:
            #--- set currentFrame
            cmds.currentTime(self.current_frame)
            #--- set a keyFrame at current time
            cmds.setKeyframe(self.sf_mesh_ctl + '.blendValue', value = 1)
            #--- set key one frame before currentFrame
            pre = self.current_frame -offset
            cmds.currentTime(pre)
            cmds.setKeyframe(self.sf_mesh_ctl + '.blendValue', value = 0)
            #--- set key one frame after currentFrame
            post = self.current_frame + offset
            cmds.currentTime(post)
            cmds.setKeyframe(self.sf_mesh_ctl + '.blendValue', value = 0)
            #--- go back to currentFrame
            cmds.currentTime(self.current_frame)
        else:
            self.__set_key()
    #end __set_triple_key()

    def __cleanup(self):
        #--- this method cleans up the shotFinal tool
        #--- lock SF nodes
        to_lock = [self.sf_mesh_ctl, self.mesh_sculpt,
                   self.mesh_negative, self.mesh_result]
        for obj in to_lock:
            for attr in 'trs':
                for axis in 'xyz':
                    cmds.setAttr(obj + '.' + attr + axis,
                                 lock = True, keyable = False)
                    cmds.setAttr(obj + '.' + attr + axis,
                                 lock = True, keyable = False)
                    cmds.setAttr(obj + '.' + attr + axis,
                                 lock = True, keyable = False)
                cmds.setAttr(obj + '.v', lock = True, keyable = False)
                cmds.setAttr(obj + '.ihi', 0)
        #--- lock isHistoricalInteresting
        to_ihi = [self.mesh_sculpt, self.mesh_negative, self.mesh_result,
                  self.sculpt_bsp, self.mesh_bsp]
        for obj in to_ihi:
            cmds.setAttr(obj + '.ihi', 0)
            rel = cmds.listRelatives(obj, allDescendents = True)
            if rel:
                for i in rel:
                    cmds.setAttr(i + '.ihi', 0)
    #end def __cleanup()

    def __create(self):
        #--- this is the create method
        #--- create the blendShape meshes
        self.__create_blendshape_meshes()
        #--- setup the blendShape meshes
        self.__setup_blendshape_meshes()
        #--- create sculpt control
        self.__create_sculpt_control()
        #--- add sculpt control attributes
        self.__add_sculpt_control_attributes()
        #--- connect sculpt control attributes
        self.__connect_sculpt_control()
        #--- setup sculpt mesh shader
        self.__setup_sculpt_shader()
        #--- keyFrame setup
        if self.tripleKey:
            #--- set a tripleKeyFrame
            self.__set_triple_key(offset = self.tripleKeyOffset)
        else:
            #--- set a keyFrame
            self.__set_key()
        #---  cleanup the shotFinal tool
        self.__cleanup()
        #--- select the shotFinal sculpt control
        cmds.select(self.sf_mesh_ctl)
    #end def __create()
#end class ShotFinalMain()


class RemoveShotFinal():
    '''
    This is the remove class of the ShotFinal Tool
    '''

    def __init__(self):
        ########################################################################
        #vars
        self.mesh           = None
        self.mesh_sculpt    = None
        self.mesh_negative  = None
        self.mesh_result    = None
        self.mesh_bsp       = None

        self.sf_sculpt      = None
        self.sf_negative    = None
        self.sf_result      = None
        self.sf_bsp_grp     = None
        self.sf_blendshapes = None

        self.sf_mesh_ctl     = None
        self.sf_mesh_ctl_grp = None
        self.sf_char_ctl_grp = None
        self.sf_controls     = None

        self.sf_mesh_abc     = None
        self.sf_mesh_abc_grp = None
        self.sf_originals    = None

        self.shotfinaling = None
        self.character    = None
        self.mesh_grp     = None
        self.target_index = 1

        #methods
        self.__create()
    #end def __init__()

    def __check_scene(self):
        #--- this method checks the scene and stores the nodes
        sel = cmds.ls(selection = True)
        if sel:
            #--- check if selection is a sculpt mesh
            if '_SCULPT' in sel[0]:
                #--- MESHES
                #--- get the final mesh
                self.mesh = sel[0].split('_SCULPT')[0]
                #--- get the mesh sculpt
                self.mesh_sculpt = sel[0]
                #--- get the mesh negative
                self.mesh_negative = (sel[0].split('_SCULPT')[0] + '_NEGATIVE'
                                      + sel[0].split('_SCULPT')[-1])
                #--- get the mesh result
                self.mesh_result = (sel[0].split('_SCULPT')[0] + '_RESULT'
                                    + sel[0].split('_SCULPT')[-1])
                #--- get the mesh bsp
                self.mesh_bsp = cmds.listConnections(self.mesh_result + 
                                                     '.original')[0]

                #--- BLENDSHAPE GROUPS
                #--- get the sculpt group
                self.sf_sculpt = cmds.listRelatives(self.mesh_sculpt, 
                                                    parent = True)[0]
                #--- get the negative group
                self.sf_negative = cmds.listRelatives(self.mesh_negative, 
                                                      parent = True)[0]
                #--- get the result group
                self.sf_result = cmds.listRelatives(self.mesh_result, 
                                                    parent = True)[0]
                #--- get the bsp grp
                self.sf_bsp_grp = cmds.listRelatives(self.sf_sculpt, 
                                                     parent = True)[0]
                #--- get the blendShapes
                self.sf_blendshapes = cmds.listRelatives(self.sf_bsp_grp, 
                                                         parent = True)[0]

                #--- CONTROLS
                #--- get the mesh control
                self.sf_mesh_ctl = cmds.listConnections(self.mesh_sculpt)[0]
                #--- get the mesh control group
                self.sf_mesh_ctl_grp = cmds.listRelatives(self.sf_mesh_ctl, 
                                                          parent = True)[0]
                #--- get the char control group
                self.sf_char_ctl_grp = cmds.listRelatives(self.sf_mesh_ctl_grp, 
                                                          parent = True)[0]
                #--- get the controls group
                self.sf_controls = cmds.listRelatives(self.sf_char_ctl_grp, 
                                                      parent = True)[0]

                #--- ORIGINALS
                #--- get the original mesh
                self.sf_mesh_abc = cmds.listConnections(self.mesh + '.original')[0]
                #--- get the original mesh group
                self.sf_mesh_abc_grp = cmds.listRelatives(self.sf_mesh_abc, 
                                                          parent = True,
                                                          fullPath = True)[0]
                #--- get the originals group
                self.sf_originals = cmds.listRelatives(self.sf_mesh_abc_grp, 
                                                       parent = True)[0]
                #--- ADDITIONALS
                #--- get target index
                self.target_index = cmds.blendShape(self.mesh_bsp, 
                                                    query = True, 
                                                    target = True).index(self.mesh_result)
                #--- get character name
                parent = cmds.listRelatives(sel[0], parent = True)[0]
                self.character = parent.split('SF_')[-1].split('_SCULPTS')[0]
                #--- get parent of the final mesh
                sel = cmds.ls(self.mesh)
                if '|' in sel[0]:
                    for i in sel:
                        if i.split('|')[0] == self.character:
                            self.mesh = i
                            break
                self.mesh_grp = cmds.listRelatives(self.mesh, 
                                                   parent = True, 
                                                   fullPath = True)[0]
                #--- get the shotFinaling group
                self.shotfinaling = cmds.listRelatives(self.sf_originals, 
                                                       parent = True)[0]
            else:
                raise Exception('Selected object is not a sculpt mesh!')
        else:
            raise Exception('You have to select a sculpt mesh!')
    #end def__check_scene()

    def __remove_blendshapes(self):
        #--- this method removes the blendShape nodes
        #--- remove blendShape connection
        cmds.blendShape(self.mesh_bsp, 
                        edit = True, 
                        topologyCheck = False, 
                        remove = True, 
                        target = ((self.mesh, self.target_index, self.mesh_result, 1),
                                  (self.mesh, self.target_index, self.mesh, 1)))
        #--- remove the sculpt mesh
        cmds.delete(self.mesh_sculpt)
        #--- remove the negative mesh
        cmds.delete(self.mesh_negative)
        #--- remove the result mesh
        cmds.delete(self.mesh_result)

        #--- delete the sculpt group
        if not cmds.listRelatives(self.sf_sculpt, allDescendents = True):
            cmds.delete(self.sf_sculpt)
        #--- delete the negative group
        if not cmds.listRelatives(self.sf_negative, allDescendents = True):
            cmds.delete(self.sf_negative)
        #--- delete the result group
        if not cmds.listRelatives(self.sf_result, allDescendents = True):
            cmds.delete(self.sf_result)

        #--- delete the bsp grp
        if not cmds.listRelatives(self.sf_bsp_grp, allDescendents = True):
            cmds.delete(self.sf_bsp_grp)
        #--- delete the blendShapes grp
        if not cmds.listRelatives(self.sf_blendshapes, allDescendents = True):
            cmds.delete(self.sf_blendshapes)
    #end def __remove_blendshapes()

    def __remove_controls(self):
        #--- this method removes the controls
        #--- remove the mesh control
        cmds.delete(self.sf_mesh_ctl)

        #--- delete the mesh ctl grp
        if not cmds.listRelatives(self.sf_mesh_ctl_grp, allDescendents = True):
            cmds.delete(self.sf_mesh_ctl_grp)
        #--- delete the char ctl grp
        if not cmds.listRelatives(self.sf_char_ctl_grp, allDescendents = True):
            cmds.delete(self.sf_char_ctl_grp)
        #--- delete the controls group
        if not cmds.listRelatives(self.sf_controls, allDescendents = True):
            cmds.delete(self.sf_controls)
    #end def __remove_controls()

    def __restore_originals(self):
        #--- this method restores the original state
        #--- list the sculpts in the sculpts group
        if not cmds.objExists(self.sf_sculpt):
            if cmds.listRelatives(self.sf_mesh_abc_grp, 
                                  children = True, 
                                  fullPath = True):
                rel = cmds.listRelatives(self.sf_mesh_abc_grp, 
                                         children = True)
                character = self.character + '_'
                for abc in rel:
                    if '|' in self.mesh:
                        mesh = self.mesh.split('|')[-1]
                        mesh = character + mesh + '_ABC'
                    else:
                        mesh = character + self.mesh + '_ABC'
                    sel = cmds.ls(mesh)
                    if sel:
                        if '|' in sel[0]:
                            for i in sel:
                                if i.split('|')[0] == self.character:
                                    mesh = i
                                    break
                    #--- get the parent of the original mesh
                    if cmds.objExists(mesh):
                        mesh_grp = cmds.listRelatives(mesh, 
                                                      parent = True, 
                                                      fullPath = True)[0]
                        #--- rename the original mesh
                        for obj in cmds.listRelatives(mesh_grp, children = True):
                            par = cmds.ls(obj.split(character)[-1].split('_ABC')[0])
                            for i in par:
                                if '|' in i:
                                    ori_par = i.split('|')[-2] + '_'
                                    if ori_par == character:
                                        cmds.delete(i)
                                        dup_mesh = obj.split(character)[-1].split('_ABC')[0]
                                        rnm = cmds.rename(obj, dup_mesh)
                                        #--- parent the original mesh to the mesh grp
                                        cmds.parent(rnm, i.split('|')[-2])
                                else:
                                    par_mesh = cmds.listRelatives(i, 
                                                                  parent = True, 
                                                                  fullPath = True)[0]
                                    cmds.delete(i)
                                    rnm = cmds.rename(obj, i)
                                    #--- parent the original mesh to the mesh grp
                                    cmds.parent(rnm, par_mesh)
                        #--- delete the original mesh group
                        if not cmds.listRelatives(mesh_grp, 
                                                  allDescendents = True,
                                                  fullPath = True):
                            cmds.delete(mesh_grp)
                        #--- delete the originals group
                        if not cmds.listRelatives(self.sf_originals, 
                                                  allDescendents = True,
                                                  fullPath = True):
                            cmds.delete(self.sf_originals)
        #--- delete the shotFinaling group
        if not cmds.listRelatives(self.shotfinaling, 
                                  allDescendents = True,
                                  fullPath = True):
            cmds.delete(self.shotfinaling)
    #end def __restore_originals()

    def __create(self):
        #--- this is the main creation method
        #--- check the scene
        self.__check_scene()
        #--- remove blendShapes
        self.__remove_blendshapes()
        #--- remove controls
        self.__remove_controls()
        #--- restore originals
        self.__restore_originals()
    #end def __create()

#ShotFinalMain()
#RemoveShotFinal()
