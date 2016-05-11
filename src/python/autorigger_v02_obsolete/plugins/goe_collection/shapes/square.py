'''
Created on Sep 5, 2015

@author: Emre
'''

from maya import OpenMaya
from maya import OpenMayaRender

nodename = 'goe_locator'
nodeid = OpenMaya.MTypeId(0x4728489)

gl_renderer = OpenMayaRender.MHardwareRenderer.theRenderer()
gl_ft = gl_renderer.glFunctionTable()

PI = 3.14159265359


def square(render=OpenMayaRender.MGL_LINE_STRIP, value=1.0):
    """Create a square shape."""
    gl_ft.glBegin(render)
    gl_ft.glVertex3f(-value, 0.0, -value)
    gl_ft.glVertex3f(-value, 0.0, value)
    gl_ft.glVertex3f(value, 0.0, value)
    gl_ft.glVertex3f(value, 0.0, -value)
    gl_ft.glVertex3f(-value, 0.0, -value)
    gl_ft.glEnd()
# end def square



def box(render=OpenMayaRender.MGL_LINE_STRIP):
    """Create a box shape."""
    gl_ft.glBegin(render)
    gl_ft.glVertex3f(-1.0008, 0.0, -0.834)
    gl_ft.glVertex3f(-0.834, 0.0, -0.834)
    gl_ft.glVertex3f(-0.834, 0.0, -0.5004)
    gl_ft.glVertex3f(-1.0008, 0.0, -0.5004)
    gl_ft.glVertex3f(-1.0008, 0.0, -0.834)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(-1.0008, 0.0, -0.834)
    gl_ft.glVertex3f(-0.834, 0.0, -0.834)
    gl_ft.glVertex3f(-0.834, 0.0, -1.0008)
    gl_ft.glVertex3f(-1.0008, 0.0, -0.834)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(-0.834, 0.0, -0.834)
    gl_ft.glVertex3f(-0.834, 0.0, -1.0008)
    gl_ft.glVertex3f(-0.5004, 0.0, -1.0008)
    gl_ft.glVertex3f(-0.5004, 0.0, -0.834)
    gl_ft.glVertex3f(-0.834, 0.0, -0.834)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(-0.5004, 0.0, -0.952760054778)
    gl_ft.glVertex3f(0.5004, 0.0, -0.952760054778)
    gl_ft.glVertex3f(0.5004, 0.0, -0.882039945222)
    gl_ft.glVertex3f(-0.5004, 0.0, -0.882039945222)
    gl_ft.glVertex3f(-0.5004, 0.0, -0.952760054778)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(0.834, 0.0, -1.0008)
    gl_ft.glVertex3f(0.834, 0.0, -0.834)
    gl_ft.glVertex3f(0.5004, 0.0, -0.834)
    gl_ft.glVertex3f(0.5004, 0.0, -1.0008)
    gl_ft.glVertex3f(0.834, 0.0, -1.0008)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(0.834, 0.0, -1.0008)
    gl_ft.glVertex3f(0.834, 0.0, -0.834)
    gl_ft.glVertex3f(1.0008, 0.0, -0.834)
    gl_ft.glVertex3f(0.834, 0.0, -1.0008)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(0.834, 0.0, -0.834)
    gl_ft.glVertex3f(1.0008, 0.0, -0.834)
    gl_ft.glVertex3f(1.0008, 0.0, -0.5004)
    gl_ft.glVertex3f(0.834, 0.0, -0.5004)
    gl_ft.glVertex3f(0.834, 0.0, -0.834)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(0.952760054778, 0.0, -0.5004)
    gl_ft.glVertex3f(0.952760054778, 0.0, 0.5004)
    gl_ft.glVertex3f(0.882039945222, 0.0, 0.5004)
    gl_ft.glVertex3f(0.882039945222, 0.0, -0.5004)
    gl_ft.glVertex3f(0.952760054778, 0.0, -0.5004)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(1.0008, 0.0, 0.834)
    gl_ft.glVertex3f(0.834, 0.0, 0.834)
    gl_ft.glVertex3f(0.834, 0.0, 0.5004)
    gl_ft.glVertex3f(1.0008, 0.0, 0.5004)
    gl_ft.glVertex3f(1.0008, 0.0, 0.834)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(1.0008, 0.0, 0.834)
    gl_ft.glVertex3f(0.834, 0.0, 0.834)
    gl_ft.glVertex3f(0.834, 0.0, 1.0008)
    gl_ft.glVertex3f(1.0008, 0.0, 0.834)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(0.834, 0.0, 0.834)
    gl_ft.glVertex3f(0.834, 0.0, 1.0008)
    gl_ft.glVertex3f(0.5004, 0.0, 1.0008)
    gl_ft.glVertex3f(0.5004, 0.0, 0.834)
    gl_ft.glVertex3f(0.834, 0.0, 0.834)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(0.5004, 0.0, 0.952760054778)
    gl_ft.glVertex3f(-0.5004, 0.0, 0.952760054778)
    gl_ft.glVertex3f(-0.5004, 0.0, 0.882039945222)
    gl_ft.glVertex3f(0.5004, 0.0, 0.882039945222)
    gl_ft.glVertex3f(0.5004, 0.0, 0.952760054778)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(-0.834, 0.0, 1.0008)
    gl_ft.glVertex3f(-0.834, 0.0, 0.834)
    gl_ft.glVertex3f(-0.5004, 0.0, 0.834)
    gl_ft.glVertex3f(-0.5004, 0.0, 1.0008)
    gl_ft.glVertex3f(-0.834, 0.0, 1.0008)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(-0.834, 0.0, 1.0008)
    gl_ft.glVertex3f(-0.834, 0.0, 0.834)
    gl_ft.glVertex3f(-1.0008, 0.0, 0.834)
    gl_ft.glVertex3f(-0.834, 0.0, 1.0008)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(-0.834, 0.0, 0.834)
    gl_ft.glVertex3f(-1.0008, 0.0, 0.834)
    gl_ft.glVertex3f(-1.0008, 0.0, 0.5004)
    gl_ft.glVertex3f(-0.834, 0.0, 0.5004)
    gl_ft.glVertex3f(-0.834, 0.0, 0.834)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(-0.952760054778, 0.0, 0.5004)
    gl_ft.glVertex3f(-0.952760054778, 0.0, -0.5004)
    gl_ft.glVertex3f(-0.882039945222, 0.0, -0.5004)
    gl_ft.glVertex3f(-0.882039945222, 0.0, 0.5004)
    gl_ft.glVertex3f(-0.952760054778, 0.0, 0.5004)
    gl_ft.glEnd()
# end def box
