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


def cross(render=OpenMayaRender.MGL_LINE_STRIP):
    """Create a cross shape."""
    gl_ft.glBegin(render)
    gl_ft.glVertex3f(-0.2, 0.0, -0.2)
    gl_ft.glVertex3f(-0.103011337876, 0.0, -0.6)
    gl_ft.glVertex3f(-0.206022675751, 0.0, -0.6)
    gl_ft.glVertex3f(0.0, 0.0, -1.0)
    gl_ft.glVertex3f(0.206022675751, 0.0, -0.6)
    gl_ft.glVertex3f(0.103011337876, 0.0, -0.6)
    gl_ft.glVertex3f(0.2, 0.0, -0.2)
    gl_ft.glVertex3f(0.6, 0.0, -0.0883699436421)
    gl_ft.glVertex3f(0.6, 0.0, -0.176739887284)
    gl_ft.glVertex3f(1.0, 0.0, 0.0)
    gl_ft.glVertex3f(0.6, 0.0, 0.176739887284)
    gl_ft.glVertex3f(0.6, 0.0, 0.0883699436421)
    gl_ft.glVertex3f(0.2, 0.0, 0.2)
    gl_ft.glVertex3f(0.103011337876, 0.0, 0.6)
    gl_ft.glVertex3f(0.206022675751, 0.0, 0.6)
    gl_ft.glVertex3f(0.0, 0.0, 1.0)
    gl_ft.glVertex3f(-0.206022675751, 0.0, 0.6)
    gl_ft.glVertex3f(-0.103011337876, 0.0, 0.6)
    gl_ft.glVertex3f(-0.2, 0.0, 0.2)
    gl_ft.glVertex3f(-0.6, 0.0, 0.0883699436421)
    gl_ft.glVertex3f(-0.6, 0.0, 0.176739887284)
    gl_ft.glVertex3f(-1.0, 0.0, 0.0)
    gl_ft.glVertex3f(-0.6, 0.0, -0.176739887284)
    gl_ft.glVertex3f(-0.6, 0.0, -0.0883699436421)
    gl_ft.glVertex3f(-0.2, 0.0, -0.2)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(-0.2, -0.2, 8.881784197e-17)
    gl_ft.glVertex3f(-0.103011337876, -0.6, 2.6645352591e-16)
    gl_ft.glVertex3f(-0.206022675751, -0.6, 2.6645352591e-16)
    gl_ft.glVertex3f(0.0, -1.0, 4.4408920985e-16)
    gl_ft.glVertex3f(0.206022675751, -0.6, 2.6645352591e-16)
    gl_ft.glVertex3f(0.103011337876, -0.6, 2.6645352591e-16)
    gl_ft.glVertex3f(0.2, -0.2, 8.881784197e-17)
    gl_ft.glVertex3f(0.6, -0.0883699436421, 3.92441384465e-17)
    gl_ft.glVertex3f(0.6, -0.176739887284, 7.84882768931e-17)
    gl_ft.glVertex3f(1.0, 0.0, 0.0)
    gl_ft.glVertex3f(0.6, 0.176739887284, -7.84882768931e-17)
    gl_ft.glVertex3f(0.6, 0.0883699436421, -3.92441384465e-17)
    gl_ft.glVertex3f(0.2, 0.2, -8.881784197e-17)
    gl_ft.glVertex3f(0.103011337876, 0.6, -2.6645352591e-16)
    gl_ft.glVertex3f(0.206022675751, 0.6, -2.6645352591e-16)
    gl_ft.glVertex3f(0.0, 1.0, -4.4408920985e-16)
    gl_ft.glVertex3f(-0.206022675751, 0.6, -2.6645352591e-16)
    gl_ft.glVertex3f(-0.103011337876, 0.6, -2.6645352591e-16)
    gl_ft.glVertex3f(-0.2, 0.2, -8.881784197e-17)
    gl_ft.glVertex3f(-0.6, 0.0883699436421, -3.92441384465e-17)
    gl_ft.glVertex3f(-0.6, 0.176739887284, -7.84882768931e-17)
    gl_ft.glVertex3f(-1.0, 0.0, 0.0)
    gl_ft.glVertex3f(-0.6, -0.176739887284, 7.84882768931e-17)
    gl_ft.glVertex3f(-0.6, -0.0883699436421, 3.92441384465e-17)
    gl_ft.glVertex3f(-0.2, -0.2, 8.881784197e-17)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(-1.24344978758e-15, -0.2, -0.2)
    gl_ft.glVertex3f(-3.06822745594e-15, -0.6, -0.103011337876)
    gl_ft.glVertex3f(-3.20546612687e-15, -0.6, -0.206022675751)
    gl_ft.glVertex3f(-4.88498130835e-15, -1.0, 0.0)
    gl_ft.glVertex3f(-2.65651144315e-15, -0.6, 0.206022675751)
    gl_ft.glVertex3f(-2.79375011408e-15, -0.6, 0.103011337876)
    gl_ft.glVertex3f(-7.1054273576e-16, -0.2, 0.2)
    gl_ft.glVertex3f(3.67675054818e-16, -0.0883699436421, 0.6)
    gl_ft.glVertex3f(-6.40104680936e-17, -0.176739887284, 0.6)
    gl_ft.glVertex3f(1.33226762955e-15, 0.0, 1.0)
    gl_ft.glVertex3f(1.66273162355e-15, 0.176739887284, 0.6)
    gl_ft.glVertex3f(1.23104610064e-15, 0.0883699436421, 0.6)
    gl_ft.glVertex3f(1.24344978758e-15, 0.2, 0.2)
    gl_ft.glVertex3f(3.06822745594e-15, 0.6, 0.103011337876)
    gl_ft.glVertex3f(3.20546612687e-15, 0.6, 0.206022675751)
    gl_ft.glVertex3f(4.88498130835e-15, 1.0, 0.0)
    gl_ft.glVertex3f(2.65651144315e-15, 0.6, -0.206022675751)
    gl_ft.glVertex3f(2.79375011408e-15, 0.6, -0.103011337876)
    gl_ft.glVertex3f(7.1054273576e-16, 0.2, -0.2)
    gl_ft.glVertex3f(-3.67675054818e-16, 0.0883699436421, -0.6)
    gl_ft.glVertex3f(6.40104680936e-17, 0.176739887284, -0.6)
    gl_ft.glVertex3f(-1.33226762955e-15, 0.0, -1.0)
    gl_ft.glVertex3f(-1.66273162355e-15, -0.176739887284, -0.6)
    gl_ft.glVertex3f(-1.23104610064e-15, -0.0883699436421, -0.6)
    gl_ft.glVertex3f(-1.24344978758e-15, -0.2, -0.2)
    gl_ft.glEnd()
# end def cross
