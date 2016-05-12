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


def triangle(render=OpenMayaRender.MGL_LINE_STRIP):
    """Create a triangle shape."""
    gl_ft.glBegin(render)
    gl_ft.glVertex3f(0.0, 0.0, 1.0)
    gl_ft.glVertex3f(-1.0, 0.0, -1.0)
    gl_ft.glVertex3f(1.0, 0.0, -1.0)
    gl_ft.glVertex3f(0.0, 0.0, 1.0)
    gl_ft.glEnd()
# end def triangle
