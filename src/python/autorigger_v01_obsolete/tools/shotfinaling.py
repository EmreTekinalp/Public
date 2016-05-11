'''
Created on 11.11.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: This is the shotFinaling class
'''

import time
from maya import cmds


class ShotFinal():
    '''
    This is the ShotFinal Tool 2.0
    '''

    def __init__(self,
                  key = False,
                  version = 2.0):
        ########################################################################
        #vars
        self.mesh               = None
        self.currentFrame       = None
        self.time_stamp         = None
        self.sf_final_meshes    = None
        self.shotfinaling       = None
        self.blendshapes        = None
        self.mesh_shotfinal_grp = None
        self.mesh_bsp_grp       = None
        self.sculpt_grp         = None
        self.negative_grp       = None
        self.result_grp         = None
        self.final_mesh         = None
        self.final_bsp          = None
        self.sculpt_mesh        = None
        self.negative_mesh      = None
        self.result_mesh        = None
        self.result_bsp         = None
        self.plug_num           = 0
        self.shader             = []
        self.shader_set         = []
        self.sf_tool            = []
        self.sub_tool           = []
        self.sculpt_tool        = []
        #methods
        self.__create(key = key,
                      version = version)
    #end def __init__()

    def __check_scene(self):
        #--- this method checks the scene
        #--- check if something is selected
        sel = cmds.ls(selection = True)
        if sel:
            #--- check if selection is a mesh
            transform = None
            for i in sel:
                if cmds.nodeType(i) == 'transform':
                    transform = i
            if cmds.listRelatives(transform, allDescendents = True, type = 'mesh'):
                mesh = cmds.listRelatives(transform,
                                          allDescendents = True,
                                          type = 'mesh')[0]
                if cmds.nodeType(mesh) == 'mesh':
                    #--- store the mesh
                    self.mesh = transform
                    #--- get current frame
                    self.currentFrame = cmds.currentTime(query = True)
                    #--- get timestamp
                    ts = str(time.time())
                    self.time_stamp = str(ts.split('.')[0] + ts.split('.')[1])
                else:
                    raise Exception('The selected object is not a mesh!')
            else:
                raise Exception('The selected object is not a mesh!')
        else:
            raise Exception('You have to select a mesh, dude!')
    #end def __check_scene()

    def __setup_scene(self):
        #--- this method creates the proper shotFinaling groups
        #--- check if the sf final meshes group exists
        if cmds.objExists('SF_FINAL_MESHES'):
            self.sf_final_meshes = 'SF_FINAL_MESHES'
        else:
            self.sf_final_meshes = cmds.createNode('transform',
                                                   name = 'SF_FINAL_MESHES')
        #--- check if the shotFinaling group exists
        if cmds.objExists('SHOTFINALING'):
            self.shotfinaling = 'SHOTFINALING'
        else:
            self.shotfinaling = cmds.createNode('transform',
                                                name = 'SHOTFINALING')
        #--- check if the blendShapes group exists
        if cmds.objExists('BLENDSHAPES'):
            self.blendshapes = 'BLENDSHAPES'
        else:
            self.blendshapes = cmds.createNode('transform',
                                               name = 'BLENDSHAPES',
                                               parent = self.shotfinaling)
        #--- check if the mesh shotFinaling group exists
        if cmds.objExists('SHOTFINAL_GRP'):
            self.mesh_shotfinal_grp = 'SHOTFINAL_GRP'
        else:
            self.mesh_shotfinal_grp = cmds.createNode('transform',
                                                      name = ('SHOTFINAL_GRP'),
                                                      parent = self.shotfinaling)
        #--- check if the mesh blendShape group exists
        if cmds.objExists(self.mesh + '_BSP_GRP'):
            self.mesh_bsp_grp = self.mesh + '_BSP_GRP'
        else:
            self.mesh_bsp_grp = cmds.createNode('transform',
                                                name = self.mesh + '_BSP_GRP',
                                                parent = self.blendshapes)
        #--- check if the sculpt group exists
        if cmds.objExists(self.mesh + '_SCULPT_GRP'):
            self.sculpt_grp = self.mesh + '_SCULPT_GRP'
        else:
            self.sculpt_grp = cmds.createNode('transform',
                                              name = self.mesh + '_SCULPT_GRP',
                                              parent = self.mesh_bsp_grp)
        #--- check if the negative group exists
        if cmds.objExists(self.mesh + '_NEGATIVE_GRP'):
            self.negative_grp = self.mesh + '_NEGATIVE_GRP'
        else:
            self.negative_grp = cmds.createNode('transform',
                                                name = self.mesh + '_NEGATIVE_GRP',
                                                parent = self.mesh_bsp_grp)
        #--- check if the result group exists
        if cmds.objExists(self.mesh + '_RESULT_GRP'):
            self.result_grp = self.mesh + '_RESULT_GRP'
        else:
            self.result_grp = cmds.createNode('transform',
                                              name = self.mesh + '_RESULT_GRP',
                                              parent = self.mesh_bsp_grp)
    #end def __setup_scene()

    def __setup_final_meshes(self):
        #--- this method setups the final meshes
        if 'FINAL' in self.mesh:
            if cmds.objExists(self.mesh):
                self.final_mesh = self.mesh
            else:
                self.final_mesh = cmds.duplicate(self.mesh)
                cmds.parent(self.final_mesh, self.sf_final_meshes)
                final_name = cmds.rename(self.final_mesh,
                                         self.mesh)
                self.final_mesh = final_name
        else:
            if cmds.objExists(self.mesh + 'FINAL'):
                self.final_mesh = self.mesh + 'FINAL'
            else:
                self.final_mesh = cmds.duplicate(self.mesh)
                cmds.parent(self.final_mesh, self.sf_final_meshes)
                final_name = cmds.rename(self.final_mesh,
                                         self.mesh + 'FINAL')
                self.final_mesh = final_name

        if cmds.objExists(self.mesh + '_BSP'):
            #--- setup blendShape deformer
            self.final_bsp = self.mesh + '_BSP'
            cmds.setAttr(self.final_bsp + '.' + self.mesh, 1)
            cmds.setAttr(self.mesh + '.v', 0)
        else:
            if 'FINAL' in self.mesh:
                self.mesh = self.mesh.split('FINAL')[0]
            self.final_bsp = cmds.blendShape(self.mesh,
                                             self.final_mesh,
                                             name = self.mesh + '_BSP')[0]
            cmds.setAttr(self.final_bsp + '.' + self.mesh, 1)
            cmds.setAttr(self.mesh + '.v', 0)
    #end def __setup_final_meshes()

    def __setup_blendshapes(self):
        #--- this method creates the proper blendShape setup
        #--- create sculpt duplicate from the current selected mesh
        self.sculpt_mesh = cmds.duplicate(self.mesh)
        cmds.parent(self.sculpt_mesh,  self.sculpt_grp)
        sculpt_name = cmds.rename(self.sculpt_mesh,
                                  self.mesh + 'Sculpt' + self.time_stamp)
        self.sculpt_mesh = sculpt_name
        #--- create negative duplicate from the current selected mesh
        self.negative_mesh = cmds.duplicate(self.mesh)
        cmds.parent(self.negative_mesh, self.negative_grp)
        negative_name = cmds.rename(self.negative_mesh,
                                    self.mesh + 'Negative' + self.time_stamp)
        self.negative_mesh = negative_name
        #--- create neutral duplicate from the current selected mesh
        if cmds.objExists(self.final_bsp):
            cmds.setAttr(self.final_bsp + '.envelope', 0)
            self.result_mesh = cmds.duplicate(self.mesh)
            cmds.parent(self.result_mesh,  self.result_grp)
            result_name = cmds.rename(self.result_mesh,
                                      self.mesh + 'Result' + self.time_stamp)
            cmds.setAttr(self.final_bsp + '.envelope', 1)
        else:
            self.result_mesh = cmds.duplicate(self.mesh)
            cmds.parent(self.result_mesh,  self.result_grp)
            result_name = cmds.rename(self.result_mesh,
                                      self.mesh + 'Result' + self.time_stamp)
        #--- store the result mesh
        self.result_mesh = result_name
        #--- create the sculpt and negative blendShapes and set them up
        self.result_bsp = cmds.blendShape(self.sculpt_mesh,
                                          self.negative_mesh,
                                          self.result_mesh,
                                          name = self.mesh + 'Result_BSP')[0]
        #--- check for namespaces in the mesh
        if ':' in self.sculpt_mesh:
            sculpt_mesh = self.sculpt_mesh.split(':')[-1]
            negative_mesh = self.negative_mesh.split(':')[-1]
        else:
            sculpt_mesh = self.sculpt_mesh
            negative_mesh = self.negative_mesh
        #--- set positive and negative values for the resulting blendShape
        cmds.setAttr(self.result_bsp + '.' + sculpt_mesh, 1, lock = True)
        cmds.setAttr(self.result_bsp + '.' + negative_mesh, -1, lock = True)
        #--- get the targetIndex to create the blendShape
        if self.final_bsp:
            if cmds.objExists(self.final_bsp):
                world_mesh = cmds.listConnections(self.final_bsp + '.inputTarget',
                                                  plugs = True)
                cnt = cmds.listConnections(world_mesh,
                                           plugs = True,
                                           destination = True)[-1].split('.')[2].split('[')[1].split(']')[0]
                plug = int(cnt) + 1
                plug_list = []
                for i in world_mesh:
                    plug_list.append(int(cmds.listConnections(i,
                                                              plugs = True,
                                                              destination = True)[0].split('.')[2].split('[')[1].split(']')[0]))
                for plug in range(len(plug_list) + 1):
                    if plug not in plug_list:
                        #--- check free plugs
                        self.plug_num = str(plug)
                        break
                cmds.blendShape(self.final_bsp,
                                edit = True,
                                target = (self.final_mesh,
                                          plug,
                                          self.result_mesh,
                                          1.0))
                self.plug_num = str(plug)
        else:
            raise Exception('The final mesh blendShape is missing!')
    #end def __setup_blendshapes()

    def __setup_sculpt_shader(self):
        #--- this method setups the sculpt shader color
        #--- list all the shader names
        shader_list = ['sculptShaderGreen']
        #--- check if shader exists, else create a new one
        for s in range(len(shader_list)):
            if cmds.objExists(shader_list[s]):
                #--- check which mesh is selected
                self.shader = shader_list[0]
                self.shader_set = shader_list[0] + '3SG'
            else:
                #--- create the lambert shader
                self.shader = cmds.shadingNode('lambert',
                                               asShader = True,
                                               name = shader_list[0])
                self.shader_set = cmds.sets(self.shader,
                                            renderable = True,
                                            noSurfaceShader = True,
                                            empty = True,
                                            name = shader_list[0] + '3SG')
                cmds.connectAttr(self.shader + '.outColor',
                                 self.shader_set + '.surfaceShader',
                                 force = True)
        #--- change the color
        cmds.setAttr(self.shader + '.color', 0, 1, 1)
        #--- assign the shader to the sculpt_mesh
        cmds.sets(self.sculpt_mesh, forceElement = self.shader_set)
    #end def __setup_sculpt_shader()

    def __setup_shotfinal_controls(self):
        #--- check if shotFinaling tools exists
        if cmds.objExists(self.mesh + '_SHOTFINALING_TOOL'):
            self.sf_tool = self.mesh + '_SHOTFINALING_TOOL'
            if cmds.objExists(self.mesh + '_TOOL'):
                self.sub_tool = self.mesh + '_TOOL'
            else:
                self.sub_tool = cmds.createNode('transform',
                                                name = self.mesh + '_TOOL',
                                                parent = self.sf_tool)
        else:
            self.sf_tool = cmds.createNode('transform',
                                           name = self.mesh + '_SHOTFINALING_TOOL',
                                           parent = self.mesh_shotfinal_grp)
            self.sub_tool = cmds.createNode('transform',
                                            name = self.mesh + '_TOOL',
                                            parent = self.sf_tool)
 
        #--- create the sculpt_tool and parent them under the sub_tool
        if cmds.objExists(self.mesh + self.plug_num):
            self.plug_num = int(self.plug_num) + 1
            self.sculpt_tool = cmds.createNode('transform',
                                               name = self.mesh + str(self.plug_num),
                                               parent = self.sub_tool)       
        else:
            self.sculpt_tool = cmds.createNode('transform',
                                               name = self.mesh + self.plug_num,
                                               parent = self.sub_tool)
 
        #--- remove all unnecessary transform attributes
        for axis in 'xyz':
            cmds.setAttr(self.sub_tool + '.t' + axis, lock = True, keyable = False)
            cmds.setAttr(self.sub_tool + '.r' + axis, lock = True, keyable = False)
            cmds.setAttr(self.sub_tool + '.s' + axis, lock = True, keyable = False)
            cmds.setAttr(self.sculpt_tool + '.t' + axis, lock = True, keyable = False)
            cmds.setAttr(self.sculpt_tool + '.r' + axis, lock = True, keyable = False)
            cmds.setAttr(self.sculpt_tool + '.s' + axis, lock = True, keyable = False)
        cmds.setAttr(self.sculpt_tool + '.v', lock = True, keyable = False)
        cmds.setAttr(self.sculpt_tool + '.v', lock = True, keyable = False)
        #--- create the attributes for the sub tool group
        if ':' in self.mesh:
            mesh = self.mesh.split(':')[-1]
            result_mesh = self.result_mesh.split(':')[-1]
        else:
            mesh = self.mesh
            result_mesh = self.result_mesh
        if not cmds.objExists(self.sub_tool + '.' + mesh):
            cmds.addAttr(self.sub_tool,
                         longName = mesh,
                         shortName = mesh,
                         attributeType = 'short',
                         min = 0,
                         max = 1,
                         defaultValue = 1,
                         keyable = True)
            cmds.setAttr(self.sub_tool + '.' + mesh,
                         edit = True,
                         channelBox = True)
        if not cmds.objExists(self.sub_tool + '.' + mesh + '_ENVELOPE'):
            cmds.addAttr(self.sub_tool,
                         longName = mesh + '_ENVELOPE',
                         shortName = mesh + '_ENVELOPE',
                         attributeType = 'float',
                         min = 0.0,
                         max = 1.0,
                         defaultValue = 1.0,
                         keyable = True)
            cmds.setAttr(self.sub_tool + '.' + mesh + '_ENVELOPE',
                         edit = True,
                         channelBox = True)
        cmds.addAttr(self.sculpt_tool,
                     longName = mesh + '_Sculpt',
                     shortName = mesh + '_Sculpt',
                     niceName = mesh + '_Sculpt',
                     attributeType = 'short',
                     min = 0,
                     max = 1,
                     defaultValue = 1,
                     keyable = True)
        cmds.addAttr(self.sculpt_tool,
                     longName = mesh + '_BlendValue',
                     shortName = mesh + '_BlendValue',
                     niceName = mesh + '_BlendValue',
                     attributeType = 'double',
                     min = 0.00,
                     max = 1.00,
                     defaultValue = 0.00,
                     keyable = True)
        cmds.addAttr(self.sculpt_tool,
                     longName = mesh + '_FrameNumber',
                     shortName = mesh + '_FrameNumber',
                     niceName = mesh + '_FrameNumber',
                     attributeType = 'float')
        cmds.setAttr(self.sculpt_tool + '.' + mesh + '_FrameNumber',
                     self.currentFrame,
                     edit = True,
                     channelBox = True,
                     lock = True)

        #--- connect the subTool attributes with the bshpe attributes
        if not cmds.isConnected(self.sub_tool + '.' + mesh, self.final_mesh + '.v'):
            cmds.connectAttr(self.sub_tool + '.' + mesh,
                             self.final_mesh + '.v', force = True)
        cmds.connectAttr(self.sculpt_tool + '.' + mesh + '_Sculpt',
                         self.sculpt_mesh + '.v')
        if cmds.objExists(self.final_bsp + '.' + result_mesh):
            cmds.connectAttr(self.sculpt_tool + '.' + mesh + '_BlendValue',
                             self.final_bsp + '.' + result_mesh)

        #--- check if the envelope of the blendShapes is connected
        #--- with the sculpt_tool envelope attribute
        sel = cmds.ls(self.final_bsp, type = 'blendShape')
        if sel:
            for i in sel:
                if not cmds.isConnected(self.sub_tool + '.' + mesh + '_ENVELOPE',
                                        i + '.envelope'):
                    #--- connect the envelope of the blendShapes
                    #--- with the sculpt_tool envelope attribute
                    cmds.connectAttr(self.sub_tool + '.' + mesh + '_ENVELOPE',
                                     i + '.envelope')
        #--- disable the selected mesh's visibility
        cmds.setAttr(self.sub_tool + '.' + mesh, 0)
        cmds.setAttr(self.sub_tool + '.' + mesh + '_ENVELOPE', 1)
    #end def __setup_shotfinal_controls

    def __set_keyframe(self):
        #--- this method sets automatically a keyFrame at the currentFrame
        if ':' in self.mesh:
            mesh = self.mesh.split(':')[-1]
        else:
            mesh = self.mesh
        #--- get the attributeNumber of the selected sculpt
        self.currentFrame
        #set keyFrame at current time
        cmds.setKeyframe(self.sculpt_tool + '.' + mesh + '_BlendValue', value = 1)
    #end def __set_keyframe()

    def __set_keyframe_at_frame(self):
        #--- this method sets a keyframe on the current frame with a value of 1
        #--- and sets on the frames before and after a keyframe with a value of 0
        if ':' in self.mesh:
            mesh = self.mesh.split(':')[-1]
        else:
            mesh = self.mesh        
        #--- set currentFrame
        self.currentFrame
        cmds.setKeyframe(self.sculpt_tool + '.' + mesh + '_BlendValue', value = 1)
        #--- set key one frame before currentFrame
        pre = self.currentFrame -1
        cmds.currentTime(pre)
        cmds.setKeyframe(self.sculpt_tool + '.' + mesh + '_BlendValue', value = 0)
        #--- set key one frame after currentFrame
        post = self.currentFrame + 1
        cmds.currentTime(post)
        cmds.setKeyframe(self.sculpt_tool + '.' + mesh + '_BlendValue', value = 0)
        #--- go back to currentFrame
        cmds.currentTime(self.currentFrame)
    #end def__set_keyframe_at_frame()

    def __cleanup(self, version = 2.0):
        #--- hide groups and lock attributes
        cmds.setAttr(self.negative_grp + '.v', 0)
        cmds.setAttr(self.result_grp + '.v', 0)
        sf_objs = cmds.ls(self.sf_tool, self.blendshapes, self.shotfinaling,
                         self.mesh_bsp_grp, self.mesh_shotfinal_grp,
                         self.negative_grp, self.sculpt_grp, self.result_grp,
                         '*Negative*', '*Sculpt*', '*Result*', type = 'transform')
        for i in sf_objs:
            for axis in 'xyz':
                cmds.setAttr(i + '.t' + axis, lock = 1, keyable = 0)
                cmds.setAttr(i + '.r' + axis, lock = 1, keyable = 0)
                cmds.setAttr(i + '.s' + axis, lock = 1, keyable = 0)
            cmds.setAttr(i + '.v', keyable = 0)
            cmds.setAttr(i + '.ihi', 0)
        #--- hide isHistoricallyInteresting
        to_ihi = cmds.ls('*BSP*', '*Bshpe*', '*tweak*', '*Shape*')
        for i in sf_objs:
            to_ihi.append(i)
        for i in to_ihi:
            cmds.setAttr(i + '.ihi', 0)
        #--- add versionNumber of the SHOTFINAL script
        if not cmds.objExists(self.shotfinaling + '.version'):
            cmds.addAttr(self.shotfinaling,
                         longName = 'version',
                         shortName = 'version',
                         attributeType = 'float',
                         keyable = True)
            cmds.setAttr(self.shotfinaling + '.version',
                         version,
                         edit  = True,
                         channelBox = True,
                         lock = True)
        #--- select the sculpt tool
        cmds.select(self.sculpt_tool)
    #end def __cleanup()
 
    def __create(self,
                 key = False,
                 version = 2.0):
        #--- this is the main create method
        self.__check_scene()
        self.__setup_scene()
        self.__setup_final_meshes()
        self.__setup_blendshapes()
        self.__setup_sculpt_shader()
        self.__setup_shotfinal_controls()
        if key:
            self.__set_keyframe_at_frame()
        else:
            self.__set_keyframe()
        self.__cleanup(version = version)
    #end def __create()
#class ShotFinal()


class RemoveShotFinal():
    '''
    This is the remove class of the ShotFinal Tool
    @todo: delete all the empty transform nodes
    '''
    def __init__(self):
        #vars
        #methods
        self.__create()
    #end def __init__()
    def __remove_sculpt(self):
        #--- delete the sculpt and remove unnecessary empty nodes
        #--- store the selected sculpt in a list
        sel = cmds.ls(selection = True)
        #--- check if something is selected
        if sel:
            #--- check if selection is a sculpt mesh
            for i in sel:
                if 'Sculpt' in i:
                    #--- get the attributeNumber of the selected sculpt
                    count = i.split('Sculpt')[1]
                    #--- get the result mesh to get the blendShape node
                    result_mesh = i.split('Sculpt')[0] + 'Result' + count
                    #--- check if result mesh exists
                    if cmds.objExists(result_mesh):
                        #--- get the shape of the result_mesh
                        result_shape = cmds.listRelatives(result_mesh,
                                                          allDescendents = True)
                        #--- get the blendShape node
                        connections = cmds.listConnections(result_shape)
                        bshape  = []
                        ref_mesh = []
                        for cnt in connections:
                            if 'Bshpe' in cnt:
                                bshape.append(cnt)
                                #--- get the referenced mesh
                                mesh = cmds.listConnections(cnt, type = 'mesh')
                                for m in mesh:
                                    if result_mesh in m:
                                        ref_mesh.append(m)
                        #--- get the sculptTool
                        tool = cmds.listConnections(i)[0]
                        #--- delete the meshes and blendShape targets
                        delete_list = [i, i.split('Sculpt')[0] + 'Negative' +
                                       i.split('Sculpt')[1], result_mesh]
                        for d in delete_list:
                            if cmds.objExists(d):
                                #--- remove the blendShape Target
                                if ref_mesh:
                                    #--- get the target index
                                    index = cmds.blendShape(bshape,
                                                            query = True,
                                                            target = True).index(result_mesh)
                                    #--- remove the blendShape Target
                                    cmds.blendShape(bshape[0],
                                                    edit = True,
                                                    topologyCheck = False,
                                                    remove = True,
                                                    target = ((ref_mesh[0],
                                                               index,
                                                               result_mesh, 1),
                                                              (ref_mesh[0],
                                                               index,
                                                               ref_mesh[0], 1)))
                                #--- remove the sculpt, negative and result mesh
                                cmds.delete(i, i.split('Sculpt')[0] + 'Negative'
                                            + i.split('Sculpt')[1], result_mesh)
                        #--- delete the sculpt tool
                        if not cmds.objExists(i):
                            if not '_TOOL' in tool:
                                cmds.delete(tool)
                        #--- get the ShotFinal Tool name
                        tool_main = i.split('Sculpt')[0] + '_TOOL'
                        if cmds.listRelatives(tool_main, children = True):
                            #--- enable the first attribute of the tool_main
                            first_attr = i.split('Sculpt')[0]
                            cmds.setAttr(tool_main + '.' + first_attr, 1)
                        else:
                            tool_grp = cmds.listRelatives(tool_main,
                                                          parent = True,
                                                          type = 'transform')
                            first_attr = i.split('Sculpt')[0]
                            cmds.setAttr(tool_main + '.' + first_attr, 1)
                            #--- delete the tool_main
                            cmds.delete(tool_main)
                            #--- check if there are other tools inside that group
                            tool_child = cmds.listRelatives(tool_grp[0],
                                                            children = True)
                            if not tool_child:
                                #--- delete the object_SHOTFINALING_TOOL group
                                cmds.delete(tool_grp)
                                #--- get the blendShape group
                                bsp_grp = ('SHOTFINAL_GRP')
                                #--- check if there are any meshes inside the group
                                bsp_child = cmds.listRelatives(bsp_grp,
                                                               allDescendents = True,
                                                               type = 'transform')
                                if not bsp_child:
                                    cmds.delete(bsp_grp)
                                if not cmds.listRelatives(i.split("Sculpt")[0] +
                                                          "_SCULPT_GRP",
                                                          children = True):
                                    cmds.delete(i.split("Sculpt")[0] + '_SCULPT_GRP')
                                    cmds.delete(i.split("Sculpt")[0] + '_NEGATIVE_GRP')
                                    cmds.delete(i.split("Sculpt")[0] + '_RESULT_GRP')
                                    cmds.delete(i.split("Sculpt")[0] + '_BSP_GRP')
                                #--- check if BLENDSHAPES group is empty
                                if not cmds.listRelatives('BLENDSHAPES',
                                                          children = True):
                                    cmds.delete('BLENDSHAPES')
                                    cmds.delete(i.split("Sculpt")[0] + '_Bshpe')
                                #--- check if SHOTFINALING group is empty
                                if not cmds.listRelatives('SHOTFINALING',
                                                          children = True):
                                    cmds.delete('SHOTFINALING')
                    else:
                        raise Exception('Result mesh: ' + result_mesh +
                                        ' does not exist!')
                else:
                    raise Exception('Selected mesh: ' + i +
                                    ' is not a sculpt mesh!')
        else:
            raise Exception('Nothing is selected! Please, select a sculpt mesh!')
    #end def __remove_sculpt()
    def __create(self):
        #--- this is the main creation method
        self.__remove_sculpt()
    #end def __create()
ShotFinal()
#RemoveShotFinal()