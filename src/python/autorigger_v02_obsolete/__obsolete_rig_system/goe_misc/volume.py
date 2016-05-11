'''
Created on May 12, 2015

@author: Emre
'''

from pymel import core as pm
from pymel.core.general import nodeType


class VolumePushCollider(object):
    """
    Create a volume detection based push collider along a given curve by using
    a wire deformer tool and a nurbsSurface. We are using pymel.
    """

    def __init__(self, side, name, curve, surface, mesh, parent, debug=False):
        """
        @param side(string): Valid is 'C', 'L', 'R'
        @param name(string): Descriptive part of the nodes
        @param curve(string): Curve used for wireTool deformer
        @param surface(string): NurbsSurface used to create follicle setup
        @param mesh(string): PolyMesh used to wire deform
        @param parent(string): Parent node of the rig setup
        @param debug(bool): Work in debug mode and unlock all attributes
        """

        # args
        self.side = side
        self.name = name
        self.curve = curve
        self.surface = surface
        self.mesh = mesh
        self.parent = parent
        self.debug = debug

        # vars
        self.rig_grp = 'RIG_GRP'
        self.mod_grp = '%s_%s_M' % (side, name)
        self.fol_grp = '%s_%sFollicles_GRP' % (side, name)
        self.vol_grp = '%s_%sVolumes_GRP' % (side, name)
        self.wire_grp = '%s_%sWire_GRP' % (side, name)
        self.collider = '%s_%sCollider_LOC' % (side, name)
        self.wire = '%s_%s_WRE' % (side, name)
        self.wirebase = '%s_%sBase_WRE' % (side, name)
        self.volumes = list()
        self.param = dict()
        self.follicle = dict()
        self.pointmatrixmult = list()
        self.reverse = list()

        # methods
        self._check_parameter()
        self._create_groups()
        self._add_attributes()
#         self._find_closest_parameter()
#         self._create_follicles()
#         self._create_volume_setup()
#         self._setup_wire_deformer()
#         self._setup_parent()
#         self._setup_display()
#         self._clean_up()
    # END def __init__

    def _check_parameter(self):
        """
        Check the given parameters for validation.
        """

        # check type errors
        self.__check_type(self.side, str)
        self.__check_type(self.name, str)
        self.__check_type(self.curve, str)
        self.__check_type(self.surface, str)

        # side
        if not (self.side == 'C' or self.side == 'L' or self.side == 'R'):
            raise ValueError('Please specify "C", "L" or "R"!')
        # END if

        # check nodetypes of curve, surface and mesh
        self.__check_nodetype(self.curve, 'nurbsCurve')
        self.__check_nodetype(self.surface, 'nurbsSurface')
        self.__check_nodetype(self.mesh, 'mesh')

        # parent
        parent = pm.PyNode(self.parent)
        assert parent.objExists(), 'Object does not exist %s' % parent
        if not parent.nodeType() == 'transform':
            raise ValueError('Please specify a transform for parent!')
        # END if
    # END def _check_parameter

    def _create_groups(self):
        """
        Create and setup proper groups for the rig setup.
        """

        trn = 'transform'
        if not pm.objExists(self.rig_grp):
            self.rig_grp = pm.createNode(trn, n=self.rig_grp)
        # END if
        if not pm.objExists(self.mod_grp):
            self.mod_grp = pm.createNode(trn, n=self.mod_grp, p=self.rig_grp)
        # END if
        if not pm.objExists(self.fol_grp):
            self.fol_grp = pm.createNode(trn, n=self.fol_grp, p=self.mod_grp)
        # END if
        if not pm.objExists(self.vol_grp):
            self.vol_grp = pm.createNode(trn, n=self.vol_grp, p=self.mod_grp)
        # END if
        if not pm.objExists(self.wire_grp):
            self.wire_grp = pm.createNode(trn, n=self.wire_grp, p=self.mod_grp)
        # END if
    # END def _create_groups

    def _add_attributes(self):
        """
        Add attributes to nodes.
        """

        self.__attr(self.mod_grp, 'showHistory')
        self.__attr(self.mod_grp, 'showFollicles')
        self.__attr(self.mod_grp, 'showVolumes')
        self.__attr(self.mod_grp, 'showCurve')
        self.__attr(self.mod_grp, 'showSurface')
        self.__attr(self.mod_grp, 'showCollider')
    # END def _add_attributes

    def __check_type(self, param, ptype):
        """
        Helper function to check the type of the given parameter

        @param param(string): Parameter to check the type of
        @param ptype(string): Python valid types
        """

        if not isinstance(param, ptype):
            raise TypeError('Use %s as inputType for %s!' % (ptype, param))
        # END if
    # END def __check_type

    def __check_nodetype(self, node, nodetype):
        """
        Helper function to check the node type of a shape.

        @param node(string): Object whose nodetype will be checked
        @param nodetype(string): Nodetype to check the object for
        """

        obj = pm.PyNode(node)
        assert obj.objExists(), 'Object does not exist %s' % obj
        if obj.nodeType() == 'transform':
            obj = obj.getShape()
        # END if
        if not obj.nodeType() == nodetype:
            raise ValueError('Please specify a %s for curve!' % nodetype)
        # END if
    # END def __check_nodetype

    def __attr(self, node, attr):
        """
        Helper function to create a short attribute which is displayable.

        @param node(string): The pyNode object we add an attribute to
        @param attr(string): Attribute we will add
        """

        if not node.hasAttr(attr):
            node.addAttr(attr, at='short', min=0, max=1, dv=self.debug)
            node.setAttr(attr, e=True, cb=True)
        # END if
    # END def __attr
# END class VolumePushCollider

vpc = VolumePushCollider('L', 'shirt', 'curve', 'surface', 'mesh', 'C_cog_CTL')
