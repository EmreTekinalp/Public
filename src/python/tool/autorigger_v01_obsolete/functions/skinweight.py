'''
Created on 23.02.2014
@author: Emre Tekinalp
@e-mail: e.tekinalp@icloud.com
@website: www.gravityofexplosion.com
@brief: The skinWeights class of the AutoRigger
'''

import time
from maya import cmds


class Weights(object):
    def __init__(self):
        pass
    #END def __init__()

    def get_skin_weights(self):
        #--- this method gets the skin weight information in the scene
        #--- get the current time
        current = time.time()
        #--- get the meshes 
        m = cmds.ls(type = 'mesh')
        geo = list()
        for i in m:
            if not 'Orig' in i:
                c = cmds.listRelatives(i, parent=True)[0]
                geo.append(c)
        #--- get the skinClusters of the meshes
        meshes = list()
        shapes = list()
        skins = list()
        joints = list()
        for i in geo:
            mesh_shapes = cmds.listRelatives(i, ad=True)
            for shape in mesh_shapes:
                cnt = cmds.listConnections(shape, p=True)
                for c in cnt:
                    if 'outputGeometry[0]' in c:
                        if 'skinCluster' in c:
                            skins.append(c.split('.')[0])
            shapes.append(shape)                
            meshes.append(i)

        #--- get the skin joints
        jnt = cmds.ls('*JNT', type = 'joint')
        for j in jnt:
            if cmds.objExists(j + '.SKIN'):
                if not 'IK_JNT' in j:
                    if not 'FK_JNT' in j:
                        joints.append(j)
        return meshes, shapes, skins, joints
        #--- list all the joints in the scene and the vertices of the meshes
        jnt = cmds.ls('*JNT', type = 'joint')
        verts=list()
        for mesh in meshes:
            vtx = cmds.ls(mesh + '.vtx[*]', flatten=True)
            verts.append(vtx)
        #--- get the mesh, skinCluster, joint, vertice and weight information
        weights = list()    
        for i, skin, mesh in zip(verts, skins, meshes):
            for j in jnt:
                if cmds.objExists(j + '.SKIN'):
                    if not 'IK_JNT' in j:
                        if not 'FK_JNT' in j:
                            try:
                                for w in i:
                                    val = cmds.skinPercent(skin, w, transform=j, query=True )
                                    result = [mesh, skin, j, w, val]
                                    weights.append(result)
                            except:
                                pass
        #--- calculate the time for saving the weights(I know it's slow :()
        t = (time.time() - current)
        print 'seconds: ', t
        return weights
    #END def get_skin_weights()
#END class Weights()
