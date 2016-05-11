"""
@author: Emre Tekinalp
@date: May 3rd, 2015
@contact: e.tekinalp@icloud.com
@brief: Create a volume push collider rig setup
@requires: volumePushCollider.so and nurbsRivet.so plugin
@version: 1.0.0
"""

from maya import cmds, OpenMaya
import pymel.core as pm
from utility import plugin
reload(plugin)


class VolumePushCollider(object):
    """Create a volume detection based push collider along a given curve by
    using a wire deformer tool and a nurbsSurface.

    @DONE: Create groups and proper hierarchy
    @DONE: Find closestParam of the curve on the nurbsSurface
    @DONE: Create follicles
    @DONE: Get worldMatrix of the curve and multiply it with the curvepoint
    @DONE: Create volume objects at each follicle using implicit spheres
    @DONE: Create collision setup
    @DONE: Create locator collider object flag
    @DONE: Create wireTool setup
    @DONE: 2 collider setup with middle volume merge feature
    @DONE: Debug mode
    @DONE: General cleanup of code
    @DONE: Display setup
    @DONE: Create custom plugins as faster option and set it up
    @DONE: Add volumeOffset and volumeScale attributes on parent and connect
    @DONE: Create additional main controls
    @todo: Create a pymel version
    """
    def __init__(self, side, name, curve, surface, mesh, parent,
                 volumeoffset=[0, 0, 0], volumescale=[1, 1, 1],
                 complexity=0, controlatcv=[], useplugin=False, debug=False):
        """Define and setup global parameters and call methods.

        @param side (string) Valid is 'C', 'L', 'R'
        @param name (string) Descriptive part of the nodes
        @param curve (string) Curve used for wireTool deformer
        @param surface (string) NurbsSurface used to create follicle setup
        @param mesh (string) PolyMesh used to wire deform
        @param parent (string) Parent node of the rig setup
        @param volumeoffset (list) Modify relative position of created volumes
        @param volumescale (list) Modify scale of created volumes
        @param complexity (uint) Define the complexity level of this rig setup
                                  0 = fundamental setup, no extra controls
                                  1 = 0 level + create additional main controls
        @param controlatcv (list) Specify the cv index in a list to create
                                  a control of complexity level 1 at that cv
        @param useplugin (bool) Create the setup using maya nodes or plugins
        @param debug (bool) Work in debug mode and unlock all attributes
        """
        # args
        self.side = side
        self.name = name
        self.curve = curve
        self.surface = surface
        self.mesh = mesh
        self.parent = parent
        self.volumeoffset = volumeoffset
        self.volumescale = volumescale
        self.complexity = complexity
        self.controlatcv = controlatcv
        self.useplugin = useplugin
        self.debug = debug

        # vars
        self.rig_grp = 'RIG_GRP'
        self.mod_grp = '%s_%s_M' % (side, name)
        self.fol_grp = '%s_%sFollicles_GRP' % (side, name)
        self.vol_grp = '%s_%sVolumes_GRP' % (side, name)
        self.wire_grp = '%s_%sWire_GRP' % (side, name)
        self.wire = '%s_%s_WRE' % (side, name)
        self.wirebase = '%s_%sBase_WRE' % (side, name)
        self.collider = '%s_%sCollider0_LOC' % (side, name)
        self.colliders = [self.collider]
        self.volumes = list()
        self.param = dict()
        self.follicle = dict()
        self.nrbwire = '%s_%sSurface_WRE' % (side, name)
        self.nrbwirebase = '%s_%sSurfaceBase_WRE' % (side, name)
        self.nrbcurve = '%s_%sSurface_CRV' % (side, name)
        self.pointmatrixmult = list()
        self.reverse = list()
        self.controls = list()
        self.joints = list()
        self.vpc_plug = None
        self.nrb_plug = None

        # methods
        self._check_parameter()
        self._create_groups()
        self._add_attributes()
        self._find_closest_parameter()
        self._create_rivets()
        self._create_volume_setup()
        self._setup_wire_deformer(self.mesh, self.wire, self.wirebase,
                                  self.curve, self.wire_grp, self.complexity)
        if self.complexity:
            self._create_main_controls()
            self._bind_joint_setup()
        # end if
        self._setup_parent()
        self._setup_display()
        self._clean_up()
    # end def __init__

    def add_collider(self):
        """Create a collider object, reconnect to pointMatrixMult nodes."""
        amount = len(self.colliders)
        locname = '%s_%sCollider%s_LOC' % (self.side, self.name, amount)
        loc = self.__locator(locname)
        cmds.parent(loc, self.mod_grp)
        cmds.connectAttr('%s.showCollider' % self.mod_grp, '%s.v' % loc)
        [cmds.setAttr('%s.%s' % (loc, attr), l=True, k=False)
         for attr in ['sx', 'sy', 'sz', 'v']]

        if self.useplugin:
            cmds.connectAttr('%s.worldMatrix' % loc,
                             '%s.inCollider[%s]' % (self.vpc_plug, amount))
            self.colliders.append(loc)
            return loc
        # end if
        dcmname = '%s_%sCollider%s_DCM' % (self.side, self.name, amount)
        dcm = self.__node('decomposeMatrix', dcmname)
        cmds.connectAttr('%s.worldMatrix' % loc, '%s.inputMatrix' % dcm)

        for cv in range(len(self.volumes)):
            self._create_collision_setup(len(self.reverse),
                                         self.volumes[cv], dcm,
                                         self.follicle[cv][1])
            name = '%s_%s%s_PMA' % (self.side, self.name, len(self.reverse))
            pma = self.__node('plusMinusAverage', name)
            cmds.connectAttr('%s.outputX' % self.reverse[cv],
                             '%s.input1D[0]' % pma)
            revlen = len(self.reverse) - 1
            cmds.connectAttr('%s.outputX' % self.reverse[revlen],
                             '%s.input1D[1]' % pma)
            cmds.connectAttr('%s.output1D' % pma,
                             '%s.parameterV' % self.follicle[cv][1], f=True)
            if not self.debug:
                cmds.setAttr('%s.parameterV' % self.follicle[cv][1], l=True)
            # end if
        # end for
        return loc
    # end def add_collider

    def edit_volumes(self, volumes, offset=None, scale=None):
        """This is the edit function for the implicit volume spheres.
        Modify by using the given flags and extend this method if needed.

        @param volumes(list): List of volume elements we want to edit
        @param offset(list): Modify relative position of specified volumes
        @param scale(list): Modify scale of specified volumes
        """
        if offset:
            [cmds.xform(vol, t=offset) for vol in volumes]
        # end if
        if scale:
            [cmds.xform(vol, s=scale) for vol in volumes]
        # end if
    # end def edit_volumes

    def edit_wire(self, rotation=0.0, dropoffdistance=1000.0, scale=1.0):
        """This is the edit function for the wire deformer.
        Modify by using the given flags and extend this method if needed.

        @param rotation(float): Define if vertices should move along world
        @param dropoffdistance(float): Dropoff distance of the wire deformer
        @param scale(float): Scale value of the wire deformer
        """
        [cmds.setAttr('%s.%s' % (self.wire, attr), l=False)
         for attr in ['rotation', 'dropoffDistance[0]', 'scale[0]']]
        cmds.setAttr('%s.rotation' % self.wire, rotation, l=True)
        cmds.setAttr('%s.dds[0]' % self.wire, dropoffdistance, l=True)
        cmds.setAttr('%s.scale[0]' % self.wire, scale, l=True)
    # end def edit_wire

    def _check_parameter(self):
        """Check the given parameters for validation."""
        # check type errors
        self.__check_type(self.side, str)
        self.__check_type(self.name, str)
        self.__check_type(self.curve, str)
        self.__check_type(self.surface, str)

        # side
        if not (self.side == 'C' or self.side == 'L' or self.side == 'R'):
            raise ValueError('Please specify "C", "L" or "R"!')
        # end if

        # curve
        crv = self.curve
        assert cmds.objExists(crv), 'Object does not exist %s' % crv
        if cmds.nodeType(crv) == 'transform':
            crv = cmds.listRelatives(crv, ad=True, type='shape')[0]
        # end if
        if not cmds.nodeType(crv) == 'nurbsCurve':
            raise ValueError('Please specify a nurbsCurve for curve!')
        # end if

        # surface
        msg = 'Surface does not exist %s' % self.surface
        assert cmds.objExists(self.surface), msg
        sur = self.surface
        if cmds.nodeType(sur) == 'transform':
            sur = cmds.listRelatives(sur, ad=True, type='shape')[0]
        # end if
        if not cmds.nodeType(sur) == 'nurbsSurface':
            raise ValueError('Please specify a nurbsSurface for surface!')
        # end if

        # mesh
        msg = 'Mesh does not exist %s' % self.mesh
        assert cmds.objExists(self.mesh), msg
        ply = self.mesh
        if cmds.nodeType(ply) == 'transform':
            ply = cmds.listRelatives(ply, ad=True, type='shape')[0]
        # end if
        if not cmds.nodeType(ply) == 'mesh':
            raise ValueError('Please specify a polyMesh for mesh!')
        # end if

        # parent
        parent = self.parent
        assert cmds.objExists(parent), 'Object does not exist %s' % parent
        if not cmds.nodeType(parent) == 'transform':
            raise ValueError('Please specify a transform for parent!')
        # end if

        # controlatcv
        if self.complexity:
            if not self.controlatcv:
                raise ValueError('Please specify at least one cv index!')
            # end if
        # end if
    # end def _check_parameter

    def _create_groups(self):
        """Create and setup proper groups for the rig setup."""
        if not cmds.objExists(self.rig_grp):
            cmds.createNode('transform', n=self.rig_grp)
        # end if
        if not cmds.objExists(self.mod_grp):
            cmds.createNode('transform', n=self.mod_grp, p=self.rig_grp)
        # end if
        if not cmds.objExists(self.fol_grp):
            cmds.createNode('transform', n=self.fol_grp, p=self.mod_grp)
        # end if
        if not cmds.objExists(self.vol_grp):
            cmds.createNode('transform', n=self.vol_grp, p=self.mod_grp)
        # end if
        if not cmds.objExists(self.wire_grp):
            cmds.createNode('transform', n=self.wire_grp, p=self.mod_grp)
        # end if
    # end def _create_groups

    def _add_attributes(self):
        """Add attributes to nodes."""
        if not cmds.objExists('%s.showHistory' % self.mod_grp):
            cmds.addAttr(self.mod_grp, ln='showHistory', sn='sho', at='short',
                         min=0, max=1, dv=self.debug, k=False)
            cmds.setAttr('%s.showHistory' % self.mod_grp, e=True, cb=True)
        # end if

        if not cmds.objExists('%s.showFollicles' % self.mod_grp):
            cmds.addAttr(self.mod_grp, ln='showFollicles', at='short',
                         min=0, max=1, dv=self.debug, k=False)
            cmds.setAttr('%s.showFollicles' % self.mod_grp, e=True, cb=True)
        # end if

        if not cmds.objExists('%s.showVolumes' % self.mod_grp):
            cmds.addAttr(self.mod_grp, ln='showVolumes', at='short',
                         min=0, max=1, dv=self.debug, k=False)
            cmds.setAttr('%s.showVolumes' % self.mod_grp, e=True, cb=True)
        # end if

        if not cmds.objExists('%s.showCurve' % self.mod_grp):
            cmds.addAttr(self.mod_grp, ln='showCurve', at='short',
                         min=0, max=1, dv=self.debug, k=False)
            cmds.setAttr('%s.showCurve' % self.mod_grp, e=True, cb=True)
        # end if

        if not cmds.objExists('%s.showSurface' % self.mod_grp):
            cmds.addAttr(self.mod_grp, ln='showSurface', at='short',
                         min=0, max=1, dv=self.debug, k=False)
            cmds.setAttr('%s.showSurface' % self.mod_grp, e=True, cb=True)
        # end if

        if self.complexity:
            if not cmds.objExists('%s.showJoints' % self.mod_grp):
                cmds.addAttr(self.mod_grp, ln='showJoints', at='short',
                             min=0, max=1, dv=self.debug, k=False)
                cmds.setAttr('%s.showJoints' % self.mod_grp, e=True, cb=True)
            # end if

            if not cmds.objExists('%s.showMainControls' % self.mod_grp):
                cmds.addAttr(self.mod_grp, ln='showMainControls', at='short',
                             min=0, max=1, dv=self.debug, k=False)
                cmds.setAttr('%s.showMainControls' % self.mod_grp,
                             e=True, cb=True)
            # end if
        # end if

        if not cmds.objExists('%s.showCollider' % self.mod_grp):
            cmds.addAttr(self.mod_grp, ln='showCollider', at='short',
                         min=0, max=1, dv=self.debug, k=False)
            cmds.setAttr('%s.showCollider' % self.mod_grp, e=True, cb=True)
        # end if

        if not cmds.objExists('%s.%s_VOLUMES' % (self.parent, self.name)):
            cmds.addAttr(self.parent, ln='%s_VOLUMES' % self.name,
                         min=0, max=0, at='short')
            cmds.setAttr('%s.%s_VOLUMES' % (self.parent, self.name),
                         e=True, cb=True)
        # end if

        if not cmds.objExists('%s.volumeOffset' % self.parent):
            cmds.addAttr(self.parent, ln='volumeOffset', at='double3', k=True)
            [cmds.addAttr(self.parent, ln='volumeOffset%s' % axis, at='double',
                          p='volumeOffset', dv=self.volumeoffset[i], k=True)
             for i, axis in enumerate('XYZ')]
        # end if

        if not cmds.objExists('%s.volumeScale' % self.parent):
            cmds.addAttr(self.parent, ln='volumeScale', at='double3', k=True)
            [cmds.addAttr(self.parent, ln='volumeScale%s' % axis, at='double',
                          p='volumeScale', dv=self.volumescale[i], k=True)
             for i, axis in enumerate('XYZ')]
        # end if
    # end def _add_attributes

    def _find_closest_parameter(self):
        """Find closest parameter on given nurbsSurface from the curve."""
        # get shapes
        nrbshp = self.__get_shape(self.surface)
        crvshp = self.__get_shape(self.curve)

        # get MObject of the curve and surface and create proper functionSets
        msel = OpenMaya.MSelectionList()
        [msel.add(item) for item in [nrbshp, crvshp]]
        osurface, ocurve = OpenMaya.MObject(), OpenMaya.MObject()
        msel.getDependNode(0, osurface), msel.getDependNode(1, ocurve)
        fnSurface = OpenMaya.MFnNurbsSurface(osurface)
        fnCurve = OpenMaya.MFnNurbsCurve(ocurve)

        # get worldMatrix as MMatrix of the curve object
        fnThisNode = OpenMaya.MFnDependencyNode(ocurve)
        matrixAttr = fnThisNode.attribute('worldMatrix')
        matrixPlug = OpenMaya.MPlug(ocurve, matrixAttr)
        matrixPlug = matrixPlug.elementByLogicalIndex(0)
        matrixObject = matrixPlug.asMObject()
        worldmatrixData = OpenMaya.MFnMatrixData(matrixObject)
        worldmatrix = worldmatrixData.matrix()

        # create double pointers
        uutil, vutil = OpenMaya.MScriptUtil(), OpenMaya.MScriptUtil()
        uutil.createFromDouble(0.0), vutil.createFromDouble(0.0)
        uptr, vptr = uutil.asDoublePtr(), vutil.asDoublePtr()

        # get the positions of curve
        pacurve = OpenMaya.MPointArray()
        fnCurve.getCVs(pacurve)
        amount = pacurve.length()
        if fnCurve.form() == 3:
            amount = pacurve.length() - 3
        # end if
        for i in range(amount):
            fnSurface.closestPoint(pacurve[i] * worldmatrix, uptr, vptr)
            self.param[i] = [uutil.getDouble(uptr) / fnSurface.numPatchesInU(),
                             vutil.getDouble(vptr) / fnSurface.numPatchesInV()]
        # end for
    # end def _find_closest_parameter

    def _create_rivets(self):
        """Create the follicles or rivets at the retrieved parameter values."""
        if self.useplugin:
            # create nurbsRivet plugin and connect surface and curve properly
            plugname = '%s_%s_NRN' % (self.side, self.name)
            self.nrb_plug = cmds.createNode('MultiNurbsRivet', n=plugname)
            cmds.connectAttr('%s.showHistory' % self.mod_grp,
                             '%s.ihi' % self.nrb_plug)
            nrbshape = self.__get_shape(self.surface)
            crvshape = self.__get_shape(self.curve)
            cmds.connectAttr('%s.worldSpace' % nrbshape,
                             '%s.inSurface' % self.nrb_plug)
            cmds.connectAttr('%s.worldMatrix' % self.surface,
                             '%s.inMatrix' % self.nrb_plug)
            # setup the rivets
            [self._rivet(k, self.param[k], crvshape) for k in self.param]
            return
        # end if
        self.follicle = [self._follicle(k, self.param[k]) for k in self.param]
    # end def _create_rivets

    def _rivet(self, index, paramuv, curveshape):
        """Connect to curve and set parameter values of the nurbsRivet plugin.

        @param index(uint): Unsigned integer index value
        @param paramuv(list): List storing the u and v parameter
        @param curveshape(string): Shape of the curve
        """
        cmds.setAttr('%s.parameterUV[%s].parameterU' %
                     (self.nrb_plug, index), paramuv[0])
        cmds.setAttr('%s.parameterUV[%s].parameterV' %
                     (self.nrb_plug, index), paramuv[1])
        cmds.connectAttr('%s.outTranslate[%s]' % (self.nrb_plug, index),
                         '%s.controlPoints[%s]' % (curveshape, index))
    # end def _rivet

    def _follicle(self, index, paramuv):
        """Create and return a follicle at the defined parameter values.

        @param index(uint): Unsigned integer index value
        @param paramuv(list): List storing the u and v parameter
        """
        fname = '%s_%s%s_FOLShape' % (self.side, self.name, index)
        fshape = self.__node('follicle', fname)
        ftform = cmds.listRelatives(fshape, p=True)[0]
        nrb = self.__get_shape(self.surface)
        cmds.parent(ftform, self.fol_grp)
        cmds.connectAttr('%s.local' % nrb, '%s.inputSurface' % fshape)
        cmds.connectAttr('%s.worldMatrix' % nrb,
                         '%s.inputWorldMatrix' % fshape)
        cmds.connectAttr('%s.outTranslate' % fshape, '%s.translate' % ftform)
        cmds.connectAttr('%s.outRotate' % fshape, '%s.rotate' % ftform)
        cmds.setAttr('%s.parameterU' % fshape, paramuv[0])
        cmds.setAttr('%s.parameterV' % fshape, paramuv[1])
        return [ftform, fshape]
    # end def _follicle

    def _create_volume_setup(self):
        """Setup implicit spheres which will be used as volume spheres."""
        self.__locator(self.collider)
        if self.useplugin:
            # use the plugins
            plugname = '%s_%s_VPC' % (self.side, self.name)
            self.vpc_plug = cmds.createNode('VolumePushCollider', n=plugname)
            cmds.connectAttr('%s.worldMatrix' % self.collider,
                             '%s.inCollider[0]' % self.vpc_plug)
            cmds.connectAttr('%s.showHistory' % self.mod_grp,
                             '%s.ihi' % self.vpc_plug)
            for i in self.param:
                n = '%s_%s' % (self.side, self.name)
                imp = self.__node('implicitSphere', '%s%s_IMPShape' % (n, i))
                trn = cmds.listRelatives(imp, p=True, type='transform')[0]
                grp = cmds.group(trn, n='%sVol%s_TRN' % (n, i))
                cmds.connectAttr('%s.sho' % self.mod_grp, '%s.ihi' % grp)
                p = cmds.getAttr('%s.outTranslate[%s]' % (self.nrb_plug, i))[0]
                r = cmds.getAttr('%s.outRotate[%s]' % (self.nrb_plug, i))[0]
                [cmds.connectAttr('%s.volumeOffset%s' % (self.parent, n),
                                  '%s.translate%s' % (trn, m))
                 for n, m in zip('XYZ', 'YXZ')]
                [cmds.connectAttr('%s.volumeScale%s' % (self.parent, n),
                                  '%s.scale%s' % (trn, m))
                 for n, m in zip('XYZ', 'YXZ')]
                cmds.xform(grp, t=p, ws=True)
                cmds.xform(grp, ro=r)
                cmds.parent(grp, self.vol_grp)
                self._setup_collision_plugin(i, trn)
                self.volumes.append(trn)
            # end for
        else:
            # use the maya nodes
            dcmname = '%s_%sCollider0_DCM' % (self.side, self.name)
            dcm = self.__node('decomposeMatrix', dcmname)
            cmds.connectAttr('%s.wm' % self.collider, '%s.inputMatrix' % dcm)
            for i, f in enumerate(self.follicle):
                n = '%s_%s%s_IMPShape' % (self.side, self.name, i)
                imp = self.__node('implicitSphere', n)
                trn = cmds.listRelatives(imp, p=True, type='transform')[0]
                grp = cmds.group(trn, n='%sVol%s_TRN' % (n, i))
                cmds.parent(grp, f[0])
                cmds.connectAttr('%s.sho' % self.mod_grp, '%s.ihi' % grp)
                [cmds.connectAttr('%s.volumeOffset%s' % (self.parent, n),
                                  '%s.translate%s' % (trn, m))
                 for n, m in zip('XYZ', 'YXZ')]
                [cmds.connectAttr('%s.volumeScale%s' % (self.parent, n),
                                  '%s.scale%s' % (trn, m))
                 for n, m in zip('XYZ', 'YXZ')]
                cmds.xform(grp, ro=[0, 0, 0])
                cmds.parent(grp, self.vol_grp)
                self._create_collision_setup(i, trn, dcm, f[1])
                self._connect_curve_to_follicle(i, f[0])
                self.volumes.append(trn)
            # end for
        # end if
    # end def _create_volume_setup

    def _setup_collision_plugin(self, index, volume):
        """Create volume detection collision setup using a volumPushCollider.

        @param index(uint): Unsigned integer index value
        @param volume(string): Volume transform node
        """
        cmds.connectAttr('%s.worldInverseMatrix' % volume,
                         '%s.inVolume[%s]' % (self.vpc_plug, index))
        cmds.connectAttr('%s.output[%s]' % (self.vpc_plug, index),
                         '%s.puv[%s].parameterV' % (self.nrb_plug, index))
    # end def _setup_collision_plugin

    def _create_collision_setup(self, index, volume, collidermatrix, follicle):
        """Create the volume detection collision setup.

        @param index(uint): Unsigned integer index value
        @param volume(string): Volume transform node
        @param colliderMatrix(string): DecomposeMatrix node of the collider
        @param follicle(string): Follicle shape to access the vParameter
        """
        name = '%s_%s%s' % (self.side, self.name, index)
        pmm = self.__node('pointMatrixMult', '%s_PMM' % name)
        vpr = self.__node('vectorProduct', '%s_VPR' % name)
        cnd = self.__node('condition', '%s_CND' % name)
        rev = self.__node('reverse', '%s_REV' % name)
        self.pointmatrixmult.append(pmm)
        self.reverse.append(rev)
        # connect attributes
        cmds.connectAttr('%s.worldInverseMatrix' % volume, '%s.inMatrix' % pmm)
        cmds.connectAttr('%s.outputTranslate' % collidermatrix,
                         '%s.inPoint' % pmm)
        cmds.connectAttr('%s.output' % pmm, '%s.input1' % vpr)
        cmds.connectAttr('%s.output' % pmm, '%s.input2' % vpr)
        cmds.connectAttr('%s.outputX' % vpr, '%s.firstTerm' % cnd)
        cmds.connectAttr('%s.outputX' % vpr, '%s.colorIfTrueR' % cnd)
        cmds.connectAttr('%s.outColorR' % cnd, '%s.inputX' % rev)
        cmds.setAttr('%s.parameterV' % follicle, l=False)
        cmds.connectAttr('%s.outputX' % rev,
                         '%s.parameterV' % follicle, f=True)
        # set attributes
        cmds.setAttr('%s.secondTerm' % cnd, 1.0)
        cmds.setAttr('%s.operation' % cnd, 5)
        cmds.setAttr('%s.colorIfFalseR' % cnd, 1.0)
    # end def _create_collision_setup

    def _connect_curve_to_follicle(self, index, follicle):
        """Connect each cv to the proper follicle. This will reshape the curve.

        @param index(uint): Unsigned integer index value
        @param follicle(string): Follicle transform to retrieve worldMatrix
        """
        name = '%s_%s%sToFollicle_DCM' % (self.side, self.name, index)
        crvshape = self.__get_shape(self.curve)
        dcm = self.__node('decomposeMatrix', name)
        cmds.connectAttr('%s.worldMatrix' % follicle, '%s.inputMatrix' % dcm)
        cmds.connectAttr('%s.outputTranslate' % dcm,
                         '%s.controlPoints[%s]' % (crvshape, index))
    # end def _connect_curve_to_follicle

    def _setup_wire_deformer(self, mesh, wire, wirebase, curve,
                             parent, complexity):
        """Setup the wire deformer. If complexity is 1 or higher call this
        function recursively to create a wire deformer on the nurbs surface.

        @param mesh(string): PolyMesh used to wire deform
        @param wire(string): Descriptive part of the name of the wire deformer
        @param wirebase(string): Descriptive part of the name of the base wire
        @param curve(string): Curve used for wireTool deformer
        @param parent(string): Parent node of the wire setup
        @param complexity(uint): complexity level value
        """
        w = wire
        wb = wirebase
        cmds.wire(mesh, w=curve, dds=[0, 10000], n=w, foc=False)
        cmds.rename(cmds.listConnections('%s.baseWire[0]' % w)[0], wb)
        if not cmds.listRelatives(curve, p=True) == [self.wire_grp]:
            cmds.parent(curve, wb, self.wire_grp)
        # end if
        wbs = cmds.listRelatives(wb, ad=True, type='shape')[0]
        cs = cmds.listRelatives(curve, ad=True, type='shape')[0]
        cmds.setAttr('%s.rotation' % w, 0)
        # connect to showHistory
        cmds.connectAttr('%s.showHistory' % self.mod_grp, '%s.ihi' % w)
        cmds.connectAttr('%s.showHistory' % self.mod_grp, '%s.ihi' % wb)
        cmds.connectAttr('%s.showHistory' % self.mod_grp, '%s.ihi' % wbs)
        cmds.connectAttr('%s.showHistory' % self.mod_grp, '%s.ihi' % cs)
        if complexity:
            cmds.duplicate(self.curve, n=self.nrbcurve)
            return self._setup_wire_deformer(self.surface, self.nrbwire,
                                             self.nrbwirebase, self.nrbcurve,
                                             self.parent, 0)
        # end if
    # end def _setup_wire_deformer

    def _create_main_controls(self):
        """Create main controls which drives nurbsSurface via wireDeformer."""
        for cvid in self.controlatcv:
            pos = cmds.xform('%s.cv[%s]' % (self.nrbcurve, cvid),
                             q=True, t=True, ws=True)
            ctl = self._create_control(cvid, pos, self.parent)
            jnt = self._create_joint(cvid, ctl)
            self.controls.append(ctl)
            self.joints.append(jnt)
        # end for
    # end def _create_main_controls

    def _create_control(self, index, position, parent):
        """Create and return a control and its group.

        @param index(uint): Index value to name the joint properly
        @param position(list): 3 float value list storing position information
        @param parent(string): Parent of the control group
        """
        n = '%s_%s%s' % (self.side, self.name, index)
        grp = cmds.createNode('transform', n='%s_GRP' % n)
        ctl = cmds.spaceLocator(n='%s_CTL' % n)[0]
        shp = cmds.listRelatives(ctl, ad=True, type='shape')[0]
        cmds.parent(ctl, grp)
        cmds.xform(grp, t=position, ws=True)
        cmds.parent(grp, parent)
        # connect to showHistory and showMainControls
        cmds.connectAttr('%s.showMainControls' % self.mod_grp, '%s.v' % shp)
        cmds.connectAttr('%s.showHistory' % self.mod_grp, '%s.ihi' % grp)
        return ctl
    # end def _create_control

    def _create_joint(self, index, control):
        """Create and return a joint parented under the specified control.

        @param index(uint): Index value to name the joint properly
        @param control(string): Parent of the joint
        """
        n = '%s_%s%s' % (self.side, self.name, index)
        jnt = cmds.createNode('joint', n='%s_JNT' % n, p=control)
        cmds.xform(jnt, t=[0, 0, 0]), cmds.xform(jnt, ro=[0, 0, 0])
        cmds.setAttr('%s.jo' % jnt, 0, 0, 0)
        cmds.connectAttr('%s.showJoints' % self.mod_grp, '%s.v' % jnt)
        cmds.connectAttr('%s.showHistory' % self.mod_grp, '%s.ihi' % jnt)
        return jnt
    # end def _create_joint

    def _bind_joint_setup(self):
        """Skinweight the nurbs curve which affects the nurbs surface."""
        skn = cmds.skinCluster(self.nrbcurve, self.joints,
                               tsb=True, nw=1, sm=0, bm=0, mi=1, dr=10)[0]
        bindpose = cmds.listConnections('%s.bindPose' % skn)[0]
        cmds.connectAttr('%s.showHistory' % self.mod_grp, '%s.ihi' % skn)
        cmds.connectAttr('%s.showHistory' % self.mod_grp, '%s.ihi' % bindpose)
    # end def _bind_joint_setup

    def _setup_parent(self):
        """Parent and constraint the nodes of the rig setup properly."""
        # constraint the volume group to the parent
        pac = cmds.parentConstraint(self.parent, self.vol_grp, mo=True)[0]
        scn = cmds.scaleConstraint(self.parent, self.vol_grp, mo=True)[0]
        [cmds.connectAttr('%s.showHistory' % self.mod_grp, '%s.ihi' % item)
         for item in [pac, scn, self.surface]]
        children = [self.surface, self.wirebase]
        if self.complexity:
            children.append(self.nrbwirebase)
        # end if
        cmds.parent(children, self.parent)
        cmds.parent(self.collider, self.mod_grp)
    # end def _setup_parent

    def _setup_display(self):
        """Setup the proper visibility connections to the mod group."""
        cmds.connectAttr('%s.showFollicles' % self.mod_grp,
                         '%s.v' % self.fol_grp)
        cmds.connectAttr('%s.showVolumes' % self.mod_grp,
                         '%s.v' % self.vol_grp)
        cmds.connectAttr('%s.showCurve' % self.mod_grp,
                         '%s.v' % self.wire_grp)
        cmds.connectAttr('%s.showSurface' % self.mod_grp,
                         '%s.v' % self.surface)
        cmds.connectAttr('%s.showCollider' % self.mod_grp,
                         '%s.v' % self.collider)
        [cmds.setAttr('%s.%s' % (self.collider, attr), l=True, k=False)
         for attr in ['sx', 'sy', 'sz', 'v']]
    # end def _setup_display

    def _clean_up(self):
        """Lock and hide all attributes of the items in the to_clean list."""
        if self.debug:
            return
        # end if
        i1 = set(cmds.listConnections('%s.sho' % self.mod_grp))
        i2 = set(cmds.listConnections('%s.sho' % self.mod_grp, sh=True))
        for item in i1 | i2:
            if item == self.collider:
                continue
            # end if
            attrs = cmds.listAttr(item, k=True)
            if attrs:
                [cmds.setAttr('%s.%s' % (item, attr), l=True, k=False)
                 for attr in attrs if cmds.objExists('%s.%s' % (item, attr))]
            # end if
        # end for
        [cmds.setAttr('%s.%s' % (item, attr), l=True, k=False)
         for item in [self.mod_grp, self.fol_grp, self.vol_grp, self.wire_grp]
         for attr in cmds.listAttr(item, k=True)]
    # end def _clean_up

    def __check_type(self, param, ptype):
        """Helper function to check the type of the given parameter.

        @param param(string): Parameter to check the type of
        @param ptype(string): Python valid types
        """
        if not isinstance(param, ptype):
            raise TypeError('Use %s as inputType for %s!' % (ptype, param))
        # end if
    # end def __check_type

    def __get_shape(self, transform):
        """
        Helper function which returns the shape node of the given transform.

        @param transform(string): The transform node of which we get the shape
        """
        return cmds.listRelatives(transform, ad=True, type='shape')[0]
    # end def __get_shape

    def __node(self, nodetype, name):
        """Helper function to create and return a maya node whose
        isHistoricallyInteresting attribute is connected to the
        mod group's showHistory attribute.

        @param nodetype(string): The type of the node which gets created
        @param name(string): Name of the node
        """
        nd = cmds.createNode(nodetype, n=name)
        cmds.connectAttr('%s.showHistory' % self.mod_grp, '%s.ihi' % nd)
        return nd
    # end def __node

    def __locator(self, name):
        """Helper function to create and return a maya spacelocator whose
        isHistoricallyInteresting attribute is connected to the
        mod group's showHistory attribute.

        @param name(string): Name of the spaceLocator
        """
        loc = cmds.spaceLocator(n=name)[0]
        locshape = cmds.listRelatives(loc, ad=True, type='shape')[0]
        cmds.connectAttr('%s.showHistory' % self.mod_grp, '%s.ihi' % loc)
        cmds.connectAttr('%s.showHistory' % self.mod_grp, '%s.ihi' % locshape)
        return loc
    # end def __locator
# end class VolumePushCollider


plugin.initialize('VolumePushCollider')
plugin.initialize('MultiNurbsRivet')


# vpc = VolumePushCollider(side='C', name='shirt', curve='C_shirt_CRV',
#                          surface='C_shirt_NRB', mesh='C_dress_LO',
#                          parent='C_spinePelvis_CTL', volumeoffset=[0, 1.5, 0],
#                          volumescale=[2.5, 3, 3], complexity=1,
#                          controlatcv=[19, 31, 7, 43], useplugin=True)
# vpc.add_collider()
