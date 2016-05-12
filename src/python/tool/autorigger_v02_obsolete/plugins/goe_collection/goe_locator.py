"""
@package: core.interface
@brief: RigInterface implementations of the rig interfaces
@author: Emre Tekinalp
@contact: e.tekinalp@icloud.com
"""

from maya import cmds
from maya import OpenMaya
from maya import OpenMayaMPx
from maya import OpenMayaRender
from maya import OpenMayaUI
from shapes import (arrow, circle, cog, cross, cube, dial, gear, misc,
                    ring, sphere, square, triangle)

nodename = 'goe_locator'
nodeid = OpenMaya.MTypeId(0x4728489)

gl_renderer = OpenMayaRender.MHardwareRenderer.theRenderer()
gl_ft = gl_renderer.glFunctionTable()

PI = 3.14159265359


class CustomControl(OpenMayaMPx.MPxLocatorNode):

    """Create a custom locator used for the PandorasBox rig system."""

    a_shape = OpenMaya.MObject()
    a_size = OpenMaya.MObject()
    a_orientation = OpenMaya.MObject()
    a_fill = OpenMaya.MObject()
    a_alpha = OpenMaya.MObject()
    a_annotation = OpenMaya.MObject()

    def __init__(self):
        """Initialize CustomControl class."""
        OpenMayaMPx.MPxLocatorNode.__init__(self)
        self.shape = 0
        self.size = 1
        self.rotation = 0
        self.fill = 0
        self.alpha = 0
        self.annotation = 0
    # end def __init__()

    def compute(self, plug, data):
        """Compute method of the MPxLocatorNode."""
        return OpenMaya.kUnknownParameter
    # end def compute()

    def draw(self, view, path, style, status):
        """Draw method generates the custom locator shape by using OpenGL."""
        node = OpenMaya.MFnDependencyNode(self.thisMObject())

        # get the shape value
        self.shape = OpenMaya.MPlug(self.thisMObject(),
                                    CustomControl.a_shape).asShort()
        # get the size value
        self.size = OpenMaya.MPlug(self.thisMObject(),
                                   CustomControl.a_size).asFloat()
        # get the orientation value
        self.rotation = OpenMaya.MPlug(self.thisMObject(),
                                       CustomControl.a_orientation).asShort()
        # get the alpha value
        self.alpha = OpenMaya.MPlug(self.thisMObject(),
                                    CustomControl.a_alpha).asFloat()
        # get the fill value
        self.fill = OpenMaya.MPlug(self.thisMObject(),
                                   CustomControl.a_fill).asShort()
        # get the annotation value
        self.annotation = OpenMaya.MPlug(self.thisMObject(),
                                         CustomControl.a_annotation).asShort()
        # get the color value
        color = cmds.getAttr('%s.overrideColor' % node.name())
        if color:
            if isinstance(color, list):
                color = int(color[0] - 1)
            else:
                color = int(color - 1)
            # end if color is a list
        # end if color is not 0
        if color < 0:
            color = 0
        # end if color is smaller than 0

        view.beginGL()
        # enable blend mode
        gl_ft.glEnable(OpenMayaRender.MGL_BLEND)
        # define blend mode
        gl_ft.glBlendFunc(OpenMayaRender.MGL_SRC_ALPHA,
                          OpenMayaRender.MGL_ONE_MINUS_SRC_ALPHA)
        rgba = view.colorAtIndex(int(color), OpenMayaUI.M3dView.kActiveColors)
        rgba.a = self.alpha
        # define the colors of the current state
        if (status == OpenMayaUI.M3dView.kLead):
            rgba = view.colorAtIndex(18, OpenMayaUI.M3dView.kActiveColors)
        elif (status == OpenMayaUI.M3dView.kActive):
            view.setDrawColor(15, OpenMayaUI.M3dView.kActiveColors)
        elif (status == OpenMayaUI.M3dView.kActiveAffected):
            view.setDrawColor(8, OpenMayaUI.M3dView.kActiveColors)
        elif (status == OpenMayaUI.M3dView.kDormant):
            gl_ft.glColor4f(rgba.r, rgba.g, rgba.b, rgba.a)
        elif (status == OpenMayaUI.M3dView.kHilite):
            view.setDrawColor(17, OpenMayaUI.M3dView.kActiveColors)
        # end if setDrawColor

        # set the transform values
        self._set_transforms(node)
        # set text of node
        if self.annotation:
            p_text = OpenMaya.MPoint(0, 0, 0)
            view.drawText(node.name(), p_text)
        # end if show annotation

        # draw the shape
        self._shapes(rgba)
        # disable blend mode
        gl_ft.glDisable(OpenMayaRender.MGL_BLEND)

        view.endGL()
    # end def draw()

    def _shapes(self, rgba):
        """Storage of all the shape vertex point positions."""
        if self.shape == 0:
            circle.circle()
            if self.fill:
                gl_ft.glColor4f(rgba.r, rgba.g, rgba.b, rgba.a)
                circle.circle(OpenMayaRender.MGL_POLYGON)
            # end if fill
        elif self.shape == 1:
            square.square()
            if self.fill:
                gl_ft.glColor4f(rgba.r, rgba.g, rgba.b, rgba.a)
                square.square(OpenMayaRender.MGL_POLYGON)
            # end if fill
        elif self.shape == 2:
            triangle.triangle()
            if self.fill:
                gl_ft.glColor4f(rgba.r, rgba.g, rgba.b, rgba.a)
                triangle.triangle(OpenMayaRender.MGL_TRIANGLE_STRIP)
            # end if fill
        elif self.shape == 3:
            sphere.sphere()
            if self.fill:
                gl_ft.glColor4f(rgba.r, rgba.g, rgba.b, rgba.a)
                sphere.sphere(OpenMayaRender.MGL_POLYGON)
            # end if fill
        elif self.shape == 4:
            cube.cube()
            if self.fill:
                gl_ft.glColor4f(rgba.r, rgba.g, rgba.b, rgba.a)
                cube.cube(OpenMayaRender.MGL_POLYGON)
            # end if fill
        elif self.shape == 5:
            gear.gear()
        elif self.shape == 6:
            circle.two_arrow_circle()
        elif self.shape == 7:
            circle.four_arrow_circle()
        elif self.shape == 8:
            arrow.arrow()
        elif self.shape == 9:
            arrow.big_arrow()
        elif self.shape == 10:
            arrow.double_arrow()
        elif self.shape == 11:
            arrow.visor_arrow()
        elif self.shape == 12:
            cross.cross()
        elif self.shape == 13:
            ring.ring()
        elif self.shape == 14:
            square.box()
            if self.fill:
                gl_ft.glColor4f(rgba.r, rgba.g, rgba.b, rgba.a)
                square.box(OpenMayaRender.MGL_POLYGON)
            # end if fill
        elif self.shape == 15:
            gear.gear2(OpenMayaRender.MGL_QUADS)
        elif self.shape == 16:
            ring.ring2(OpenMayaRender.MGL_POLYGON)
        elif self.shape == 17:
            gear.gear3(OpenMayaRender.MGL_POLYGON)
        elif self.shape == 18:
            gear.halfgear(OpenMayaRender.MGL_POLYGON)
        elif self.shape == 19:
            ring.ring3(OpenMayaRender.MGL_POLYGON)
        elif self.shape == 20:
            ring.ring4(OpenMayaRender.MGL_POLYGON)
        elif self.shape == 21:
            dial.dial(OpenMayaRender.MGL_POLYGON)
        elif self.shape == 22:
            ring.ring5(OpenMayaRender.MGL_POLYGON)
        elif self.shape == 23:
            dial.dial2(OpenMayaRender.MGL_POLYGON)
        elif self.shape == 24:
            cog.cog1(OpenMayaRender.MGL_TRIANGLE_FAN)
        elif self.shape == 25:
            misc.goe()
        # end if call shapes
    # end def _shapes()

    def _set_transforms(self, node):
        """Helper function to set localPosition values of given node."""
        lx = cmds.getAttr(node.name() + '.localPositionX')
        ly = cmds.getAttr(node.name() + '.localPositionY')
        lz = cmds.getAttr(node.name() + '.localPositionZ')
        if isinstance(lx, list):
            lx = lx[0]
        if isinstance(ly, list):
            ly = ly[0]
        if isinstance(lz, list):
            lz = lz[0]
        gl_ft.glTranslatef(lx, ly, lz)

        # rotate the shape
        if not self.rotation:
            gl_ft.glRotatef(0, 1, 0, 0)
            gl_ft.glScalef(1, 1, 1)
        elif self.rotation == 1:
            gl_ft.glRotatef(0, 1, 0, 0)
            gl_ft.glScalef(-1, 1, 1)
        elif self.rotation == 2:
            gl_ft.glRotatef(0, 1, 0, 0)
            gl_ft.glScalef(1, -1, 1)
        elif self.rotation == 3:
            gl_ft.glRotatef(0, 1, 0, 0)
            gl_ft.glScalef(-1, -1, 1)
        elif self.rotation == 4:
            gl_ft.glRotatef(0, 1, 0, 0)
            gl_ft.glScalef(1, 1, -1)
        elif self.rotation == 5:
            gl_ft.glRotatef(0, 1, 0, 0)
            gl_ft.glScalef(1, -1, -1)
        elif self.rotation == 6:
            gl_ft.glRotatef(0, 1, 0, 0)
            gl_ft.glScalef(-1, -1, -1)
        elif self.rotation == 7:
            gl_ft.glRotatef(0, 1, 0, 0)
            gl_ft.glScalef(-1, 1, -1)
        elif self.rotation == 8:
            gl_ft.glRotatef(90, 0, 1, 0)
            gl_ft.glScalef(1, 1, 1)
        elif self.rotation == 9:
            gl_ft.glRotatef(90, 0, 1, 0)
            gl_ft.glScalef(-1, 1, 1)
        elif self.rotation == 10:
            gl_ft.glRotatef(90, 0, 1, 0)
            gl_ft.glScalef(1, -1, 1)
        elif self.rotation == 11:
            gl_ft.glRotatef(90, 0, 1, 0)
            gl_ft.glScalef(-1, -1, 1)
        elif self.rotation == 12:
            gl_ft.glRotatef(90, 0, 1, 0)
            gl_ft.glScalef(1, 1, -1)
        elif self.rotation == 13:
            gl_ft.glRotatef(90, 0, 1, 0)
            gl_ft.glScalef(1, -1, -1)
        elif self.rotation == 14:
            gl_ft.glRotatef(90, 0, 1, 0)
            gl_ft.glScalef(-1, -1, -1)
        elif self.rotation == 15:
            gl_ft.glRotatef(90, 0, 1, 0)
            gl_ft.glScalef(-1, 1, -1)
        elif self.rotation == 16:
            gl_ft.glRotatef(90, 0, 0, 1)
            gl_ft.glScalef(1, 1, 1)
        elif self.rotation == 17:
            gl_ft.glRotatef(90, 0, 0, 1)
            gl_ft.glScalef(-1, 1, 1)
        elif self.rotation == 18:
            gl_ft.glRotatef(90, 0, 0, 1)
            gl_ft.glScalef(1, -1, 1)
        elif self.rotation == 19:
            gl_ft.glRotatef(90, 0, 0, 1)
            gl_ft.glScalef(-1, -1, 1)
        elif self.rotation == 20:
            gl_ft.glRotatef(90, 0, 0, 1)
            gl_ft.glScalef(1, 1, -1)
        elif self.rotation == 21:
            gl_ft.glRotatef(90, 0, 0, 1)
            gl_ft.glScalef(1, -1, -1)
        elif self.rotation == 22:
            gl_ft.glRotatef(90, 0, 0, 1)
            gl_ft.glScalef(-1, -1, -1)
        elif self.rotation == 23:
            gl_ft.glRotatef(90, 0, 0, 1)
            gl_ft.glScalef(-1, 1, -1)
        elif self.rotation == 24:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glRotatef(90, 0, 0, 1)
            gl_ft.glScalef(1, 1, 1)
        elif self.rotation == 25:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glRotatef(90, 0, 0, 1)
            gl_ft.glScalef(-1, 1, 1)
        elif self.rotation == 26:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glRotatef(90, 0, 0, 1)
            gl_ft.glScalef(1, -1, 1)
        elif self.rotation == 27:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glRotatef(90, 0, 0, 1)
            gl_ft.glScalef(-1, -1, 1)
        elif self.rotation == 28:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glRotatef(90, 0, 0, 1)
            gl_ft.glScalef(1, 1, -1)
        elif self.rotation == 29:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glRotatef(90, 0, 0, 1)
            gl_ft.glScalef(1, -1, -1)
        elif self.rotation == 30:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glRotatef(90, 0, 0, 1)
            gl_ft.glScalef(-1, -1, -1)
        elif self.rotation == 31:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glRotatef(90, 0, 0, 1)
            gl_ft.glScalef(-1, 1, -1)
        elif self.rotation == 32:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glRotatef(90, 0, 1, 0)
            gl_ft.glScalef(1, 1, 1)
        elif self.rotation == 33:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glRotatef(90, 0, 1, 0)
            gl_ft.glScalef(-1, 1, 1)
        elif self.rotation == 34:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glRotatef(90, 0, 1, 0)
            gl_ft.glScalef(1, -1, 1)
        elif self.rotation == 35:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glRotatef(90, 0, 1, 0)
            gl_ft.glScalef(-1, -1, 1)
        elif self.rotation == 36:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glRotatef(90, 0, 1, 0)
            gl_ft.glScalef(1, 1, -1)
        elif self.rotation == 37:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glRotatef(90, 0, 1, 0)
            gl_ft.glScalef(1, -1, -1)
        elif self.rotation == 38:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glRotatef(90, 0, 1, 0)
            gl_ft.glScalef(-1, -1, -1)
        elif self.rotation == 39:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glRotatef(90, 0, 1, 0)
            gl_ft.glScalef(-1, 1, -1)
        elif self.rotation == 40:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glScalef(1, 1, 1)
        elif self.rotation == 41:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glScalef(-1, 1, 1)
        elif self.rotation == 42:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glScalef(1, -1, 1)
        elif self.rotation == 43:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glScalef(-1, -1, 1)
        elif self.rotation == 44:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glScalef(1, 1, -1)
        elif self.rotation == 45:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glScalef(1, -1, -1)
        elif self.rotation == 46:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glScalef(-1, -1, -1)
        elif self.rotation == 47:
            gl_ft.glRotatef(90, 1, 0, 0)
            gl_ft.glScalef(-1, 1, -1)
        # end if set orientation

        # define the globalSize of the locator
        gl_ft.glScalef(self.size, self.size, self.size)

        # define the localSize of the locator
        lsx = cmds.getAttr(node.name() + '.localScaleX')
        lsy = cmds.getAttr(node.name() + '.localScaleY')
        lsz = cmds.getAttr(node.name() + '.localScaleZ')
        if isinstance(lsx, list):
            lsx = lsx[0]
        if isinstance(lsy, list):
            lsy = lsy[0]
        if isinstance(lsz, list):
            lsz = lsz[0]
        gl_ft.glScalef(lsx, lsy, lsz)
    # end def _set_transforms()
# end class CustomControl()


def get_node_position(node):
    """Get the worldSpace position of the created node."""
    fn_dagnode = OpenMaya.MFnDagNode(node)
    dag_path = OpenMaya.MDagPath()
    fn_dagnode.getPath(dag_path)
    dag_path.pop()
    fn_transform = OpenMaya.MFnTransform(dag_path)
    return fn_transform.translation(OpenMaya.MSpace.kWorld)
# end def get_node_position


def nodeCreator():
    """Recreate node function."""
    return OpenMayaMPx.asMPxPtr(CustomControl())
# end def nodeCreator()


def nodeInitializer():
    """Initialize attributes and setup attribue affects."""
    n_attr = OpenMaya.MFnNumericAttribute()

    # size
    CustomControl.a_size = n_attr.create('size', 'siz',
                                         OpenMaya.MFnNumericData.kFloat, 1.0)
    n_attr.setWritable(True)
    n_attr.setReadable(True)
    n_attr.setStorable(True)
    n_attr.setKeyable(False)
    n_attr.setChannelBox(True)
    CustomControl.addAttribute(CustomControl.a_size)

    # shape
    CustomControl.a_shape = n_attr.create('shape', 'shp',
                                          OpenMaya.MFnNumericData.kShort)
    n_attr.setWritable(True)
    n_attr.setReadable(True)
    n_attr.setStorable(True)
    n_attr.setKeyable(False)
    n_attr.setChannelBox(True)
    n_attr.setMin(0)
    n_attr.setMax(25)
    CustomControl.addAttribute(CustomControl.a_shape)

    # orientation
    CustomControl.a_orientation = n_attr.create('orientation', 'ori',
                                                OpenMaya.MFnNumericData.kShort)
    n_attr.setWritable(True)
    n_attr.setReadable(True)
    n_attr.setStorable(True)
    n_attr.setKeyable(False)
    n_attr.setChannelBox(True)
    n_attr.setMin(0)
    n_attr.setMax(47)
    CustomControl.addAttribute(CustomControl.a_orientation)

    # alpha
    CustomControl.a_alpha = n_attr.create('alpha', 'alp',
                                          OpenMaya.MFnNumericData.kFloat, 1.0)
    n_attr.setWritable(True)
    n_attr.setReadable(True)
    n_attr.setStorable(True)
    n_attr.setKeyable(False)
    n_attr.setChannelBox(True)
    n_attr.setMin(0.0)
    n_attr.setMax(1.0)
    CustomControl.addAttribute(CustomControl.a_alpha)

    # fill
    CustomControl.a_fill = n_attr.create('fill', 'fil',
                                         OpenMaya.MFnNumericData.kShort)
    n_attr.setWritable(True)
    n_attr.setReadable(True)
    n_attr.setStorable(True)
    n_attr.setKeyable(False)
    n_attr.setChannelBox(True)
    n_attr.setMin(0)
    n_attr.setMax(1)
    CustomControl.addAttribute(CustomControl.a_fill)

    # annotation
    CustomControl.a_annotation = n_attr.create('annotation', 'ano',
                                               OpenMaya.MFnNumericData.kShort)
    n_attr.setWritable(True)
    n_attr.setReadable(True)
    n_attr.setStorable(True)
    n_attr.setKeyable(False)
    n_attr.setChannelBox(True)
    n_attr.setMin(0)
    n_attr.setMax(1)
    CustomControl.addAttribute(CustomControl.a_annotation)
# end def nodeInitializer()


def initializePlugin(obj):
    """Initialize plugin."""
    plugin = OpenMayaMPx.MFnPlugin(obj, 'GravityOfExplosion', '1.0', 'Any')
    try:
        plugin.registerNode(nodename, nodeid, nodeCreator, nodeInitializer,
                            OpenMayaMPx.MPxNode.kLocatorNode)
    except:
        raise Exception('Failed to load plugin: %s' % nodename)
# end def initializePlugin()


def uninitializePlugin(obj):
    """Uninitialize plugin."""
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(nodeid)
    except:
        raise Exception('Failed to unload plugin: %s' % nodename)
# end def uninitializePlugin()


def curve_to_opengl():
    """Select curves and run this script. It returns you the proper gl_ft."""
    for crv in cmds.ls(sl=True):
        print '\n    gl_ft.glBegin(render)'
        for cv in cmds.ls('%s.vtx[*]' % crv, fl=True):
            pos = cmds.xform(cv, q=True, t=True, ws=True)
            print '    gl_ft.glVertex3f(%s, %s, %s)' % (pos[0], pos[1], pos[2])
        # end for iterate cvs of curve
        print '    gl_ft.glEnd()'
    # end for iterate selected curves
# end def curve_to_opengl

curve_to_opengl()
