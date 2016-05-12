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


def goe(render=OpenMayaRender.MGL_LINE_STRIP):
    """The logo of gravity of explosion."""
    gl_ft.glBegin(render)
    gl_ft.glVertex3f(0.98479272731, 0.0, -0.173610761384)
    gl_ft.glVertex3f(0.360732536321, 0.0, -0.172833786259)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(0.961577693202, 0.0, -0.274538647455)
    gl_ft.glVertex3f(0.676297750874, -0.00167339274653, -0.274615713084)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(0.720690487651, 0.0, 0.115750573358)
    gl_ft.glVertex3f(0.382854202515, 0.0, 0.115750573358)
    gl_ft.glEnd()

    gl_ft.glBegin(render)
    gl_ft.glVertex3f(-0.185305748009, 0.0, 0.0752448406889)
    gl_ft.glVertex3f(0.0, 0.0, 0.0752448406889)
    gl_ft.glVertex3f(0.0, 0.0, -0.0694039072129)
    gl_ft.glVertex3f(-0.187571573682, 0.0, -0.0694039072129)
    gl_ft.glEnd()

    gl_ft.glRotatef(10, 0, 1, 0)

    gl_ft.glBegin(render)
    for i in range(180):
        x = math.cos(1 * i * 2 * PI / 2 / 91)
        z = math.sin(1 * i * 2 * PI / 2 / 91)
        gl_ft.glVertex3f(x, 0, z)
    gl_ft.glEnd()

    gl_ft.glRotatef(12.1, 0, 1, 0)

    gl_ft.glBegin(render)
    for i in range(180):
        x = math.cos(i * 3 * PI / 3 / 98)
        z = math.sin(i * 3 * PI / 3 / 98)
        gl_ft.glVertex3f(x / 1.37, 0, -z / 1.37)
    gl_ft.glEnd()

    gl_ft.glRotatef(3.5, 0, 1, 0)

    gl_ft.glBegin(render)
    for i in range(180):
        x = math.cos(i * 3 * PI / 3 / 101.45)
        z = math.sin(i * 3 * PI / 3 / 101.45)
        gl_ft.glVertex3f(x / 2.5, 0, -z / 2.5)
    gl_ft.glEnd()

    gl_ft.glRotatef(-3.5, 0, 1, 0)

    gl_ft.glBegin(render)
    for i in range(180):
        x = math.cos(i * 3 * PI / 3 / 101.45)
        z = math.sin(i * 3 * PI / 3 / 101.45)
        gl_ft.glVertex3f(- x / 5, 0, z / 5)
    gl_ft.glEnd()
# end def goe
