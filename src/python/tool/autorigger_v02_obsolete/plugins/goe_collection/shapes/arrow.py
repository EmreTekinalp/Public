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



def arrow(render=OpenMayaRender.MGL_LINE_STRIP):
    """Create an arrow shape."""
    gl_ft.glBegin(render)
    gl_ft.glVertex3f(1.0, 0.0, -0.356839146005)
    gl_ft.glVertex3f(-0.340491309259, 0.0, -0.225141166382)
    gl_ft.glVertex3f(-0.340491309259, 0.0, -0.41729606295)
    gl_ft.glVertex3f(-1.0, 0.0, 0.0)
    gl_ft.glVertex3f(-0.340491309259, 0.0, 0.41729606295)
    gl_ft.glVertex3f(-0.340491309259, 0.0, 0.225141166382)
    gl_ft.glVertex3f(1.0, 0.0, 0.356839146005)
    gl_ft.glVertex3f(1.0, 0.0, -0.356839146005)
    gl_ft.glEnd()
# end def arrow


def big_arrow(render=OpenMayaRender.MGL_LINE_STRIP):
    """Create a big_arrow shape."""
    gl_ft.glBegin(render)
    gl_ft.glVertex3f(1.0, 0.0, -0.356839146005)
    gl_ft.glVertex3f(-0.340491309259, 0.0, -0.225141166382)
    gl_ft.glVertex3f(-0.340491309259, 0.0, -0.41729606295)
    gl_ft.glVertex3f(-1.0, 0.0, 0.0)
    gl_ft.glVertex3f(-0.340491309259, 0.0, 0.41729606295)
    gl_ft.glVertex3f(-0.340491309259, 0.0, 0.225141166382)
    gl_ft.glVertex3f(1.0, 0.0, 0.356839146005)
    gl_ft.glVertex3f(1.0, 0.0, -0.356839146005)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(1.0, 0.356839146005, 1.58468414393e-16)
    gl_ft.glVertex3f(-0.340491309259, 0.225141166382, 9.99827626833e-17)
    gl_ft.glVertex3f(-0.340491309259, 0.41729606295, 1.85316678869e-16)
    gl_ft.glVertex3f(-1.0, 0.0, 0.0)
    gl_ft.glVertex3f(-0.340491309259, -0.41729606295, -1.85316678869e-16)
    gl_ft.glVertex3f(-0.340491309259, -0.225141166382, -9.99827626833e-17)
    gl_ft.glVertex3f(1.0, -0.356839146005, -1.58468414393e-16)
    gl_ft.glVertex3f(1.0, 0.356839146005, 1.58468414393e-16)
    gl_ft.glEnd()
# end def big_arrow


def double_arrow(render=OpenMayaRender.MGL_LINE_STRIP):
    """Create a double_arrow shape."""
    gl_ft.glBegin(render)
    gl_ft.glVertex3f(0.0, 0.0, -0.5)
    gl_ft.glVertex3f(1.0, 0.0, -0.5)
    gl_ft.glVertex3f(1.0, 0.0, -1.0)
    gl_ft.glVertex3f(2.0, 0.0, 0.0)
    gl_ft.glVertex3f(1.0, 0.0, 1.0)
    gl_ft.glVertex3f(1.0, 0.0, 0.5)
    gl_ft.glVertex3f(0.0, 0.0, 0.5)
    gl_ft.glVertex3f(-1.0, 0.0, 0.5)
    gl_ft.glVertex3f(-1.0, 0.0, 1.0)
    gl_ft.glVertex3f(-2.0, 0.0, 0.0)
    gl_ft.glVertex3f(-1.0, 0.0, -1.0)
    gl_ft.glVertex3f(-1.0, 0.0, -0.5)
    gl_ft.glVertex3f(0.0, 0.0, -0.5)
    gl_ft.glEnd()
# end def double_arrow


def visor_arrow(render=OpenMayaRender.MGL_LINE_STRIP):
    """Create a visor arrow shape."""
    gl_ft.glBegin(render)
    gl_ft.glVertex3f(0.0, 0.0, -0.499988098016)
    gl_ft.glVertex3f(0.999976196031, 0.0, -0.245364529232)
    gl_ft.glVertex3f(0.999976196031, 0.0, -0.490729058463)
    gl_ft.glVertex3f(1.99995239206, 0.0, 0.0)
    gl_ft.glVertex3f(0.999976196031, 0.0, 0.490729058463)
    gl_ft.glVertex3f(0.999976196031, 0.0, 0.245364529232)
    gl_ft.glVertex3f(0.0, 0.0, 0.499988098016)
    gl_ft.glVertex3f(-0.999976196031, 0.0, 0.245364529232)
    gl_ft.glVertex3f(-0.999976196031, 0.0, 0.490729058463)
    gl_ft.glVertex3f(-1.99995239206, 0.0, 0.0)
    gl_ft.glVertex3f(-0.999976196031, 0.0, -0.490729058463)
    gl_ft.glVertex3f(-0.999976196031, 0.0, -0.245364529232)
    gl_ft.glVertex3f(0.0, 0.0, -0.499988098016)
    gl_ft.glEnd()
# end def visor_arrow
