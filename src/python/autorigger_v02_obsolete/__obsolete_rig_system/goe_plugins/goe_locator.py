"""
@package: core.interface
@brief: RigInterface implementations of the rig interfaces
@author: Emre Tekinalp
@contact: e.tekinalp@icloud.com
"""

import math
from maya import cmds
from maya import OpenMaya
from maya import OpenMayaMPx
from maya import OpenMayaRender
from maya import OpenMayaUI

nodename = 'pb_control'
nodeid = OpenMaya.MTypeId(0x4728489)

gl_renderer = OpenMayaRender.MHardwareRenderer.theRenderer()
gl_ft = gl_renderer.glFunctionTable()


class CustomControl(OpenMayaMPx.MPxLocatorNode):

    """Create a custom locator used for the PandorasBox rig system."""

    a_shape = OpenMaya.MObject()
    a_size = OpenMaya.MObject()
    a_orientation = OpenMaya.MObject()

    def __init__(self):
        """Initialize CustomControl class."""
        OpenMayaMPx.MPxLocatorNode.__init__(self)
        self.shape = 0
        self.size = 1
        self.rotation = 0
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

        color = cmds.getAttr('%s.overrideColor' % node.name())
        if color:
            if isinstance(color, list):
                color = int(color[0] - 1)
            else:
                color = int(color - 1)
            # end if color is a list
        if color < 0:
            color = 0
        # end if color is smaller than 0

        view.beginGL()
        # enable blend mode
        gl_ft.glEnable(OpenMayaRender.MGL_BLEND)
        # define blend mode
        gl_ft.glBlendFunc(OpenMayaRender.MGL_SRC_ALPHA,
                          OpenMayaRender.MGL_ONE_MINUS_SRC_ALPHA)
        # define the colors of the current state
        if (status == OpenMayaUI.M3dView.kLead):
            view.setDrawColor(18, OpenMayaUI.M3dView.kActiveColors)
        elif (status == OpenMayaUI.M3dView.kActive):
            view.setDrawColor(15, OpenMayaUI.M3dView.kActiveColors)
        elif (status == OpenMayaUI.M3dView.kActiveAffected):
            view.setDrawColor(8, OpenMayaUI.M3dView.kActiveColors)
        elif (status == OpenMayaUI.M3dView.kDormant):
            view.setDrawColor(int(color), OpenMayaUI.M3dView.kActiveColors)
        elif (status == OpenMayaUI.M3dView.kHilite):
            view.setDrawColor(17, OpenMayaUI.M3dView.kActiveColors)
        # end if setDrawColor

        # set the transform values
        self._set_transforms(node)
        # draw the shape
        shapes(self.shape, self.size)
        # disable blend mode
        gl_ft.glDisable(OpenMayaRender.MGL_BLEND)

        view.endGL()
    # end def draw()

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
    n_attr.setMax(38)
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
# end def nodeInitializer()


def shapes(shape, size):
    """Storage of all the shape vertex point positions."""
    PI = 3.14159265359

    if shape == 0:
        # 0 circle
        posx, posz = 0, 0
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(256):
            x = math.cos(i * 2 * PI / 128) + posx
            z = math.sin(i * 2 * PI / 128) + posz
            gl_ft.glVertex3f(x, 0, z)
        gl_ft.glEnd()
    elif shape == 1:
        # 1 square
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(-1.0, 0.0, -1.0)
        gl_ft.glVertex3f(-1.0, 0.0, 1.0)
        gl_ft.glVertex3f(1.0, 0.0, 1.0)
        gl_ft.glVertex3f(1.0, 0.0, -1.0)
        gl_ft.glVertex3f(-1.0, 0.0, -1.0)
        gl_ft.glEnd()
    elif shape == 2:
        # 2 triangle
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(0.0, 0.0, 1.0)
        gl_ft.glVertex3f(-1.0, 0.0, -1.0)
        gl_ft.glVertex3f(1.0, 0.0, -1.0)
        gl_ft.glVertex3f(0.0, 0.0, 1.0)
        gl_ft.glEnd()
    elif shape == 3:
        # 3 circlein circle
        posx = 0
        posz = 0

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(180):
            x = math.cos(1 * i * 2 * PI / 89.5) + posx
            z = math.sin(1 * i * 2 * PI / 89.5) + posz
            gl_ft.glVertex3f(x, 0, z)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(180):
            x = math.cos(1 * i * 2 * PI / 89.5) + posx
            z = math.sin(1 * i * 2 * PI / 89.5) + posz
            gl_ft.glVertex3f(x / 2, 0, z / 2)
        gl_ft.glEnd()
    elif shape == 4:
        # 4 targetA
        posx, posz = 0, 0

        gl_ft.glRotatef(45, 0, 1, 0)

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(200):
            x = math.cos(1 * i * 1 * PI / 4 / 99.5) + posx
            z = math.sin(1 * i * 1 * PI / 4 / 99.5) + posz
            gl_ft.glVertex3f(x, 0, z)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(0.0, 0.0, 1.0)
        gl_ft.glVertex3f(0.0, 0.0, -1.0)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(1.0, 0.0, 0.0)
        gl_ft.glVertex3f(-1.0, 0.0, 0.0)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(200):
            x = math.cos(1 * i * 1 * PI / 4 / 99.5) + posx
            z = math.sin(1 * i * 1 * PI / 4 / 99.5) + posz
            gl_ft.glVertex3f(-x, 0, -z)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(200):
            x = math.cos(1 * i * 1 * PI / 4 / 100) + posx
            z = math.sin(1 * i * 1 * PI / 4 / 100) + posz
            gl_ft.glVertex3f(-x / 2, 0, z / 2)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(200):
            x = math.cos(1 * i * 1 * PI / 4 / 100) + posx
            z = math.sin(1 * i * 1 * PI / 4 / 100) + posz
            gl_ft.glVertex3f(x / 2, 0, -z / 2)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(200):
            x = math.cos(1 * i * 1 * PI / 4 / 99.5) + posx
            z = math.sin(1 * i * 1 * PI / 4 / 99.5) + posz
            gl_ft.glVertex3f(-x / 1.15, 0, z / 1.15)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(200):
            x = math.cos(1 * i * 1 * PI / 4 / 99.5) + posx
            z = math.sin(1 * i * 1 * PI / 4 / 99.5) + posz
            gl_ft.glVertex3f(x / 1.15, 0, -z / 1.15)
        gl_ft.glEnd()
    elif shape == 5:
        # 5 targetB
        posx, posz = 0, 0
        startx, startz = 0, 0
        endx, endz = 0, 0

        gl_ft.glRotatef(45, 0, 1, 0)

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 8 / 80) + posx
            z = math.sin(1 * i * 2 * PI / 8 / 80) + posz
            if not i:
                startx += x
                startz += z
            elif i == 159:
                endx += x
                endz += z
            gl_ft.glVertex3f(x, 0, z)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 8 / 80) + posx
            z = math.sin(1 * i * 2 * PI / 8 / 80) + posz
            gl_ft.glVertex3f(x / 1.5, 0, z / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 8 / 80) + posx
            z = math.sin(1 * i * 2 * PI / 8 / 80) + posz
            gl_ft.glVertex3f(-x, 0, -z)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 8 / 80) + posx
            z = math.sin(1 * i * 2 * PI / 8 / 80) + posz
            gl_ft.glVertex3f(-x / 1.5, 0, -z / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(startx, 0.0, startz)
        gl_ft.glVertex3f(startx / 1.5, 0.0, startz / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(-startx, 0.0, startz)
        gl_ft.glVertex3f(-startx / 1.5, 0.0, startz / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(-endx, 0.0, -endz)
        gl_ft.glVertex3f(-endx / 1.5, 0.0, -endz / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(endx, 0.0, endz)
        gl_ft.glVertex3f(endx / 1.5, 0.0, endz / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(200):
            x = math.cos(i * 2 * PI / 100) + posx
            z = math.sin(i * 2 * PI / 100) + posz
            gl_ft.glVertex3f(x / 2, 0, z / 2)
        gl_ft.glEnd()
    elif shape == 6:
        # 6 targetC
        posx, posz = 0, 0
        startx, startz = 0, 0
        endx, endz = 0, 0

        gl_ft.glRotatef(45, 0, 1, 0)

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 8 / 80) + posx
            z = math.sin(1 * i * 2 * PI / 8 / 80) + posz
            if not i:
                startx += x
                startz += z
            elif i == 159:
                endx += x
                endz += z
            gl_ft.glVertex3f(x, 0, z)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 8 / 80) + posx
            z = math.sin(1 * i * 2 * PI / 8 / 80) + posz
            gl_ft.glVertex3f(x / 1.5, 0, z / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 8 / 80) + posx
            z = math.sin(1 * i * 2 * PI / 8 / 80) + posz
            gl_ft.glVertex3f(-x, 0, -z)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 8 / 80) + posx
            z = math.sin(1 * i * 2 * PI / 8 / 80) + posz
            gl_ft.glVertex3f(-x / 1.5, 0, -z / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(startx, 0.0, startz)
        gl_ft.glVertex3f(startx / 1.5, 0.0, startz / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(-startx, 0.0, startz)
        gl_ft.glVertex3f(-startx / 1.5, 0.0, startz / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(-endx, 0.0, -endz)
        gl_ft.glVertex3f(-endx / 1.5, 0.0, -endz / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(endx, 0.0, endz)
        gl_ft.glVertex3f(endx / 1.5, 0.0, endz / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(200):
            x = math.cos(i * 2 * PI / 100) + posx
            z = math.sin(i * 2 * PI / 100) + posz
            gl_ft.glVertex3f(x / 2, 0, z / 2)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(200):
            x = math.cos(i * 2 * PI / 100) + posx
            z = math.sin(i * 2 * PI / 100) + posz
            gl_ft.glVertex3f(x / 0.85, 0, z / 0.85)
        gl_ft.glEnd()
    elif shape == 7:
        # 7 targetD
        posx, posz = 0, 0
        startx, startz = 0, 0
        endx, endz = 0, 0

        gl_ft.glRotatef(45, 0, 1, 0)

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 8 / 80) + posx
            z = math.sin(1 * i * 2 * PI / 8 / 80) + posz
            if not i:
                startx += x
                startz += z
            elif i == 159:
                endx += x
                endz += z
            gl_ft.glVertex3f(x, 0, z)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 8 / 80) + posx
            z = math.sin(1 * i * 2 * PI / 8 / 80) + posz
            gl_ft.glVertex3f(x / 1.5, 0, z / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 8 / 80) + posx
            z = math.sin(1 * i * 2 * PI / 8 / 80) + posz
            gl_ft.glVertex3f(-x, 0, -z)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 8 / 80) + posx
            z = math.sin(1 * i * 2 * PI / 8 / 80) + posz
            gl_ft.glVertex3f(-x / 1.5, 0, -z / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(startx, 0.0, startz)
        gl_ft.glVertex3f(startx + 0.1, 0.0, -startz)
        gl_ft.glVertex3f(startx - 0.181, 0.0, startz - 0.15)
        gl_ft.glVertex3f(startx - 0.44, 0.0, startz)
        gl_ft.glVertex3f(startx / 1.5, 0.0, startz / 0.15)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(-startx, 0.0, startz)
        gl_ft.glVertex3f(-startx - 0.1, 0.0, startz)
        gl_ft.glVertex3f(-startx + 0.181, 0.0, startz + 0.15)
        gl_ft.glVertex3f(-startx + 0.44, 0.0, -startz)
        gl_ft.glVertex3f(-startx / 1.5, 0.0, startz / 0.15)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(endx, 0.0, endz)
        gl_ft.glVertex3f(endx, 0.0, endz + 0.1)
        gl_ft.glVertex3f(endx - 0.16, 0.0, endz - 0.181)
        gl_ft.glVertex3f(endx, 0.0, endz - 0.44)
        gl_ft.glVertex3f(endx / 1.5, 0.0, endz / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        endx = endx - 0.02
        gl_ft.glVertex3f(endx, 0.0, - endz)
        gl_ft.glVertex3f(endx, 0.0, -endz - 0.1)
        gl_ft.glVertex3f(endx + 0.16, 0.0, -endz + 0.181)
        gl_ft.glVertex3f(endx, 0.0, -endz + 0.44)
        gl_ft.glVertex3f(endx / 1.5, 0.0, -endz / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(i * 2 * PI / 80) + posx
            z = math.sin(i * 2 * PI / 80) + posz
            gl_ft.glVertex3f(x / 2, 0, z / 2)
        gl_ft.glEnd()
    elif shape == 8:
        # 8 targetE
        posx, posz = 0, 0
        startx, startz = 0, 0
        endx, endz = 0, 0

        gl_ft.glRotatef(45, 0, 1, 0)

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 8 / 80) + posx
            z = math.sin(1 * i * 2 * PI / 8 / 80) + posz
            if not i:
                startx += x
                startz += z
            elif i == 159:
                endx += x
                endz += z
            gl_ft.glVertex3f(x, 0, z)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 8 / 80) + posx
            z = math.sin(1 * i * 2 * PI / 8 / 80) + posz
            gl_ft.glVertex3f(x / 1.5, 0, z / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 8 / 80) + posx
            z = math.sin(1 * i * 2 * PI / 8 / 80) + posz
            gl_ft.glVertex3f(-x, 0, -z)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 8 / 80) + posx
            z = math.sin(1 * i * 2 * PI / 8 / 80) + posz
            gl_ft.glVertex3f(-x / 1.5, 0, -z / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(startx, 0.0, startz)
        gl_ft.glVertex3f(startx + 0.1, 0.0, -startz)
        gl_ft.glVertex3f(startx - 0.181, 0.0, startz - 0.15)
        gl_ft.glVertex3f(startx - 0.44, 0.0, startz)
        gl_ft.glVertex3f(startx / 1.5, 0.0, startz / 0.15)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(-startx, 0.0, startz)
        gl_ft.glVertex3f(-startx - 0.1, 0.0, startz)
        gl_ft.glVertex3f(-startx + 0.181, 0.0, startz + 0.15)
        gl_ft.glVertex3f(-startx + 0.44, 0.0, -startz)
        gl_ft.glVertex3f(-startx / 1.5, 0.0, startz / 0.15)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(endx, 0.0, endz)
        gl_ft.glVertex3f(endx, 0.0, endz + 0.1)
        gl_ft.glVertex3f(endx - 0.16, 0.0, endz - 0.181)
        gl_ft.glVertex3f(endx, 0.0, endz - 0.44)
        gl_ft.glVertex3f(endx / 1.5, 0.0, endz / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        endx = endx - 0.02
        gl_ft.glVertex3f(endx, 0.0, - endz)
        gl_ft.glVertex3f(endx, 0.0, -endz - 0.1)
        gl_ft.glVertex3f(endx + 0.16, 0.0, -endz + 0.181)
        gl_ft.glVertex3f(endx, 0.0, -endz + 0.44)
        gl_ft.glVertex3f(endx / 1.5, 0.0, -endz / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(i * 2 * PI / 80) + posx
            z = math.sin(i * 2 * PI / 80) + posz
            gl_ft.glVertex3f(x / 1.2, 0, z / 1.2)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(i * 2 * PI / 80) + posx
            z = math.sin(i * 2 * PI / 80) + posz
            gl_ft.glVertex3f(x / 2, 0, z / 2)
        gl_ft.glEnd()
    elif shape == 9:
        # 9 targetF
        posx, posz = 0, 0
        startx, startz = 0, 0
        endx, endz = 0, 0

        gl_ft.glRotatef(45, 0, 1, 0)

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 8 / 80) + posx
            z = math.sin(1 * i * 2 * PI / 8 / 80) + posz
            if not i:
                startx += x
                startz += z
            elif i == 159:
                endx += x
                endz += z
            gl_ft.glVertex3f(x, 0, z)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 8 / 80) + posx
            z = math.sin(1 * i * 2 * PI / 8 / 80) + posz
            gl_ft.glVertex3f(x / 1.5, 0, z / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 8 / 80) + posx
            z = math.sin(1 * i * 2 * PI / 8 / 80) + posz
            gl_ft.glVertex3f(-x, 0, -z)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 8 / 80) + posx
            z = math.sin(1 * i * 2 * PI / 8 / 80) + posz
            gl_ft.glVertex3f(-x / 1.5, 0, -z / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(startx, 0.0, startz)
        gl_ft.glVertex3f(startx + 0.1, 0.0, -startz)
        gl_ft.glVertex3f(startx - 0.181, 0.0, startz - 0.15)
        gl_ft.glVertex3f(startx - 0.44, 0.0, startz)
        gl_ft.glVertex3f(startx / 1.5, 0.0, startz / 0.15)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(-startx, 0.0, startz)
        gl_ft.glVertex3f(-startx - 0.1, 0.0, startz)
        gl_ft.glVertex3f(-startx + 0.181, 0.0, startz + 0.15)
        gl_ft.glVertex3f(-startx + 0.44, 0.0, -startz)
        gl_ft.glVertex3f(-startx / 1.5, 0.0, startz / 0.15)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(endx, 0.0, endz)
        gl_ft.glVertex3f(endx, 0.0, endz + 0.1)
        gl_ft.glVertex3f(endx - 0.16, 0.0, endz - 0.181)
        gl_ft.glVertex3f(endx, 0.0, endz - 0.44)
        gl_ft.glVertex3f(endx / 1.5, 0.0, endz / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        endx = endx - 0.02
        gl_ft.glVertex3f(endx, 0.0, - endz)
        gl_ft.glVertex3f(endx, 0.0, -endz - 0.1)
        gl_ft.glVertex3f(endx + 0.16, 0.0, -endz + 0.181)
        gl_ft.glVertex3f(endx, 0.0, -endz + 0.44)
        gl_ft.glVertex3f(endx / 1.5, 0.0, -endz / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(i * 2 * PI / 80) + posx
            z = math.sin(i * 2 * PI / 80) + posz
            gl_ft.glVertex3f(x / 0.8, 0, z / 0.8)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(i * 2 * PI / 80) + posx
            z = math.sin(i * 2 * PI / 80) + posz
            gl_ft.glVertex3f(x / 2, 0, z / 2)
        gl_ft.glEnd()
    elif shape == 10:
        # 10 full circleone arrow
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(1.771415, 0.0, 3.50177e-07)
        gl_ft.glVertex3f(1.293396, 0.0, 0.364362)
        gl_ft.glVertex3f(1.293396, 0.0, 0.19509)
        gl_ft.glVertex3f(0.980785, 0.0, 0.19509)
        gl_ft.glVertex3f(0.923879, 0.0, 0.382683)
        gl_ft.glVertex3f(0.831469, 0.0, 0.55557)
        gl_ft.glVertex3f(0.707107, 0.0, 0.707107)
        gl_ft.glVertex3f(0.55557, 0.0, 0.83147)
        gl_ft.glVertex3f(0.382683, 0.0, 0.923879)
        gl_ft.glVertex3f(0.19509, 0.0, 0.980785)
        gl_ft.glVertex3f(-1.63913e-07, 0.0, 1.0)
        gl_ft.glVertex3f(-0.19509, 0.0, 0.980785)
        gl_ft.glVertex3f(-0.382683, 0.0, 0.923879)
        gl_ft.glVertex3f(-0.55557, 0.0, 0.831469)
        gl_ft.glVertex3f(-0.707107, 0.0, 0.707106)
        gl_ft.glVertex3f(-0.831469, 0.0, 0.55557)
        gl_ft.glVertex3f(-0.923879, 0.0, 0.382683)
        gl_ft.glVertex3f(-0.980785, 0.0, 0.19509)
        gl_ft.glVertex3f(-0.999999, 0.0, -3.27826e-07)
        gl_ft.glVertex3f(-0.980785, 0.0, -0.195091)
        gl_ft.glVertex3f(-0.923879, 0.0, -0.382683)
        gl_ft.glVertex3f(-0.831469, 0.0, -0.55557)
        gl_ft.glVertex3f(-0.707106, 0.0, -0.707106)
        gl_ft.glVertex3f(-0.555569, 0.0, -0.831469)
        gl_ft.glVertex3f(-0.382683, 0.0, -0.923879)
        gl_ft.glVertex3f(-0.19509, 0.0, -0.980784)
        gl_ft.glVertex3f(4.47035e-07, 0.0, -0.999999)
        gl_ft.glVertex3f(0.195091, 0.0, -0.980784)
        gl_ft.glVertex3f(0.382683, 0.0, -0.923878)
        gl_ft.glVertex3f(0.55557, 0.0, -0.831468)
        gl_ft.glVertex3f(0.707106, 0.0, -0.707106)
        gl_ft.glVertex3f(0.831469, 0.0, -0.555569)
        gl_ft.glVertex3f(0.923879, 0.0, -0.382683)
        gl_ft.glVertex3f(0.980784, 0.0, -0.19509)
        gl_ft.glVertex3f(1.293396, 0.0, -0.19509)
        gl_ft.glVertex3f(1.293396, 0.0, -0.364361)
        gl_ft.glVertex3f(1.771415, 0.0, 3.50177e-07)
        gl_ft.glEnd()
    elif shape == 11:
        # 11 full circle2 arrows
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(3.8742999999999997e-07, 0.0, -0.999999)
        gl_ft.glVertex3f(0.195091, 0.0, -0.980785)
        gl_ft.glVertex3f(0.382683, 0.0, -0.923879)
        gl_ft.glVertex3f(0.55557, 0.0, -0.831469)
        gl_ft.glVertex3f(0.707106, 0.0, -0.707106)
        gl_ft.glVertex3f(0.831469, 0.0, -0.55557)
        gl_ft.glVertex3f(0.923879, 0.0, -0.382683)
        gl_ft.glVertex3f(0.980784, 0.0, -0.19509)
        gl_ft.glVertex3f(1.128127, 0.0, -0.19509)
        gl_ft.glVertex3f(1.128127, 0.0, -0.255385)
        gl_ft.glVertex3f(1.282292, 0.0, 5.1707e-05)
        gl_ft.glVertex3f(1.128127, 0.0, 0.255385)
        gl_ft.glVertex3f(1.128127, 0.0, 0.19509)
        gl_ft.glVertex3f(0.980785, 0.0, 0.19509)
        gl_ft.glVertex3f(0.923879, 0.0, 0.382683)
        gl_ft.glVertex3f(0.831469, 0.0, 0.55557)
        gl_ft.glVertex3f(0.707107, 0.0, 0.707106)
        gl_ft.glVertex3f(0.55557, 0.0, 0.831469)
        gl_ft.glVertex3f(0.382683, 0.0, 0.923879)
        gl_ft.glVertex3f(0.19509, 0.0, 0.980785)
        gl_ft.glVertex3f(-2.23517e-07, 0.0, 0.999999)
        gl_ft.glVertex3f(-0.19509, 0.0, 0.980785)
        gl_ft.glVertex3f(-0.382684, 0.0, 0.923879)
        gl_ft.glVertex3f(-0.55557, 0.0, 0.831469)
        gl_ft.glVertex3f(-0.707107, 0.0, 0.707106)
        gl_ft.glVertex3f(-0.831469, 0.0, 0.555569)
        gl_ft.glVertex3f(-0.923879, 0.0, 0.382683)
        gl_ft.glVertex3f(-0.980785, 0.0, 0.19509)
        gl_ft.glVertex3f(-1.128127, 0.0, 0.19509)
        gl_ft.glVertex3f(-1.128127, 0.0, 0.255385)
        gl_ft.glVertex3f(-1.282292, 0.0, -5.25415e-05)
        gl_ft.glVertex3f(-1.128127, 0.0, -0.255386)
        gl_ft.glVertex3f(-1.128127, 0.0, -0.195091)
        gl_ft.glVertex3f(-0.980785, 0.0, -0.195091)
        gl_ft.glVertex3f(-0.923879, 0.0, -0.382684)
        gl_ft.glVertex3f(-0.831469, 0.0, -0.55557)
        gl_ft.glVertex3f(-0.707106, 0.0, -0.707107)
        gl_ft.glVertex3f(-0.555569, 0.0, -0.831469)
        gl_ft.glVertex3f(-0.382683, 0.0, -0.923879)
        gl_ft.glVertex3f(-0.19509, 0.0, -0.980785)
        gl_ft.glVertex3f(3.8742999999999997e-07, 0.0, -0.999999)
        gl_ft.glEnd()
    elif shape == 12:
        # 12 full circle4 arrows
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(5.25415e-05, 0.0, -1.282292)
        gl_ft.glVertex3f(0.255386, 0.0, -1.128127)
        gl_ft.glVertex3f(0.195091, 0.0, -1.128127)
        gl_ft.glVertex3f(0.195091, 0.0, -0.980785)
        gl_ft.glVertex3f(0.382683, 0.0, -0.923879)
        gl_ft.glVertex3f(0.55557, 0.0, -0.831469)
        gl_ft.glVertex3f(0.707106, 0.0, -0.707106)
        gl_ft.glVertex3f(0.831469, 0.0, -0.55557)
        gl_ft.glVertex3f(0.923879, 0.0, -0.382683)
        gl_ft.glVertex3f(0.980784, 0.0, -0.19509)
        gl_ft.glVertex3f(1.128127, 0.0, -0.19509)
        gl_ft.glVertex3f(1.128127, 0.0, -0.255385)
        gl_ft.glVertex3f(1.282292, 0.0, 5.1707e-05)
        gl_ft.glVertex3f(1.128127, 0.0, 0.255385)
        gl_ft.glVertex3f(1.128127, 0.0, 0.19509)
        gl_ft.glVertex3f(0.980785, 0.0, 0.19509)
        gl_ft.glVertex3f(0.923879, 0.0, 0.382683)
        gl_ft.glVertex3f(0.831469, 0.0, 0.55557)
        gl_ft.glVertex3f(0.707107, 0.0, 0.707106)
        gl_ft.glVertex3f(0.55557, 0.0, 0.831469)
        gl_ft.glVertex3f(0.382683, 0.0, 0.923879)
        gl_ft.glVertex3f(0.19509, 0.0, 0.980785)
        gl_ft.glVertex3f(0.19509, 0.0, 1.128127)
        gl_ft.glVertex3f(0.255385, 0.0, 1.128127)
        gl_ft.glVertex3f(-5.1707e-05, 0.0, 1.282292)
        gl_ft.glVertex3f(-0.255385, 0.0, 1.128127)
        gl_ft.glVertex3f(-0.19509, 0.0, 1.128127)
        gl_ft.glVertex3f(-0.19509, 0.0, 0.980785)
        gl_ft.glVertex3f(-0.382684, 0.0, 0.923879)
        gl_ft.glVertex3f(-0.55557, 0.0, 0.831469)
        gl_ft.glVertex3f(-0.707107, 0.0, 0.707106)
        gl_ft.glVertex3f(-0.831469, 0.0, 0.555569)
        gl_ft.glVertex3f(-0.923879, 0.0, 0.382683)
        gl_ft.glVertex3f(-0.980785, 0.0, 0.19509)
        gl_ft.glVertex3f(-1.128127, 0.0, 0.19509)
        gl_ft.glVertex3f(-1.128127, 0.0, 0.255385)
        gl_ft.glVertex3f(-1.282292, 0.0, -5.25415e-05)
        gl_ft.glVertex3f(-1.128127, 0.0, -0.255386)
        gl_ft.glVertex3f(-1.128127, 0.0, -0.195091)
        gl_ft.glVertex3f(-0.980785, 0.0, -0.195091)
        gl_ft.glVertex3f(-0.923879, 0.0, -0.382684)
        gl_ft.glVertex3f(-0.831469, 0.0, -0.55557)
        gl_ft.glVertex3f(-0.707106, 0.0, -0.707107)
        gl_ft.glVertex3f(-0.555569, 0.0, -0.831469)
        gl_ft.glVertex3f(-0.382683, 0.0, -0.923879)
        gl_ft.glVertex3f(-0.19509, 0.0, -0.980785)
        gl_ft.glVertex3f(-0.19509, 0.0, -1.128127)
        gl_ft.glVertex3f(-0.255385, 0.0, -1.128127)
        gl_ft.glVertex3f(5.25415e-05, 0.0, -1.282292)
        gl_ft.glEnd()
    elif shape == 13:
        # 13 gear
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(-0.156434, 0.0, -0.987689)
        gl_ft.glVertex3f(-0.154815, 0.0, -1.206708)
        gl_ft.glVertex3f(0.154815, 0.0, -1.206708)
        gl_ft.glVertex3f(0.156435, 0.0, -0.987689)
        gl_ft.glVertex3f(0.309017, 0.0, -0.951057)
        gl_ft.glVertex3f(0.453991, 0.0, -0.891007)
        gl_ft.glVertex3f(0.587786, 0.0, -0.809017)
        gl_ft.glVertex3f(0.743801, 0.0, -0.962742)
        gl_ft.glVertex3f(0.962743, 0.0, -0.743801)
        gl_ft.glVertex3f(0.809018, 0.0, -0.587785)
        gl_ft.glVertex3f(0.891007, 0.0, -0.453991)
        gl_ft.glVertex3f(0.951057, 0.0, -0.309017)
        gl_ft.glVertex3f(0.987689, 0.0, -0.156434)
        gl_ft.glVertex3f(1.206708, 0.0, -0.154814)
        gl_ft.glVertex3f(1.206708, 0.0, 0.154815)
        gl_ft.glVertex3f(0.987688, 0.0, 0.156434)
        gl_ft.glVertex3f(0.951057, 0.0, 0.309017)
        gl_ft.glVertex3f(0.891007, 0.0, 0.453991)
        gl_ft.glVertex3f(0.809017, 0.0, 0.587785)
        gl_ft.glVertex3f(0.962742, 0.0, 0.743801)
        gl_ft.glVertex3f(0.743801, 0.0, 0.962742)
        gl_ft.glVertex3f(0.587785, 0.0, 0.809017)
        gl_ft.glVertex3f(0.453991, 0.0, 0.891007)
        gl_ft.glVertex3f(0.309017, 0.0, 0.951057)
        gl_ft.glVertex3f(0.156434, 0.0, 0.987689)
        gl_ft.glVertex3f(0.154815, 0.0, 1.206708)
        gl_ft.glVertex3f(-0.154815, 0.0, 1.206708)
        gl_ft.glVertex3f(-0.156435, 0.0, 0.987689)
        gl_ft.glVertex3f(-0.309017, 0.0, 0.951057)
        gl_ft.glVertex3f(-0.453991, 0.0, 0.891007)
        gl_ft.glVertex3f(-0.587786, 0.0, 0.809017)
        gl_ft.glVertex3f(-0.743801, 0.0, 0.962742)
        gl_ft.glVertex3f(-0.962742, 0.0, 0.743801)
        gl_ft.glVertex3f(-0.809017, 0.0, 0.587785)
        gl_ft.glVertex3f(-0.891007, 0.0, 0.45399)
        gl_ft.glVertex3f(-0.951057, 0.0, 0.309017)
        gl_ft.glVertex3f(-0.987689, 0.0, 0.156434)
        gl_ft.glVertex3f(-1.206708, 0.0, 0.154815)
        gl_ft.glVertex3f(-1.206708, 0.0, -0.154815)
        gl_ft.glVertex3f(-0.987689, 0.0, -0.156435)
        gl_ft.glVertex3f(-0.951057, 0.0, -0.309017)
        gl_ft.glVertex3f(-0.891007, 0.0, -0.453991)
        gl_ft.glVertex3f(-0.809017, 0.0, -0.587786)
        gl_ft.glVertex3f(-0.962742, 0.0, -0.743801)
        gl_ft.glVertex3f(-0.743801, 0.0, -0.962742)
        gl_ft.glVertex3f(-0.587785, 0.0, -0.809018)
        gl_ft.glVertex3f(-0.453991, 0.0, -0.891007)
        gl_ft.glVertex3f(-0.309017, 0.0, -0.951057)
        gl_ft.glVertex3f(-0.156434, 0.0, -0.987689)
        gl_ft.glEnd()
    elif shape == 14:
        # 14 sphere
        posx, posy, posz = 0, 0, 0
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(256):
            y = math.cos(i * 2 * PI / 128) + posy
            z = math.sin(i * 2 * PI / 128) + posz
            gl_ft.glVertex3f(0, y, z)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(256):
            x = math.cos(i * 2 * PI / 128) + posx
            z = math.sin(i * 2 * PI / 128) + posz
            gl_ft.glVertex3f(x, 0, z)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(256):
            x = math.cos(i * 2 * PI / 128) + posx
            y = math.sin(i * 2 * PI / 128) + posy
            gl_ft.glVertex3f(x, y, 0)
        gl_ft.glEnd()
    elif shape == 15:
        # 15 arc full circle
        posx = 0
        posz = 0
        startx, startz = 0, 0
        endx, endz = 0, 0

        cposx = list()
        cposz = list()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(180):
            x = math.cos(1 * i * 2 * PI / 4 / 89.5) + posx
            z = math.sin(1 * i * 2 * PI / 4 / 89.5) + posz
            if not i:
                startx += x
                startz += z
            if i == 179:
                endx += x
                endz += z
            if i == 90:
                cposx.append(x * 1.25)
                cposz.append(z * 1.25)
                gl_ft.glVertex3f(x, 0.0, z)
                gl_ft.glVertex3f(x * 1.25, 0.0, z * 1.25)
            gl_ft.glVertex3f(x, 0, z)
        gl_ft.glEnd()

        for x, z in zip(cposx, cposz):
            gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
            for i in range(100):
                cx = math.cos(i * 2 * PI / 50) + (x * 4.8)
                cz = math.sin(i * 2 * PI / 50) + (z * 4.8)
                gl_ft.glVertex3f(cx * 0.25, 0, cz * 0.25)
            gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(180):
            x = math.cos(1 * i * 2 * PI / 4 / 89.5) + posx
            z = math.sin(1 * i * 2 * PI / 4 / 89.5) + posz
            gl_ft.glVertex3f(x / 1.5, 0, z / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(startx, 0.0, startz)
        gl_ft.glVertex3f(startx / 1.5, 0.0, startz / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(endx, 0.0, endz)
        gl_ft.glVertex3f(endx / 1.5, 0.0, endz / 1.5)
        gl_ft.glEnd()
    elif shape == 16:
        # 16 semiCircle
        posx = 0
        posz = 0
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(180):
            x = math.cos(1 * i * 2 * PI / 4 / 89.5) + posx
            z = math.sin(1 * i * 2 * PI / 4 / 89.5) + posz
            gl_ft.glVertex3f(x, 0, z)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(-1, 0.0, 0)
        gl_ft.glVertex3f(1, 0.0, 0)
        gl_ft.glEnd()
    elif shape == 17:
        # 17 bowA
        posx = 0
        posz = 0
        startx, startz = 0, 0
        endx, endz = 0, 0

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(180):
            x = math.cos(1 * i * 2 * PI / 4 / 89.5) + posx
            z = math.sin(1 * i * 2 * PI / 4 / 89.5) + posz
            if not i:
                startx += x
                startz += z
            if i == 179:
                endx += x
                endz += z
            gl_ft.glVertex3f(x, 0, z)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(180):
            x = math.cos(1 * i * 2 * PI / 4 / 89.5) + posx
            z = math.sin(1 * i * 2 * PI / 4 / 89.5) + posz
            gl_ft.glVertex3f(x / 1.5, 0, z / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(startx, 0.0, startz)
        gl_ft.glVertex3f(startx / 1.5, 0.0, startz / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(endx, 0.0, endz)
        gl_ft.glVertex3f(endx / 1.5, 0.0, endz / 1.5)
        gl_ft.glEnd()
    elif shape == 18:
        posx = 0
        posz = 0
        startx, startz = 0, 0
        endx, endz = 0, 0

        # 18 bowB
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(180):
            x = math.cos(1 * i * 2 * PI / 4 / 89.5) + posx
            z = math.sin(1 * i * 2 * PI / 4 / 89.5) + posz
            if not i:
                startx += x
                startz += z
            if i == 179:
                endx += x
                endz += z
            gl_ft.glVertex3f(x, 0, z)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(180):
            x = math.cos(1 * i * 2 * PI / 4 / 89.5) + posx
            z = math.sin(1 * i * 2 * PI / 4 / 89.5) + posz
            gl_ft.glVertex3f(x / 1.5, 0, z / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(startx, 0.0, startz)
        gl_ft.glVertex3f(startx / 1.5, 0.0, startz / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(endx, 0.0, endz)
        gl_ft.glVertex3f(endx / 1.5, 0.0, endz / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(200):
            x = math.cos(i * 2 * PI / 100) + posx
            z = math.sin(i * 2 * PI / 100) + posz
            gl_ft.glVertex3f(x / 2, 0, z / 2)
        gl_ft.glEnd()
    elif shape == 19:
        # 19 arc multi circles
        posx = 0
        posz = 0
        startx, startz = 0, 0
        endx, endz = 0, 0

        amount = range(180)
        num = amount[0::45]
        num.append(179)

        cposx = list()
        cposz = list()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in amount:
            x = math.cos(1 * i * 2 * PI / 4 / 89.5) + posx
            z = math.sin(1 * i * 2 * PI / 4 / 89.5) + posz
            if not i:
                startx += x
                startz += z
            if i == 179:
                endx += x
                endz += z
            for j in num:
                if i == j:
                    cposx.append(x * 1.25)
                    cposz.append(z * 1.25)
                    gl_ft.glVertex3f(x, 0.0, z)
                    gl_ft.glVertex3f(x * 1.25, 0.0, z * 1.25)
            gl_ft.glVertex3f(x, 0, z)
        gl_ft.glEnd()

        for x, z in zip(cposx, cposz):
            gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
            for i in range(100):
                cx = math.cos(i * 2 * PI / 50) + (x * 4.8)
                cz = math.sin(i * 2 * PI / 50) + (z * 4.8)
                gl_ft.glVertex3f(cx * 0.25, 0, cz * 0.25)
            gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(180):
            x = math.cos(1 * i * 2 * PI / 4 / 89.5) + posx
            z = math.sin(1 * i * 2 * PI / 4 / 89.5) + posz
            gl_ft.glVertex3f(x / 1.5, 0, z / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(startx, 0.0, startz)
        gl_ft.glVertex3f(startx / 1.5, 0.0, startz / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(endx, 0.0, endz)
        gl_ft.glVertex3f(endx / 1.5, 0.0, endz / 1.5)
        gl_ft.glEnd()
    elif shape == 20:
        # 20 full circlemulti line circles
        posx = 0
        posz = 0
        startx, startz = 0, 0
        endx, endz = 0, 0

        amount = range(180)
        num = amount[0::20]
        num.append(179)

        cposx = list()
        cposz = list()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in amount:
            x = math.cos(1 * i * 2 * PI / 89.5) + posx
            z = math.sin(1 * i * 2 * PI / 89.5) + posz
            if not i:
                startx += x
                startz += z
            if i == 179:
                endx += x
                endz += z
            for j in num:
                if i == j:
                    cposx.append(x * 1.25)
                    cposz.append(z * 1.25)
                    gl_ft.glVertex3f(x, 0.0, z)
                    gl_ft.glVertex3f(x * 1.25, 0.0, z * 1.25)
            gl_ft.glVertex3f(x, 0, z)
        gl_ft.glEnd()

        for x, z in zip(cposx, cposz):
            gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
            for i in range(100):
                cx = math.cos(i * 2 * PI / 50) + (x * 4.8)
                cz = math.sin(i * 2 * PI / 50) + (z * 4.8)
                gl_ft.glVertex3f(cx * 0.25, 0, cz * 0.25)
            gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(180):
            x = math.cos(1 * i * 2 * PI / 4 / 89.5) + posx
            z = math.sin(1 * i * 2 * PI / 4 / 89.5) + posz
            gl_ft.glVertex3f(x / 1.5, 0, z / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(startx, 0.0, startz)
        gl_ft.glVertex3f(startx / 1.5, 0.0, startz / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(endx, 0.0, endz)
        gl_ft.glVertex3f(endx / 1.5, 0.0, endz / 1.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(-0.666, 0.0, 0)
        gl_ft.glVertex3f(-1, 0.0, 0)
        gl_ft.glEnd()
    elif shape == 21:
        # 21 semicircleline full circle
        posx = 0
        posz = 0

        cposx = list()
        cposz = list()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(180):
            x = math.cos(1 * i * 2 * PI / 4 / 89.5) + posx
            z = math.sin(1 * i * 2 * PI / 4 / 89.5) + posz
            if i == 90:
                cposx.append(x * 1.25)
                cposz.append(z * 1.25)
                gl_ft.glVertex3f(x, 0.0, z)
                gl_ft.glVertex3f(x * 1.25, 0.0, z * 1.25)
            gl_ft.glVertex3f(x, 0, z)
        gl_ft.glEnd()

        for x, z in zip(cposx, cposz):
            gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
            for i in range(100):
                cx = math.cos(i * 2 * PI / 50) + (x * 2.25)
                cz = math.sin(i * 2 * PI / 50) + (z * 2.25)
                gl_ft.glVertex3f(cx * 0.69, 0, cz * 0.69)
            gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(-1, 0.0, 0)
        gl_ft.glVertex3f(1, 0.0, 0)
        gl_ft.glEnd()
    elif shape == 22:
        # 22 full circleline semi circle
        posx = 0
        posz = 0

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(180):
            x = math.cos(1 * i * 2 * PI / 4 / 89.5) + posx
            z = math.sin(1 * i * 2 * PI / 4 / 89.5) + posz + 2
            gl_ft.glVertex3f(-x, 0, -z)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(100):
            cx = math.cos(i * 2 * PI / 50)
            cz = math.sin(i * 2 * PI / 50)
            gl_ft.glVertex3f(cx, 0, cz)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(-1, 0.0, -2)
        gl_ft.glVertex3f(1, 0.0, -2)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(0, 0.0, -2)
        gl_ft.glVertex3f(0, 0.0, -1)
        gl_ft.glEnd()
    elif shape == 23:
        # 23 circleline circle
        posx = 0
        posz = 0

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(180):
            x = math.cos(1 * i * 2 * PI / 89.5) + posx
            z = math.sin(1 * i * 2 * PI / 89.5) + posz
            gl_ft.glVertex3f(x - 2, 0, z)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(180):
            x = math.cos(1 * i * 2 * PI / 89.5) + posx
            z = math.sin(1 * i * 2 * PI / 89.5) + posz
            gl_ft.glVertex3f(x + 2, 0, z)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(-1, 0.0, 0)
        gl_ft.glVertex3f(1, 0.0, 0)
        gl_ft.glEnd()
    elif shape == 24:
        # 24 face to face circle
        posx = 0
        posy = 0

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(180):
            y = math.cos(1 * i * 2 * PI / 89.5) + posx
            z = math.sin(1 * i * 2 * PI / 89.5) + posy
            gl_ft.glVertex3f(-1, y, z)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(180):
            y = math.cos(1 * i * 2 * PI / 89.5) + posx
            z = math.sin(1 * i * 2 * PI / 89.5) + posy
            gl_ft.glVertex3f(1, y, z)
        gl_ft.glEnd()
    elif shape == 25:
        # 25 single arrow
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(2.0, 0.0, 0.0)
        gl_ft.glVertex3f(1.0, 0.0, -0.569349)
        gl_ft.glVertex3f(1.0, 0.0, -0.366071)
        gl_ft.glVertex3f(-1.0, 0.0, -0.366071)
        gl_ft.glVertex3f(-1.0, 0.0, 0.366071)
        gl_ft.glVertex3f(1.0, 0.0, 0.366071)
        gl_ft.glVertex3f(1.0, 0.0, 0.569349)
        gl_ft.glVertex3f(2.0, 0.0, -1.4007099999999998e-06)
        gl_ft.glEnd()
    elif shape == 26:
        # 26 double arrow
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(2.0, 0.0, 0.0)
        gl_ft.glVertex3f(1.0, 0.0, 0.569349)
        gl_ft.glVertex3f(1.0, 0.0, 0.366071)
        gl_ft.glVertex3f(-1.0, 0.0, 0.366071)
        gl_ft.glVertex3f(-1.0, 0.0, 0.569349)
        gl_ft.glVertex3f(-2.0, 0.0, 0.0)
        gl_ft.glVertex3f(-1.0, 0.0, -0.569349)
        gl_ft.glVertex3f(-1.0, 0.0, -0.366071)
        gl_ft.glVertex3f(1.0, 0.0, -0.366071)
        gl_ft.glVertex3f(1.0, 0.0, -0.569349)
        gl_ft.glVertex3f(2.0, 0.0, 0.0)
        gl_ft.glEnd()
    elif shape == 27:
        # 27 arrow line arrow
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(0.0, 0.0, -1.0)
        gl_ft.glVertex3f(-1.0, 0.0, -1.0)
        gl_ft.glVertex3f(0.0, 0.0, -2.0)
        gl_ft.glVertex3f(1.0, 0.0, -1.0)
        gl_ft.glVertex3f(0.0, 0.0, -1.0)
        gl_ft.glVertex3f(0.0, 0.0, 1.0)
        gl_ft.glVertex3f(-1.0, 0.0, 1.0)
        gl_ft.glVertex3f(0.0, 0.0, 2.0)
        gl_ft.glVertex3f(1.0, 0.0, 1.0)
        gl_ft.glVertex3f(0.0, 0.0, 1.0)
        gl_ft.glEnd()
    elif shape == 28:
        # 28 cross 1D
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(0.0, 0.0, 1.0)
        gl_ft.glVertex3f(-0.25, 0.0, 0.75)
        gl_ft.glVertex3f(-0.15, 0.0, 0.75)
        gl_ft.glVertex3f(-0.15, 0.0, 0.25)
        gl_ft.glVertex3f(-0.25, 0.0, 0.15)
        gl_ft.glVertex3f(-0.75, 0.0, 0.15)
        gl_ft.glVertex3f(-0.75, 0.0, 0.25)
        gl_ft.glVertex3f(-1.0, 0.0, 4.4408920985e-16)
        gl_ft.glVertex3f(-0.75, 0.0, -0.25)
        gl_ft.glVertex3f(-0.75, 0.0, -0.15)
        gl_ft.glVertex3f(-0.25, 0.0, -0.15)
        gl_ft.glVertex3f(-0.15, 0.0, -0.25)
        gl_ft.glVertex3f(-0.15, 0.0, -0.75)
        gl_ft.glVertex3f(-0.25, 0.0, -0.75)
        gl_ft.glVertex3f(0.0, 0.0, -1.0)
        gl_ft.glVertex3f(0.25, 0.0, -0.75)
        gl_ft.glVertex3f(0.15, 0.0, -0.75)
        gl_ft.glVertex3f(0.15, 0.0, -0.25)
        gl_ft.glVertex3f(0.25, 0.0, -0.15)
        gl_ft.glVertex3f(0.75, 0.0, -0.15)
        gl_ft.glVertex3f(0.75, 0.0, -0.25)
        gl_ft.glVertex3f(1.0, 0.0, -4.4408920985e-16)
        gl_ft.glVertex3f(0.75, 0.0, 0.25)
        gl_ft.glVertex3f(0.75, 0.0, 0.15)
        gl_ft.glVertex3f(0.25, 0.0, 0.15)
        gl_ft.glVertex3f(0.15, 0.0, 0.25)
        gl_ft.glVertex3f(0.15, 0.0, 0.75)
        gl_ft.glVertex3f(0.25, 0.0, 0.75)
        gl_ft.glVertex3f(0.0, 0.0, 1.0)
        gl_ft.glEnd()
    elif shape == 29:
        # 29 cross 2D
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(0.0, 0.0, 1.0)
        gl_ft.glVertex3f(-0.25, 0.0, 0.75)
        gl_ft.glVertex3f(-0.15, 0.0, 0.75)
        gl_ft.glVertex3f(-0.15, 0.0, 0.25)
        gl_ft.glVertex3f(-0.25, 0.0, 0.15)
        gl_ft.glVertex3f(-0.75, 0.0, 0.15)
        gl_ft.glVertex3f(-0.75, 0.0, 0.25)
        gl_ft.glVertex3f(-1.0, 0.0, 4.4408920985e-16)
        gl_ft.glVertex3f(-0.75, 0.0, -0.25)
        gl_ft.glVertex3f(-0.75, 0.0, -0.15)
        gl_ft.glVertex3f(-0.25, 0.0, -0.15)
        gl_ft.glVertex3f(-0.15, 0.0, -0.25)
        gl_ft.glVertex3f(-0.15, 0.0, -0.75)
        gl_ft.glVertex3f(-0.25, 0.0, -0.75)
        gl_ft.glVertex3f(0.0, 0.0, -1.0)
        gl_ft.glVertex3f(0.25, 0.0, -0.75)
        gl_ft.glVertex3f(0.15, 0.0, -0.75)
        gl_ft.glVertex3f(0.15, 0.0, -0.25)
        gl_ft.glVertex3f(0.25, 0.0, -0.15)
        gl_ft.glVertex3f(0.75, 0.0, -0.15)
        gl_ft.glVertex3f(0.75, 0.0, -0.25)
        gl_ft.glVertex3f(1.0, 0.0, -4.4408920985e-16)
        gl_ft.glVertex3f(0.75, 0.0, 0.25)
        gl_ft.glVertex3f(0.75, 0.0, 0.15)
        gl_ft.glVertex3f(0.25, 0.0, 0.15)
        gl_ft.glVertex3f(0.15, 0.0, 0.25)
        gl_ft.glVertex3f(0.15, 0.0, 0.75)
        gl_ft.glVertex3f(0.25, 0.0, 0.75)
        gl_ft.glVertex3f(0.0, 0.0, 1.0)
        gl_ft.glEnd()
        gl_ft.glRotatef(90, 1, 0, 0)
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(0.0, 0.0, 1.0)
        gl_ft.glVertex3f(-0.25, 0.0, 0.75)
        gl_ft.glVertex3f(-0.15, 0.0, 0.75)
        gl_ft.glVertex3f(-0.15, 0.0, 0.25)
        gl_ft.glVertex3f(-0.25, 0.0, 0.15)
        gl_ft.glVertex3f(-0.75, 0.0, 0.15)
        gl_ft.glVertex3f(-0.75, 0.0, 0.25)
        gl_ft.glVertex3f(-1.0, 0.0, 4.4408920985e-16)
        gl_ft.glVertex3f(-0.75, 0.0, -0.25)
        gl_ft.glVertex3f(-0.75, 0.0, -0.15)
        gl_ft.glVertex3f(-0.25, 0.0, -0.15)
        gl_ft.glVertex3f(-0.15, 0.0, -0.25)
        gl_ft.glVertex3f(-0.15, 0.0, -0.75)
        gl_ft.glVertex3f(-0.25, 0.0, -0.75)
        gl_ft.glVertex3f(0.0, 0.0, -1.0)
        gl_ft.glVertex3f(0.25, 0.0, -0.75)
        gl_ft.glVertex3f(0.15, 0.0, -0.75)
        gl_ft.glVertex3f(0.15, 0.0, -0.25)
        gl_ft.glVertex3f(0.25, 0.0, -0.15)
        gl_ft.glVertex3f(0.75, 0.0, -0.15)
        gl_ft.glVertex3f(0.75, 0.0, -0.25)
        gl_ft.glVertex3f(1.0, 0.0, -4.4408920985e-16)
        gl_ft.glVertex3f(0.75, 0.0, 0.25)
        gl_ft.glVertex3f(0.75, 0.0, 0.15)
        gl_ft.glVertex3f(0.25, 0.0, 0.15)
        gl_ft.glVertex3f(0.15, 0.0, 0.25)
        gl_ft.glVertex3f(0.15, 0.0, 0.75)
        gl_ft.glVertex3f(0.25, 0.0, 0.75)
        gl_ft.glVertex3f(0.0, 0.0, 1.0)
        gl_ft.glEnd()
    elif shape == 30:
        # 30 cross 3D
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(0.0, 0.0, 1.0)
        gl_ft.glVertex3f(-0.25, 0.0, 0.75)
        gl_ft.glVertex3f(-0.15, 0.0, 0.75)
        gl_ft.glVertex3f(-0.15, 0.0, 0.25)
        gl_ft.glVertex3f(-0.25, 0.0, 0.15)
        gl_ft.glVertex3f(-0.75, 0.0, 0.15)
        gl_ft.glVertex3f(-0.75, 0.0, 0.25)
        gl_ft.glVertex3f(-1.0, 0.0, 4.4408920985e-16)
        gl_ft.glVertex3f(-0.75, 0.0, -0.25)
        gl_ft.glVertex3f(-0.75, 0.0, -0.15)
        gl_ft.glVertex3f(-0.25, 0.0, -0.15)
        gl_ft.glVertex3f(-0.15, 0.0, -0.25)
        gl_ft.glVertex3f(-0.15, 0.0, -0.75)
        gl_ft.glVertex3f(-0.25, 0.0, -0.75)
        gl_ft.glVertex3f(0.0, 0.0, -1.0)
        gl_ft.glVertex3f(0.25, 0.0, -0.75)
        gl_ft.glVertex3f(0.15, 0.0, -0.75)
        gl_ft.glVertex3f(0.15, 0.0, -0.25)
        gl_ft.glVertex3f(0.25, 0.0, -0.15)
        gl_ft.glVertex3f(0.75, 0.0, -0.15)
        gl_ft.glVertex3f(0.75, 0.0, -0.25)
        gl_ft.glVertex3f(1.0, 0.0, -4.4408920985e-16)
        gl_ft.glVertex3f(0.75, 0.0, 0.25)
        gl_ft.glVertex3f(0.75, 0.0, 0.15)
        gl_ft.glVertex3f(0.25, 0.0, 0.15)
        gl_ft.glVertex3f(0.15, 0.0, 0.25)
        gl_ft.glVertex3f(0.15, 0.0, 0.75)
        gl_ft.glVertex3f(0.25, 0.0, 0.75)
        gl_ft.glVertex3f(0.0, 0.0, 1.0)
        gl_ft.glEnd()
        gl_ft.glRotatef(90, 1, 0, 0)
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(0.0, 0.0, 1.0)
        gl_ft.glVertex3f(-0.25, 0.0, 0.75)
        gl_ft.glVertex3f(-0.15, 0.0, 0.75)
        gl_ft.glVertex3f(-0.15, 0.0, 0.25)
        gl_ft.glVertex3f(-0.25, 0.0, 0.15)
        gl_ft.glVertex3f(-0.75, 0.0, 0.15)
        gl_ft.glVertex3f(-0.75, 0.0, 0.25)
        gl_ft.glVertex3f(-1.0, 0.0, 4.4408920985e-16)
        gl_ft.glVertex3f(-0.75, 0.0, -0.25)
        gl_ft.glVertex3f(-0.75, 0.0, -0.15)
        gl_ft.glVertex3f(-0.25, 0.0, -0.15)
        gl_ft.glVertex3f(-0.15, 0.0, -0.25)
        gl_ft.glVertex3f(-0.15, 0.0, -0.75)
        gl_ft.glVertex3f(-0.25, 0.0, -0.75)
        gl_ft.glVertex3f(0.0, 0.0, -1.0)
        gl_ft.glVertex3f(0.25, 0.0, -0.75)
        gl_ft.glVertex3f(0.15, 0.0, -0.75)
        gl_ft.glVertex3f(0.15, 0.0, -0.25)
        gl_ft.glVertex3f(0.25, 0.0, -0.15)
        gl_ft.glVertex3f(0.75, 0.0, -0.15)
        gl_ft.glVertex3f(0.75, 0.0, -0.25)
        gl_ft.glVertex3f(1.0, 0.0, -4.4408920985e-16)
        gl_ft.glVertex3f(0.75, 0.0, 0.25)
        gl_ft.glVertex3f(0.75, 0.0, 0.15)
        gl_ft.glVertex3f(0.25, 0.0, 0.15)
        gl_ft.glVertex3f(0.15, 0.0, 0.25)
        gl_ft.glVertex3f(0.15, 0.0, 0.75)
        gl_ft.glVertex3f(0.25, 0.0, 0.75)
        gl_ft.glVertex3f(0.0, 0.0, 1.0)
        gl_ft.glEnd()
        gl_ft.glRotatef(90, 0, 0, 1)
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(0.0, 0.0, 1.0)
        gl_ft.glVertex3f(-0.25, 0.0, 0.75)
        gl_ft.glVertex3f(-0.15, 0.0, 0.75)
        gl_ft.glVertex3f(-0.15, 0.0, 0.25)
        gl_ft.glVertex3f(-0.25, 0.0, 0.15)
        gl_ft.glVertex3f(-0.75, 0.0, 0.15)
        gl_ft.glVertex3f(-0.75, 0.0, 0.25)
        gl_ft.glVertex3f(-1.0, 0.0, 4.4408920985e-16)
        gl_ft.glVertex3f(-0.75, 0.0, -0.25)
        gl_ft.glVertex3f(-0.75, 0.0, -0.15)
        gl_ft.glVertex3f(-0.25, 0.0, -0.15)
        gl_ft.glVertex3f(-0.15, 0.0, -0.25)
        gl_ft.glVertex3f(-0.15, 0.0, -0.75)
        gl_ft.glVertex3f(-0.25, 0.0, -0.75)
        gl_ft.glVertex3f(0.0, 0.0, -1.0)
        gl_ft.glVertex3f(0.25, 0.0, -0.75)
        gl_ft.glVertex3f(0.15, 0.0, -0.75)
        gl_ft.glVertex3f(0.15, 0.0, -0.25)
        gl_ft.glVertex3f(0.25, 0.0, -0.15)
        gl_ft.glVertex3f(0.75, 0.0, -0.15)
        gl_ft.glVertex3f(0.75, 0.0, -0.25)
        gl_ft.glVertex3f(1.0, 0.0, -4.4408920985e-16)
        gl_ft.glVertex3f(0.75, 0.0, 0.25)
        gl_ft.glVertex3f(0.75, 0.0, 0.15)
        gl_ft.glVertex3f(0.25, 0.0, 0.15)
        gl_ft.glVertex3f(0.15, 0.0, 0.25)
        gl_ft.glVertex3f(0.15, 0.0, 0.75)
        gl_ft.glVertex3f(0.25, 0.0, 0.75)
        gl_ft.glVertex3f(0.0, 0.0, 1.0)
        gl_ft.glEnd()
    elif shape == 31:
        # 31 thin and large arrow tight
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(0.0, 0.0, -0.25)
        gl_ft.glVertex3f(-1.0, 0.0, -0.75)
        gl_ft.glVertex3f(-1.0, 0.0, -1.0)
        gl_ft.glVertex3f(0.0, 0.0, -0.5)
        gl_ft.glVertex3f(1.0, 0.0, -1.0)
        gl_ft.glVertex3f(1.0, 0.0, -0.75)
        gl_ft.glVertex3f(0.0, 0.0, -0.25)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(0.0, 0.0, 1)
        gl_ft.glVertex3f(-0.5, 0.0, 0.75)
        gl_ft.glVertex3f(-1.0, 0.0, -0.5)
        gl_ft.glVertex3f(0.0, 0.0, 0.0)
        gl_ft.glVertex3f(1.0, 0.0, -0.5)
        gl_ft.glVertex3f(0.5, 0.0, 0.75)
        gl_ft.glVertex3f(0.0, 0.0, 1)
        gl_ft.glEnd()
    elif shape == 32:
        # 32 thin and large arrow tight plus frame
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(0.0, 0.0, -0.25)
        gl_ft.glVertex3f(-1.0, 0.0, -0.75)
        gl_ft.glVertex3f(-1.1, 0.0, -1.0)
        gl_ft.glVertex3f(0.0, 0.0, -0.5)
        gl_ft.glVertex3f(1.1, 0.0, -1.0)
        gl_ft.glVertex3f(1.0, 0.0, -0.75)
        gl_ft.glVertex3f(0.0, 0.0, -0.25)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(0.0, 0.0, 1)
        gl_ft.glVertex3f(-0.5, 0.0, 0.75)
        gl_ft.glVertex3f(-1.0, 0.0, -0.5)
        gl_ft.glVertex3f(0.0, 0.0, 0.0)
        gl_ft.glVertex3f(1.0, 0.0, -0.5)
        gl_ft.glVertex3f(0.5, 0.0, 0.75)
        gl_ft.glVertex3f(0.0, 0.0, 1)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(0.0, 0.0, 1.25)
        gl_ft.glVertex3f(-1, 0.0, 0.625)
        gl_ft.glVertex3f(-1.3, 0.0, -1.25)
        gl_ft.glVertex3f(1.3, 0.0, -1.25)
        gl_ft.glVertex3f(1, 0.0, 0.625)
        gl_ft.glVertex3f(0.0, 0.0, 1.25)
        gl_ft.glEnd()
    elif shape == 33:
        # 33 thin and large arrow bright
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(0.0, 0.0, -0.25)
        gl_ft.glVertex3f(-1.0, 0.0, -0.75)
        gl_ft.glVertex3f(-1.0, 0.0, -1.0)
        gl_ft.glVertex3f(0.0, 0.0, -0.5)
        gl_ft.glVertex3f(1.0, 0.0, -1.0)
        gl_ft.glVertex3f(1.0, 0.0, -0.75)
        gl_ft.glVertex3f(0.0, 0.0, -0.25)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(0.0, 0.0, 1)
        gl_ft.glVertex3f(-1, 0.0, 0.5)
        gl_ft.glVertex3f(-1.0, 0.0, -0.5)
        gl_ft.glVertex3f(0.0, 0.0, 0.0)
        gl_ft.glVertex3f(1.0, 0.0, -0.5)
        gl_ft.glVertex3f(1, 0.0, 0.5)
        gl_ft.glVertex3f(0.0, 0.0, 1)
        gl_ft.glEnd()
    elif shape == 34:
        # 34 thin and large arrow bright plus frame
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(0.0, 0.0, -0.25)
        gl_ft.glVertex3f(-1.0, 0.0, -0.75)
        gl_ft.glVertex3f(-1.0, 0.0, -1.0)
        gl_ft.glVertex3f(0.0, 0.0, -0.5)
        gl_ft.glVertex3f(1.0, 0.0, -1.0)
        gl_ft.glVertex3f(1.0, 0.0, -0.75)
        gl_ft.glVertex3f(0.0, 0.0, -0.25)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(0.0, 0.0, 1)
        gl_ft.glVertex3f(-1, 0.0, 0.5)
        gl_ft.glVertex3f(-1.0, 0.0, -0.5)
        gl_ft.glVertex3f(0.0, 0.0, 0.0)
        gl_ft.glVertex3f(1.0, 0.0, -0.5)
        gl_ft.glVertex3f(1, 0.0, 0.5)
        gl_ft.glVertex3f(0.0, 0.0, 1)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(0.0, 0.0, 1.25)
        gl_ft.glVertex3f(-1.25, 0.0, 0.625)
        gl_ft.glVertex3f(-1.25, 0.0, -1.25)
        gl_ft.glVertex3f(1.25, 0.0, -1.25)
        gl_ft.glVertex3f(1.25, 0.0, 0.625)
        gl_ft.glVertex3f(0.0, 0.0, 1.25)
        gl_ft.glEnd()
    elif shape == 35:
        # 35 foot
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(8.940696716308594e-08, 0.0, 3.0274547934532166)
        gl_ft.glVertex3f(0.1545080542564392, 0.0, 3.010420501232147)
        gl_ft.glVertex3f(0.2410280704498291, 0.0, 2.9755284190177917)
        gl_ft.glVertex3f(0.4468093812465668, 0.0, 2.8275105357170105)
        gl_ft.glVertex3f(0.5831533074378967, 0.0, 2.6794928908348083)
        gl_ft.glVertex3f(0.7148623466491699, 0.0, 2.47300523519516)
        gl_ft.glVertex3f(0.791209876537323, 0.0, 2.266518294811249)
        gl_ft.glVertex3f(0.8661590814590454, 0.0, 1.9359846711158752)
        gl_ft.glVertex3f(0.8944776058197021, 0.0, 1.6054505705833435)
        gl_ft.glVertex3f(0.8511085510253906, 0.0, 0.9973527193069458)
        gl_ft.glVertex3f(0.6504331231117249, 0.0, -0.056056540459394455)
        gl_ft.glVertex3f(0.5933024883270264, 0.0, -1.5364721417427063)
        gl_ft.glVertex3f(0.5096197128295898, 0.0, -1.6882659792900085)
        gl_ft.glVertex3f(0.3641579747200012, 0.0, -1.8219407200813293)
        gl_ft.glVertex3f(0.19144919514656067, 0.0, -1.9245763421058655)
        gl_ft.glVertex3f(7.385515843338908e-08, 0.0, -1.9723008275032043)
        gl_ft.glVertex3f(-0.19144901633262634, 0.0, -1.924576222896576)
        gl_ft.glVertex3f(-0.36415767669677734, 0.0, -1.8219406008720398)
        gl_ft.glVertex3f(-0.509619414806366, 0.0, -1.6882659792900085)
        gl_ft.glVertex3f(-0.5933021306991577, 0.0, -1.5364721417427063)
        gl_ft.glVertex3f(-0.6504332423210144, 0.0, -0.056056540459394455)
        gl_ft.glVertex3f(-0.8511086106300354, 0.0, 0.9973527789115906)
        gl_ft.glVertex3f(-0.8944775462150574, 0.0, 1.605450689792633)
        gl_ft.glVertex3f(-0.8661590218544006, 0.0, 1.9359845519065857)
        gl_ft.glVertex3f(-0.7912097573280334, 0.0, 2.266518533229828)
        gl_ft.glVertex3f(-0.714862048625946, 0.0, 2.473005712032318)
        gl_ft.glVertex3f(-0.5831533074378967, 0.0, 2.6794928908348083)
        gl_ft.glVertex3f(-0.44680944085121155, 0.0, 2.8275105357170105)
        gl_ft.glVertex3f(-0.24102792143821716, 0.0, 2.9755284190177917)
        gl_ft.glVertex3f(-0.15450866520404816, 0.0, 3.010420262813568)
        gl_ft.glVertex3f(8.940696716308594e-08, 0.0, 3.0274547934532166)
        gl_ft.glEnd()
    elif shape == 36:
        # 36 cube
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(1.0, 1.0, 1.0)
        gl_ft.glVertex3f(1.0, 1.0, -1.0)
        gl_ft.glVertex3f(-1.0, 1.0, -1.0)
        gl_ft.glVertex3f(-1.0, 1.0, 1.0)
        gl_ft.glVertex3f(1.0, 1.0, 1.0)
        gl_ft.glVertex3f(1.0, -1.0, 1.0)
        gl_ft.glVertex3f(-1.0, -1.0, 1.0)
        gl_ft.glVertex3f(-1.0, 1.0, 1.0)
        gl_ft.glVertex3f(-1.0, 1.0, -1.0)
        gl_ft.glVertex3f(-1.0, -1.0, -1.0)
        gl_ft.glVertex3f(-1.0, -1.0, 1.0)
        gl_ft.glVertex3f(1.0, -1.0, 1.0)
        gl_ft.glVertex3f(1.0, -1.0, -1.0)
        gl_ft.glVertex3f(-1.0, -1.0, -1.0)
        gl_ft.glVertex3f(-1.0, 1.0, -1.0)
        gl_ft.glVertex3f(1.0, 1.0, -1.0)
        gl_ft.glVertex3f(1.0, -1.0, -1.0)
        gl_ft.glEnd()
    elif shape == 37:
        # 37 targetG
        posx, posz = 0, 0
        startx, startz = 0, 0
        endx, endz = 0, 0

        gl_ft.glScalef(0.2, 0.2, 0.2)
        gl_ft.glRotatef(45, 0, 1, 0)

        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 8 / 80) + posx
            z = math.sin(1 * i * 2 * PI / 8 / 80) + posz
            if not i:
                startx += x
                startz += z
            elif i == 159:
                endx += x
                endz += z

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 80) + posx
            z = math.sin(1 * i * 2 * PI / 80) + posz
            gl_ft.glVertex3f(x * 4, 0, z * 4)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 80) + posx
            z = math.sin(1 * i * 2 * PI / 80) + posz
            gl_ft.glVertex3f(x / 0.2, 0, z / 0.2)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 80) + posx
            z = math.sin(1 * i * 2 * PI / 80) + posz
            gl_ft.glVertex3f(-x * 4, 0, -z * 4)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(160):
            x = math.cos(1 * i * 2 * PI / 80) + posx
            z = math.sin(1 * i * 2 * PI / 80) + posz
            gl_ft.glVertex3f(-x / 0.2, 0, -z / 0.2)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(startx, 0.0, startz)
        gl_ft.glVertex3f(startx / 0.5, 0.0, startz / 0.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(-startx, 0.0, startz)
        gl_ft.glVertex3f(-startx / 0.5, 0.0, startz / 0.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(-endx, 0.0, -endz)
        gl_ft.glVertex3f(-endx / 0.5, 0.0, -endz / 0.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(endx, 0.0, endz)
        gl_ft.glVertex3f(endx / 0.5, 0.0, endz / 0.5)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(200):
            x = math.cos(i * 2 * PI / 100) + posx
            z = math.sin(i * 2 * PI / 100) + posz
            gl_ft.glVertex3f(x / 2, 0, z / 2)
        gl_ft.glEnd()
    elif shape == 38:
        # 38 gravity of explosion logo
        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(0.98479272731, 0.0, -0.173610761384)
        gl_ft.glVertex3f(0.360732536321, 0.0, -0.172833786259)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(0.961577693202, 0.0, -0.274538647455)
        gl_ft.glVertex3f(0.676297750874, -0.00167339274653, -0.274615713084)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(0.720690487651, 0.0, 0.115750573358)
        gl_ft.glVertex3f(0.382854202515, 0.0, 0.115750573358)
        gl_ft.glEnd()

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        gl_ft.glVertex3f(-0.185305748009, 0.0, 0.0752448406889)
        gl_ft.glVertex3f(0.0, 0.0, 0.0752448406889)
        gl_ft.glVertex3f(0.0, 0.0, -0.0694039072129)
        gl_ft.glVertex3f(-0.187571573682, 0.0, -0.0694039072129)
        gl_ft.glEnd()

        gl_ft.glRotatef(10, 0, 1, 0)

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(180):
            x = math.cos(1 * i * 2 * PI / 2 / 91)
            z = math.sin(1 * i * 2 * PI / 2 / 91)
            gl_ft.glVertex3f(x, 0, z)
        gl_ft.glEnd()

        gl_ft.glRotatef(12.1, 0, 1, 0)

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(180):
            x = math.cos(i * 3 * PI / 3 / 98)
            z = math.sin(i * 3 * PI / 3 / 98)
            gl_ft.glVertex3f(x / 1.37, 0, -z / 1.37)
        gl_ft.glEnd()

        gl_ft.glRotatef(3.5, 0, 1, 0)

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(180):
            x = math.cos(i * 3 * PI / 3 / 101.45)
            z = math.sin(i * 3 * PI / 3 / 101.45)
            gl_ft.glVertex3f(x / 2.5, 0, -z / 2.5)
        gl_ft.glEnd()

        gl_ft.glRotatef(-3.5, 0, 1, 0)

        gl_ft.glBegin(OpenMayaRender.MGL_LINE_STRIP)
        for i in range(180):
            x = math.cos(i * 3 * PI / 3 / 101.45)
            z = math.sin(i * 3 * PI / 3 / 101.45)
            gl_ft.glVertex3f(- x / 5, 0, z / 5)
        gl_ft.glEnd()
# end def shapes()


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
