'''
Created on Sep 5, 2015

@author: Emre
'''

import math
from maya import OpenMaya
from maya import OpenMayaRender

nodename = 'goe_locator'
nodeid = OpenMaya.MTypeId(0x4728489)

gl_renderer = OpenMayaRender.MHardwareRenderer.theRenderer()
gl_ft = gl_renderer.glFunctionTable()

PI = 3.14159265359


def circle(render=OpenMayaRender.MGL_LINE_STRIP):
    """Create a circle shape."""
    gl_ft.glBegin(render)
    for i in range(256):
        x = math.cos(i * 2 * PI / 128)
        z = math.sin(i * 2 * PI / 128)
        gl_ft.glVertex3f(x, 0, z)
    # end for iterate range
    gl_ft.glEnd()
# end def circle



def cube(render=OpenMayaRender.MGL_LINE_STRIP):
    """Create a cube shape."""
    gl_ft.glBegin(render)
    gl_ft.glVertex3f(1.0, -1.0, -1.0)
    gl_ft.glVertex3f(-1.0, -1.0, -1.0)
    gl_ft.glVertex3f(-1.0, -1.0, 1.0)
    gl_ft.glVertex3f(1.0, -1.0, 1.0)
    gl_ft.glVertex3f(1.0, -1.0, -1.0)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(1.0, 1.0, -1.0)
    gl_ft.glVertex3f(-1.0, 1.0, -1.0)
    gl_ft.glVertex3f(-1.0, 1.0, 1.0)
    gl_ft.glVertex3f(1.0, 1.0, 1.0)
    gl_ft.glVertex3f(1.0, 1.0, -1.0)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(1.0, -1.0, 1.0)
    gl_ft.glVertex3f(-1.0, -1.0, 1.0)
    gl_ft.glVertex3f(-1.0, 1.0, 1.0)
    gl_ft.glVertex3f(1.0, 1.0, 1.0)
    gl_ft.glVertex3f(1.0, -1.0, 1.0)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(1.0, -1.0, -1.0)
    gl_ft.glVertex3f(-1.0, -1.0, -1.0)
    gl_ft.glVertex3f(-1.0, 1.0, -1.0)
    gl_ft.glVertex3f(1.0, 1.0, -1.0)
    gl_ft.glVertex3f(1.0, -1.0, -1.0)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(-1.0, -1.0, 1.0)
    gl_ft.glVertex3f(-1.0, -1.0, -1.0)
    gl_ft.glVertex3f(-1.0, 1.0, -1.0)
    gl_ft.glVertex3f(-1.0, 1.0, 1.0)
    gl_ft.glVertex3f(-1.0, -1.0, 1.0)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(1.0, -1.0, 1.0)
    gl_ft.glVertex3f(1.0, -1.0, -1.0)
    gl_ft.glVertex3f(1.0, 1.0, -1.0)
    gl_ft.glVertex3f(1.0, 1.0, 1.0)
    gl_ft.glVertex3f(1.0, -1.0, 1.0)
    gl_ft.glEnd()
# end def cube
