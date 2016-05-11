'''
Created on 11.11.2013
@author: Emre Tekinalp
@e-mail: e.tekinalp@gmx.de
@website: www.gravityofexplosion.com
@brief: This is the deformer class
'''

from maya import cmds

class Deformer(object):
    '''
    This class contains all the maya internal deformers including
    blendShape, lattice, wrap, cluster, softMod, nonLinear, sculpt,
    jiggle and wire deformers
    '''

    def __init__(self):
        pass
    #end def __init__()

    def bend(self,
             character = None,
             mod = None,
             side = None,
             name = None,
             suffix = None,
             geometry = None,
             position = [0,0,0],
             rotation = [0,0,0],
             envelope = 1,
             curvature = 0,
             lowBound = -1,
             highBound = 1,
             parent = None,
             show = True,
             lockAttr = None,
             ihi = True):
        #--- this method creates a bend deformer
        #--- select the specified geometry
        cmds.select(geometry)
        #--- create a bend deformer
        node = cmds.nonLinear(type = 'bend')
        #--- filter the individual name
        filter_name = (name + node[0].split('Handle')[0][0].upper() +
                       node[0].split('Handle')[0][1:])
        #--- rename the bend deformer
        node = self.__rename_node(mod = mod,
                                  side = side,
                                  name = filter_name,
                                  suffix = suffix,
                                  obj = node)
        #--- create a group on top and parent the deformer under the group
        node_grp = cmds.createNode('transform', parent = node[0])
        cmds.parent(node_grp, world = True)
        cmds.parent(node[0], node_grp)
        #--- rename the node group
        node_grp = self.__rename_node(mod = mod,
                                      side = side,
                                      name = filter_name,
                                      suffix = 'GRP',
                                      obj = node_grp)
        #--- reposition the transform of the deformer locally
        cmds.xform(node[0], translation = position, worldSpace = False)
        cmds.xform(node[0], rotation = rotation, worldSpace = False)
        #--- take care of the node's settings
        #--- envelope
        cmds.setAttr(node[-1] + '.envelope', envelope)
        #--- curvature
        cmds.setAttr(node[-1] + '.curvature', curvature)
        #--- lowBound
        cmds.setAttr(node[-1] + '.lowBound', lowBound)
        #--- highBound
        cmds.setAttr(node[-1] + '.highBound', highBound)
        #--- parent the group under the specified parent
        if parent:
            if not isinstance(parent, list):
                cmds.parent(node_grp, parent)
            else:
                raise Exception("Specified parent: " +
                                parent + 'is not a valid')
        #--- show or hide transform
        if not show:
            cmds.setAttr(node[0] + '.v', 0)
        #--- lock specified attributes
        if lockAttr:
            if node[-1]:
                cmds.setAttr(node[-1] + '.' + lockAttr, lock = True)
        #--- set isHistoricalInteresting attribute
        if not ihi:
            for n in node:
                cmds.setAttr(n + '.ihi', 0)
        #--- return node
        return node
    #end def bend()

    def blendShape(self,
                    character = None,
                    mod = None,
                    side = None,
                    name = None,
                    suffix = None,
                    shapes = None,
                    target = None,
                    envelope = 1,
                    shapeAttr = None,
                    shapeValue = 1,
                    show = True,
                    lockAttr = None,
                    ihi = True):
        #--- this method creates a blendShape deformer
        #--- create a blendShape deformer
        node = cmds.blendShape(shapes, target)[0]
        filter_name = (name + node[0].upper() + node[1:])
        #--- rename the blendShape deformer
        node = self.__rename_node(mod = mod,
                                  side = side,
                                  name = filter_name,
                                  suffix = suffix,
                                  obj = node)
        #--- take care of the node's settings
        #--- envelope
        cmds.setAttr(node + '.envelope', envelope)
        #--- change the shape weight value
        if isinstance(shapeAttr, list):
            for s in shapeAttr:
                cmds.setAttr(node + '.' + s, shapeValue)
        else:
            cmds.setAttr(node + '.' + shapeAttr, shapeValue)            

        #--- show or hide transform
        if not show:
            if isinstance(target, list):
                for t in target:
                    cmds.setAttr(t + '.v', 0)
            else:
                cmds.setAttr(target + '.v', 0)
        #--- lock specified attributes
        if lockAttr:
            if node:
                cmds.setAttr(node + '.' + lockAttr, lock = True)
        #--- set isHistoricalInteresting attribute
        if not ihi:
            cmds.setAttr(node + '.ihi', 0)
        #--- return node
        return node
    #end def blendShape()

    def cluster(self,
                 character = None,
                 mod = None,
                 side = None,
                 name = None,
                 suffix = None,
                 geometry = None,
                 origin = [0,0,0],
                 weightObj = None,
                 weightValue = 1,
                 parent = None,
                 show = True,
                 lockAttr = None,
                 ihi = True):
        #--- this method creates a cluster deformer
        #--- select the specified geometry
        cmds.select(geometry)        
        #--- create a cluster deformer
        node = cmds.cluster()
        filter_name = (name + node[0].split('Handle')[0][0].upper() +
                       node[0].split('Handle')[0][1:])
        #--- rename the cluster deformer
        node = self.__rename_node(mod = mod,
                                  side = side,
                                  name = filter_name,
                                  suffix = suffix,
                                  obj = node)
        #--- get the cluster deform node
        node.append(cmds.listConnections(node[0])[0])
        #--- create a group on top and parent the deformer under the group
        node_grp = cmds.createNode('transform')
        cmds.parent(node[0], node_grp)
        #--- rename the node group
        node_grp = self.__rename_node(mod = mod,
                                      side = side,
                                      name = filter_name,
                                      suffix = 'GRP',
                                      obj = node_grp)[0]        
        #--- take care of the node's settings
        #--- origin
        ori_x= cmds.getAttr(node[1] + '.originX')
        ori_y= cmds.getAttr(node[1] + '.originY')
        ori_z= cmds.getAttr(node[1] + '.originZ')
        new_origin = [ori_x + origin[0], ori_y + origin[1], ori_z + origin[2]]
        cmds.setAttr(node[1] + '.origin', 
                     new_origin[0], 
                     new_origin[1], 
                     new_origin[2])
        cmds.xform(node[0], pivots = new_origin, worldSpace = True)
        #--- reposition the pivot of the group to the location of the cluster
        cmds.xform(node_grp, pivots = new_origin, worldSpace = True)        
        #--- weightValue
        if weightObj:
            if isinstance(weightObj, list):
                if isinstance(weightValue, list):
                    for obj, val in zip(weightObj, weightValue):
                        cmds.percent(node[-1], obj, value = val)
                else:
                    for obj in weightObj:
                        cmds.percent(node[-1], obj, value = weightValue)
            else:
                cmds.percent(node[-1], weightObj, value = weightValue)

        #--- parent the group under the specified parent
        if parent:
            if not isinstance(parent, list):
                cmds.parent(node_grp, parent)
            else:
                raise Exception("Specified parent: " + 
                                parent + 'is not a valid')
        #--- show or hide transform
        if not show:
            if isinstance(target, list):
                for t in target:
                    cmds.setAttr(t + '.v', 0)
            else:
                cmds.setAttr(target + '.v', 0)
        #--- lock specified attributes
        if lockAttr:
            if node:
                cmds.setAttr(node + '.' + lockAttr, lock = True)
        #--- set isHistoricalInteresting attribute
        if not ihi:
            cmds.setAttr(node + '.ihi', 0)
        #--- return node
        return node
    #end def cluster()

    def flare(self,
              character = None,
              mod = None,
              side = None,
              name = None,
              suffix = None,
              geometry = None,
              position = [0,0,0],
              rotation = [0,0,0],
              envelope = 1,
              startFlareX = 1,
              startFlareZ = 1,
              endFlareX = 1,
              endFlareZ = 1,
              curve = 0,
              lowBound = -1,
              highBound = 1,
              parent = None,
              show = True,
              lockAttr = None,
              ihi = True):
        #--- this method creates a flare deformer
        #--- select the specified geometry
        cmds.select(geometry)
        #--- create a flare deformer
        node = cmds.nonLinear(type = 'flare')
        filter_name = (name + node[0].split('Handle')[0][0].upper() +
                       node[0].split('Handle')[0][1:])
        #--- rename the flare deformer
        node = self.__rename_node(mod = mod,
                                  side = side,
                                  name = filter_name,
                                  suffix = suffix,
                                  obj = node)
        #--- create a group on top and parent the deformer under the group
        node_grp = cmds.createNode('transform', parent = node[0])
        cmds.parent(node_grp, world = True)
        cmds.parent(node[0], node_grp)
        #--- rename the node group
        node_grp = self.__rename_node(mod = mod,
                                      side = side,
                                      name = filter_name,
                                      suffix = 'GRP',
                                      obj = node_grp)
        #--- reposition the transform of the deformer locally
        cmds.xform(node[0], translation = position, worldSpace = False)
        cmds.xform(node[0], rotation = rotation, worldSpace = False)
        #--- take care of the node's settings
        #--- envelope
        cmds.setAttr(node[-1] + '.envelope', envelope)
        #--- startFlareX
        cmds.setAttr(node[-1] + '.startFlareX', startFlareX)
        #--- startFlareZ
        cmds.setAttr(node[-1] + '.startFlareZ', startFlareZ)
        #--- endFlareX
        cmds.setAttr(node[-1] + '.endFlareX', endFlareX)
        #--- endFlareZ
        cmds.setAttr(node[-1] + '.endFlareZ', endFlareZ)
        #--- curve
        cmds.setAttr(node[-1] + '.curve', curve)
        #--- lowBound
        cmds.setAttr(node[-1] + '.lowBound', lowBound)
        #--- highBound
        cmds.setAttr(node[-1] + '.highBound', highBound)
        #--- parent the group under the specified parent
        if parent:
            if not isinstance(parent, list):
                cmds.parent(node_grp, parent)
            else:
                raise Exception("Specified parent: " +
                                parent + 'is not a valid')
        #--- show or hide transform
        if not show:
            cmds.setAttr(node[0] + '.v', 0)
        #--- lock specified attributes
        if lockAttr:
            if node[-1]:
                cmds.setAttr(node[-1] + '.' + lockAttr, lock = True)
        #--- set isHistoricalInteresting attribute
        if not ihi:
            for n in node:
                cmds.setAttr(n + '.ihi', 0)
        #--- return node
        return node
    #end def flare()

    def jiggle(self):
        #--- this method creates a jiggle deformer
        pass
    #end def jiggle()

    def lattice(self,
                 character = None,
                 mod = None,
                 side = None,
                 name = None,
                 suffix = None,
                 geometry = None,
                 position = [0,0,0],
                 rotation = [0,0,0],
                 envelope = 1,
                 divisions = [2,5,2],
                 objectCentered = True,
                 localInfluences = [2,2,2],
                 outsideLattice = 'inside',
                 outsideFalloffDist = 1,
                 resolution = 'full',
                 partialResolution = 0.01,
                 freezeGeometry = False,
                 parent = None,
                 show = True,
                 lockAttr = None,
                 ihi = True):
        #--- this method creates a lattice deformer
        #--- select the specified geometry
        cmds.select(geometry)
        #--- create a lattice deformer
        node = cmds.lattice(divisions = divisions,
                            objectCentered = objectCentered,
                            ldivisions = localInfluences)
        #--- filter the name
        filter_lat = name + 'Lattice' + node[0].split('ffd')[-1]
        filter_bas = name + 'Base' + node[0].split('ffd')[-1]
        #--- create a group on top and parent the deformer under the group
        node_grp = cmds.createNode('transform')
        #--- rename the node group
        node_grp = self.__rename_node(mod = mod,
                                      side = side,
                                      name = filter_lat,
                                      suffix = 'GRP',
                                      obj = node_grp)
        #--- rename the lattice deformer
        lat = self.__rename_node(mod = mod,
                                 side = side,
                                 name = filter_lat,
                                 suffix = suffix,
                                 obj = node)
        #--- rename the base deformer
        base = self.__rename_node(mod = mod,
                                  side = side,
                                  name = filter_bas,
                                  suffix = suffix,
                                  obj = node[-1])
        cmds.parent(node_grp, lat[0])
        cmds.parent(node_grp, world = True)
        cmds.parent(lat[0], base[0], node_grp)
        node = lat
        #--- reposition the transform of the deformer locally
        cmds.xform(node_grp, translation = position, worldSpace = False)
        cmds.xform(node_grp, rotation = rotation, worldSpace = False)
        #--- take care of the node's settings
        #--- envelope
        cmds.setAttr(node[-1] + '.envelope', envelope)
        #--- outsideLattice
        if outsideLattice == 'inside':
            cmds.setAttr(node[-1] + '.outsideLattice', 0)
        elif outsideLattice == 'all':
            cmds.setAttr(node[-1] + '.outsideLattice', 1)
        elif outsideLattice == 'falloff':
            cmds.setAttr(node[-1] + '.outsideLattice', 2)
        #--- outsideFalloffDist
        if outsideLattice == 'falloff':
            cmds.setAttr(node[-1] + '.outsideFalloffDist', outsideFalloffDist)
        #--- resolution
        if resolution == 'full':
            cmds.setAttr(node[-1] + '.usePartialResolution', 0)
        elif resolution == 'partial':
            cmds.setAttr(node[-1] + '.usePartialResolution', 1)
        #--- partialResolution
        if resolution == 'partial':
            cmds.setAttr(node[-1] + '.partialResolution', partialResolution)
        #--- freezeGeometry
        cmds.setAttr(node[-1] + '.freezeGeometry', freezeGeometry)
        #--- parent the group under the specified parent
        if parent:
            if not isinstance(parent, list):
                cmds.parent(node_grp, parent)
            else:
                raise Exception("Specified parent: " + parent + 'is not a valid')
        #--- show or hide transform
        if not show:
            cmds.setAttr(node_grp + '.v', 0)
        #--- lock specified attributes
        if lockAttr:
            if node[-1]:
                cmds.setAttr(node[-1] + '.' + lockAttr, lock = True)
        #--- set isHistoricalInteresting attribute
        if not ihi:
            for n in node:
                cmds.setAttr(n + '.ihi', 0)
            for b in base:
                cmds.setAttr(b + '.ihi', 0)
        node.insert(-1, base[0])
        #--- return node
        return node
    #end def lattice()

    def sculpt(self,
               character = None,
               mod = None,
               side = None,
               name = None,
               suffix = None,
               geometry = None,
               position = [0,0,0],
               rotation = [0,0,0],
               envelope = 1,
               mode = 'flip',
               insideMode = 'ring',
               maxDisplacement = 0.1,
               dropoffType = 'linear',
               dropoffDistance = 1,
               groupWithLocator = 0,
               objectCentered = 0,
               radius = 1,
               parent = None,
               show = True,
               lockAttr = None,
               ihi = True):
        #--- this method creates a sculpt deformer
        #--- select the specified geometry
        cmds.select(geometry)
        #--- create a sculpt deformer
        node = cmds.sculpt(mode = mode,
                           insideMode = insideMode,
                           maxDisplacement = maxDisplacement,
                           dropoffType = dropoffType,
                           dropoffDistance = dropoffDistance,
                           groupWithLocator = groupWithLocator,
                           objectCentered = objectCentered)
        #--- filter the individual name
        filter_name = node[0]
        #--- create a group on top and parent the deformer under the group
        node_grp = cmds.createNode('transform')
        #--- rename the node group
        node_grp = self.__rename_node(mod = mod,
                                      side = side,
                                      name = filter_name,
                                      suffix = 'GRP',
                                      obj = node_grp)[0]
        #--- rename the sculpt deformer
        node = self.__rename_node(mod = mod,
                                  side = side,
                                  name = filter_name,
                                  suffix = suffix,
                                  obj = node)
        cmds.parent(node_grp, node[0])
        cmds.parent(node_grp, world = True)
        cmds.parent(node[0], node_grp)
        #--- reposition the transform of the deformer locally
        cmds.xform(node[0], translation = position, worldSpace = False)
        cmds.xform(node[0], rotation = rotation, worldSpace = False)
        #--- take care of the node's settings
        #--- envelope
        cmds.setAttr(node[-1] + '.envelope', envelope)
        #--- radius
        cmds.setAttr(node[1] + '.radius', radius)
        #--- parent the group under the specified parent
        if parent:
            if not isinstance(parent, list):
                cmds.parent(node_grp, parent)
            else:
                raise Exception("Specified parent: " +
                                parent + 'is not a valid')
        #--- show or hide transform
        if not show:
            cmds.setAttr(node[0] + '.v', 0)
        #--- lock specified attributes
        if lockAttr:
            if node[-1]:
                cmds.setAttr(node[-1] + '.' + lockAttr, lock = True)
        #--- set isHistoricalInteresting attribute
        if not ihi:
            for n in node:
                cmds.setAttr(n + '.ihi', 0)
        #--- return node
        node.append(node_grp)
        return node
    #end def sculpt()

    def sine(self,
             character = None,
             mod = None,
             side = None,
             name = None,
             suffix = None,
             geometry = None,
             position = [0,0,0],
             rotation = [0,0,0],
             envelope = 1,
             amplitude = 0,
             wavelength = 2,
             offset = 0,
             dropoff = 0,
             lowBound = -1,
             highBound = 1,
             parent = None,
             show = True,
             lockAttr = None,
             ihi = True):
        #--- this method creates a sine deformer
        #--- select the specified geometry
        cmds.select(geometry)
        #--- create a sine deformer
        node = cmds.nonLinear(type = 'sine')
        #--- filter the individual name
        filter_name = (name + node[0].split('Handle')[0][0].upper() +
                       node[0].split('Handle')[0][1:])
        #--- rename the sine deformer
        node = self.__rename_node(mod = mod,
                                  side = side,
                                  name = filter_name,
                                  suffix = suffix,
                                  obj = node)
        #--- create a group on top and parent the deformer under the group
        node_grp = cmds.createNode('transform', parent = node[0])
        cmds.parent(node_grp, world = True)
        cmds.parent(node[0], node_grp)
        #--- rename the node group
        node_grp = self.__rename_node(mod = mod,
                                      side = side,
                                      name = filter_name,
                                      suffix = 'GRP',
                                      obj = node_grp)
        #--- reposition the transform of the deformer locally
        cmds.xform(node[0], translation = position, worldSpace = False)
        cmds.xform(node[0], rotation = rotation, worldSpace = False)
        #--- take care of the node's settings
        #--- envelope
        cmds.setAttr(node[-1] + '.envelope', envelope)
        #--- amplitude
        cmds.setAttr(node[-1] + '.amplitude', amplitude)
        #--- wavelength
        cmds.setAttr(node[-1] + '.wavelength', wavelength)
        #--- offset
        cmds.setAttr(node[-1] + '.offset', offset)
        #--- dropoff
        cmds.setAttr(node[-1] + '.dropoff', dropoff)
        #--- lowBound
        cmds.setAttr(node[-1] + '.lowBound', lowBound)
        #--- highBound
        cmds.setAttr(node[-1] + '.highBound', highBound)
        #--- parent the group under the specified parent
        if parent:
            if not isinstance(parent, list):
                cmds.parent(node_grp, parent)
            else:
                raise Exception("Specified parent: " +
                                parent + 'is not a valid')
        #--- show or hide transform
        if not show:
            cmds.setAttr(node[0] + '.v', 0)
        #--- lock specified attributes
        if lockAttr:
            if node[-1]:
                cmds.setAttr(node[-1] + '.' + lockAttr, lock = True)
        #--- set isHistoricalInteresting attribute
        if not ihi:
            for n in node:
                cmds.setAttr(n + '.ihi', 0)
        #--- return node
        return node
    #end def sine()

    def softMod(self):
        #--- this method creates a softMod deformer
        pass
    #end def softMod()

    def squash(self,
               character = None,
               mod = None,
               side = None,
               name = None,
               suffix = None,
               geometry = None,
               position = [0,0,0],
               rotation = [0,0,0],
               envelope = 1,
               factor = 0,
               expand = 1,
               maxExpandPos = 0.5,
               startSmoothness = 0,
               endSmoothness = 0,
               lowBound = -1,
               highBound = 1,
               parent = None,
               show = True,
               lockAttr = None,
               ihi = True):
        #--- this method creates a squash deformer
        #--- select the specified geometry
        cmds.select(geometry)
        #--- create a squash deformer
        node = cmds.nonLinear(type = 'squash')
        #--- filter the individual name
        filter_name = (name + node[0].split('Handle')[0][0].upper() +
                       node[0].split('Handle')[0][1:])
        #--- rename the squash deformer
        node = self.__rename_node(mod = mod,
                                  side = side,
                                  name = filter_name,
                                  suffix = suffix,
                                  obj = node)
        #--- create a group on top and parent the deformer under the group
        node_grp = cmds.createNode('transform', parent = node[0])
        cmds.parent(node_grp, world = True)
        cmds.parent(node[0], node_grp)
        #--- rename the node group
        node_grp = self.__rename_node(mod = mod,
                                      side = side,
                                      name = filter_name,
                                      suffix = 'GRP',
                                      obj = node_grp)
        #--- reposition the transform of the deformer locally
        cmds.xform(node[0], translation = position, worldSpace = False)
        cmds.xform(node[0], rotation = rotation, worldSpace = False)
        #--- take care of the node's settings
        #--- envelope
        cmds.setAttr(node[-1] + '.envelope', envelope)
        #--- factor
        cmds.setAttr(node[-1] + '.factor', factor)
        #--- expand
        cmds.setAttr(node[-1] + '.expand', expand)
        #--- maxExpandPos
        cmds.setAttr(node[-1] + '.maxExpandPos', maxExpandPos)
        #--- startSmoothness
        cmds.setAttr(node[-1] + '.startSmoothness', startSmoothness)
        #--- endSmoothness
        cmds.setAttr(node[-1] + '.endSmoothness', endSmoothness)
        #--- lowBound
        cmds.setAttr(node[-1] + '.lowBound', lowBound)
        #--- highBound
        cmds.setAttr(node[-1] + '.highBound', highBound)
        #--- parent the group under the specified parent
        if parent:
            if not isinstance(parent, list):
                cmds.parent(node_grp, parent)
            else:
                raise Exception("Specified parent: " +
                                parent + 'is not a valid')
        #--- show or hide transform
        if not show:
            cmds.setAttr(node[0] + '.v', 0)
        #--- lock specified attributes
        if lockAttr:
            if node[-1]:
                cmds.setAttr(node[-1] + '.' + lockAttr, lock = True)
        #--- set isHistoricalInteresting attribute
        if not ihi:
            for n in node:
                cmds.setAttr(n + '.ihi', 0)
        #--- return node
        return node
    #end def squash()

    def twist(self,
             character = None,
             mod = None,
             side = None,
             name = None,
             suffix = None,
             geometry = None,
             position = [0,0,0],
             rotation = [0,0,0],
             envelope = 1,
             startAngle = 0,
             endAngle = 0,
             lowBound = -1,
             highBound = 1,
             parent = None,
             show = True,
             lockAttr = None,
             ihi = True):
        #--- this method creates a twist deformer
        #--- select the specified geometry
        cmds.select(geometry)
        #--- create a twist deformer
        node = cmds.nonLinear(type = 'twist')
        #--- filter the individual name
        filter_name = (name + node[0].split('Handle')[0][0].upper() +
                       node[0].split('Handle')[0][1:])
        #--- rename the twist deformer
        node = self.__rename_node(mod = mod,
                                  side = side,
                                  name = filter_name,
                                  suffix = suffix,
                                  obj = node)
        #--- create a group on top and parent the deformer under the group
        node_grp = cmds.createNode('transform', parent = node[0])
        cmds.parent(node_grp, world = True)
        cmds.parent(node[0], node_grp)
        #--- rename the node group
        node_grp = self.__rename_node(mod = mod,
                                      side = side,
                                      name = filter_name,
                                      suffix = 'GRP',
                                      obj = node_grp)[0]
        #--- reposition the transform of the deformer locally
        cmds.xform(node[0], translation = position, worldSpace = False)
        cmds.xform(node[0], rotation = rotation, worldSpace = False)
        #--- take care of the node's settings
        #--- envelope
        cmds.setAttr(node[-1] + '.envelope', envelope)
        #--- startAngle
        cmds.setAttr(node[-1] + '.startAngle', startAngle)
        #--- endAngle
        cmds.setAttr(node[-1] + '.endAngle', endAngle)
        #--- lowBound
        cmds.setAttr(node[-1] + '.lowBound', lowBound)
        #--- highBound
        cmds.setAttr(node[-1] + '.highBound', highBound)
        #--- parent the group under the specified parent
        if parent:
            if not isinstance(parent, list):
                cmds.parent(node_grp, parent)
            else:
                raise Exception("Specified parent: " +
                                parent + 'is not a valid')
        #--- show or hide transform
        if not show:
            cmds.setAttr(node[0] + '.v', 0)
        #--- lock specified attributes
        if lockAttr:
            if node[-1]:
                cmds.setAttr(node[-1] + '.' + lockAttr, lock = True)
        #--- set isHistoricalInteresting attribute
        if not ihi:
            for n in node:
                cmds.setAttr(n + '.ihi', 0)
        #--- return node
        return node
    #end def twist()

    def wave(self,
             character = None,
             mod = None,
             side = None,
             name = None,
             suffix = None,
             geometry = None,
             position = [0,0,0],
             rotation = [0,0,0],
             envelope = 1,
             amplitude = 0,
             wavelength = 1,
             offset = 0,
             dropoff = 0,
             dropoffPosition = 0,
             minRadius = 0,
             maxRadius = 1,
             parent = None,
             show = True,
             lockAttr = None,
             ihi = True):
        #--- this method creates a wave deformer
        #--- select the specified geometry
        cmds.select(geometry)
        #--- create a wave deformer
        node = cmds.nonLinear(type = 'wave')
        #--- filter the individual name
        filter_name = (name + node[0].split('Handle')[0][0].upper() +
                       node[0].split('Handle')[0][1:])
        #--- rename the wave deformer
        node = self.__rename_node(mod = mod,
                                  side = side,
                                  name = filter_name,
                                  suffix = suffix,
                                  obj = node)
        #--- create a group on top and parent the deformer under the group
        node_grp = cmds.createNode('transform', parent = node[0])
        cmds.parent(node_grp, world = True)
        cmds.parent(node[0], node_grp)
        #--- rename the node group
        node_grp = self.__rename_node(mod = mod,
                                      side = side,
                                      name = filter_name,
                                      suffix = 'GRP',
                                      obj = node_grp)
        #--- reposition the transform of the deformer locally
        cmds.xform(node[0], translation = position, worldSpace = False)
        cmds.xform(node[0], rotation = rotation, worldSpace = False)
        #--- take care of the node's settings
        #--- envelope
        cmds.setAttr(node[-1] + '.envelope', envelope)
        #--- amplitude
        cmds.setAttr(node[-1] + '.amplitude', amplitude)
        #--- wavelength
        cmds.setAttr(node[-1] + '.wavelength', wavelength)
        #--- offset
        cmds.setAttr(node[-1] + '.offset', offset)
        #--- dropoff
        cmds.setAttr(node[-1] + '.dropoff', dropoff)
        #--- dropoffPosition
        cmds.setAttr(node[-1] + '.dropoffPosition', dropoffPosition)
        #--- minRadius
        cmds.setAttr(node[-1] + '.minRadius', minRadius)
        #--- maxRadius
        cmds.setAttr(node[-1] + '.maxRadius', maxRadius)
        #--- parent the group under the specified parent
        if parent:
            if not isinstance(parent, list):
                cmds.parent(node_grp, parent)
            else:
                raise Exception("Specified parent: " +
                                parent + 'is not a valid')
        #--- show or hide transform
        if not show:
            cmds.setAttr(node[0] + '.v', 0)
        #--- lock specified attributes
        if lockAttr:
            if node[-1]:
                cmds.setAttr(node[-1] + '.' + lockAttr, lock = True)
        #--- set isHistoricalInteresting attribute
        if not ihi:
            for n in node:
                cmds.setAttr(n + '.ihi', 0)
        #--- return node
        return node
    #end def wave()

    def wire(self,
             character = None,
             mod = None,
             side = None,
             name = None,
             suffix = None,
             wire = None,
             geometry = None,
             position = [0,0,0],
             rotation = [0,0,0],
             envelope = 1,
             crossingEffect = 0,
             tension = 1,
             localInfluence = 0,
             wireRotation = 1,
             dropoffDistance = 1,
             wireScale = 1,
             parent = None,
             show = True,
             lockAttr = None,
             ihi = True):
        #--- this method creates a wire deformer
        node = []
        if wire:
            if geometry:
                #--- create a wire deformer
                node = cmds.wire(geometry, wire = wire, groupWithBase = False)
                base = cmds.ls(node[-1] + 'BaseWire')
        #--- filter the individual name
        filter_name = (name + node[0][0].upper() + node[0][1:])
        #--- rename the wire deformer
        node = self.__rename_node(mod = mod,
                                  side = side,
                                  name = filter_name,
                                  suffix = suffix,
                                  obj = node)
        #--- rename the baseWire curve
        base = self.__rename_node(mod = mod,
                                  side = side,
                                  name = filter_name + 'BaseWire',
                                  suffix = suffix,
                                  obj = base)
        #--- create a group on top and parent the deformer under the group
        node_grp = cmds.createNode('transform', parent = node[0])
        cmds.parent(node_grp, world = True)
        cmds.parent(node[0], base[0], node_grp)
        #--- rename the node group
        node_grp = self.__rename_node(mod = mod,
                                      side = side,
                                      name = filter_name,
                                      suffix = 'GRP',
                                      obj = node_grp)[0]
        #--- reposition the transform of the deformer locally
        cmds.xform(node[0], translation = position, worldSpace = False)
        cmds.xform(node[0], rotation = rotation, worldSpace = False)
        #--- take care of the node's settings
        #--- envelope
        cmds.setAttr(node[-1] + '.envelope', envelope)
        #--- crossingEffect
        cmds.setAttr(node[-1] + '.crossingEffect', crossingEffect)
        #--- tension
        cmds.setAttr(node[-1] + '.tension', tension)
        #--- localInfluence
        cmds.setAttr(node[-1] + '.localInfluence', localInfluence)
        #--- wireRotation
        cmds.setAttr(node[-1] + '.rotation', wireRotation)
        #--- dropoffDistance
        cmds.setAttr(node[-1] + '.dropoffDistance[0]', dropoffDistance)
        #--- wireScale
        cmds.setAttr(node[-1] + '.scale[0]', wireScale)
        #--- parent the group under the specified parent
        if parent:
            if not isinstance(parent, list):
                cmds.parent(node_grp, parent)
            else:
                raise Exception("Specified parent: " +
                                parent + 'is not a valid')
        #--- show or hide transform
        if not show:
            cmds.setAttr(node[0] + '.v', 0)
        #--- lock specified attributes
        if lockAttr:
            if node[-1]:
                cmds.setAttr(node[-1] + '.' + lockAttr, lock = True)
        #--- set isHistoricalInteresting attribute
        if not ihi:
            for n in node:
                cmds.setAttr(n + '.ihi', 0)
        #--- add the base wire to the node list
        node.append(base[0])
        #--- return node
        return node
    #end def wire()

    def wrap(self):
        #--- this method creates a wrap deformer
        pass
    #end def wrap()

    def __rename_node(self,
                        mod = None,
                        side = None,
                        name = None,
                        suffix = None,
                        obj = None):
        #--- this method returns the final name of the node
        #--- check which one of the given obj is the transform node
        trn = []
        non = []
        if isinstance(obj, list):
            for i in obj:
                if cmds.nodeType(i) == 'transform':
                    trn.append(i)
                else:
                    if not cmds.nodeType(i) == 'shape':
                        non.append(i)
        else:
            if cmds.nodeType(obj) == 'transform':
                trn.append(obj)
            else:
                if not cmds.nodeType(obj) == 'shape':
                    non.append(obj)
        if trn:
            obj = trn[0]
        if non:
            non = non[0]
        obj_name = None
        #--- get the curve name based on the given specifications
        if mod:
            if side:
                if name:
                    if suffix:
                        #--- side_modName_suffix
                        obj_name = (side + '_' + mod + name[0].upper() +
                                    name[1:] + '_' + suffix)
                    else:
                        #--- side_modName
                        obj_name = (side + '_' + mod + name[0].upper() +
                                    name[1:])
                else:
                    if suffix:
                        #--- side_modCrv_suffix
                        obj_name = (side + '_' + mod + obj[0].upper() +
                                    obj[1:] + '_' + suffix)
                    else:
                        #--- side_modCrv
                        obj_name = (side + '_' + mod + obj[0].upper() +
                                    obj[1:])
            else:
                if name:
                    if suffix:
                        #--- modName_suffix
                        obj_name = (mod + name[0].upper() +
                                    name[1:] + '_' + suffix)
                    else:
                        #--- modName
                        obj_name = (mod + name[0].upper() + name[1:])
                else:
                    #--- modCrv
                    obj_name = (mod + obj[0].upper() + obj[1:])
        else:
            if side:
                if name:
                    if suffix:
                        #--- side_name_suffix
                        obj_name = (side + '_' + name + '_' + suffix)
                    else:
                        #--- side_name
                        obj_name = (side + '_' + name)
                else:
                    if suffix:
                        #--- side_obj_suffix
                        obj_name = (side + '_' + obj + '_' + suffix)
                    else:
                        #--- side_obj
                        obj_name = (side + '_' + obj)
            else:
                if name:
                    if suffix:
                        #--- name_suffix
                        obj_name = (name + '_' + suffix)
                    else:
                        #--- name
                        obj_name = (name)
                else:
                    #--- obj
                    obj_name = (obj)
        #--- rename the obj
        transform = cmds.rename(obj, obj_name)
        shape = []
        if cmds.listRelatives(transform, children = True):
            shape = cmds.listRelatives(transform,
                                       allDescendents = True,
                                       type = 'shape')[0]
        #--- rename the nonTransform/nonShape obj
        result = []
        if non:
            if cmds.objExists(non):
                non = cmds.rename(non, obj_name + non[0].upper() + non[1:])
                result = [transform, shape, non]
            else:
                if shape:
                    result = [transform, shape]
                else:
                    result = transform
        else:
            result = [transform, shape]
        return result
    #end def __rename_node()
#end class Deformer()

#cmds.curve(degree = 3, point = [[5,0,4], [3,0,2], [-5,0,3], [6,0,-4]])
#dfm = Deformer()
#bnd = dfm.wire(character = "ACHILLES",
#               mod = 'arm',
#               side = 'L',
#               name = 'shoulder',
#               suffix = 'DEF',
#               wire = 'curve1',
#               geometry = 'bla')