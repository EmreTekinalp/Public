'''
Created on May 13, 2015

@author: Emre
'''


from pymel import core as pm
from maya import OpenMaya


class MeshIntersector(object):
    """
    Return the faceindex value at the intersecting point of a target mesh.
    """

    def __init__(self, mesh, intersectors):
        """
        @param mesh(string): The target mesh
        @param intersectors(list): Elements of intersecting objects
        """

        # args
        self.mesh = pm.PyNode(mesh)
        self.intersectors = [pm.PyNode(item) for item in intersectors]

        # vars

        # methods
        self._check_parameters()
        self._setup_mesh()
    # END def __init__

    def _check_parameters(self):
        """
        Check the parameters for validation.
        """

        if self.mesh.nodeType() == 'transform':
            if not self.mesh.getShape().nodeType() == 'mesh':
                raise ValueError('mesh: Specified node is not a mesh!')
            # END if
        # END if
        elif not self.mesh.nodeType() == 'mesh':
            raise ValueError('mesh: Specified node is not a mesh!')
        # END elif
    # END def _check_parameters

    def _setup_mesh(self):
        """
        Setup the mesh.
        """

        pavertices = OpenMaya.MPointArray()
        fnMesh = OpenMaya.MFnMesh(self._mobject(self.mesh.getShape()))
        fnMesh.getPoints(pavertices)
        for pt in range(pavertices.length()):
            print pavertices[pt], self.mesh.getMatrix()
    # END def _setup_mesh

    def _mobject(self, node):
        """
        Helper function to return a mobject of a given node.

        @param node(string): The node whose mobject we will return.
        """

        mselection = OpenMaya.MSelectionList()
        mselection.add(node)
        mobject = OpenMaya.MObject()
        mselection.getDependNode(0, mobject)
        return mobject
    # END def _mobject
# END class MeshIntersector

MeshIntersector('target', ['intersector1'])
