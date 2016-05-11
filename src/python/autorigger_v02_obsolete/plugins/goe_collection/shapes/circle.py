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


def two_arrow_circle(render=OpenMayaRender.MGL_LINE_STRIP):
    """Create a two_arrow_circle shape."""
    gl_ft.glBegin(render)
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
# end def two_arrow_circle


def four_arrow_circle(render=OpenMayaRender.MGL_LINE_STRIP):
    """Create a four arrowed circle shape."""
    gl_ft.glBegin(render)
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
# end def four_arrow_circle
