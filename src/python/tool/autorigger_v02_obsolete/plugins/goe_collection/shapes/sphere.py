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


def sphere(render=OpenMayaRender.MGL_LINE_STRIP):
    """Create a sphere shape."""
    gl_ft.glBegin(render)
    for i in range(256):
        y = math.cos(i * 2 * PI / 128)
        z = math.sin(i * 2 * PI / 128)
        gl_ft.glVertex3f(0, y, z)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    for i in range(256):
        x = math.cos(i * 2 * PI / 128)
        z = math.sin(i * 2 * PI / 128)
        gl_ft.glVertex3f(x, 0, z)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    for i in range(256):
        x = math.cos(i * 2 * PI / 128)
        y = math.sin(i * 2 * PI / 128)
        gl_ft.glVertex3f(x, y, 0)
    gl_ft.glEnd()
# end def sphere
