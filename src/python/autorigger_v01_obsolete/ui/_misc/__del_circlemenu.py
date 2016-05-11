"""
Created on 11/29/2013
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: The custom menu circle for Pandora's Box
"""

from PySide import QtCore, QtGui


"""
subclass from QGraphicsProxyWidget

        wid = QtGui.QWidget()
        wid.setLayout(QtGui.QVBoxLayout())
        btn = QtGui.QPushButton('gggggg')
        wid.layout().addWidget(btn)

        wid.setAutoFillBackground(False)
        wid.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        wid.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        wid.move(event.scenePos().x(), event.scenePos().y())

        wid.layout().setContentsMargins(50, 50, 50, 50)

        proxy = self.addWidget(wid)

        print proxy

        proxy.setFlag(QtGui.QGraphicsItem.ItemIgnoresTransformations)

"""



class CircleMenu(QtGui.QMenu):
    """@todo: maybe subclass from QMenu"""
    def __init__(self):
        super(CircleMenu, self).__init__()
    # end def __init__

    def paintEvent(self, event):
        """"""
        backgroundColor = self.palette().light().color()
        backgroundColor.setAlpha(122)
        backgroundColor.setRgb(122, 122, 40)
        print backgroundColor
        customPainter = QtGui.QPainter()
        print self.rect()

        b = QtGui.QBrush()
        b.setColor(backgroundColor)
        customPainter.setBackground(b)
        customPainter.setBrush(b)
        customPainter.drawRect(self.rect())

    def add_action(self, action, index=-1):
        """Adds an action to this menu. The index specifies the position."""
    # end def add_action

    def open(self):
        """Opens the menu with an animation."""
        pass
    # end def open

    def close(self):
        """Closes the menu with an animation."""
        pass
    # end def close

    def calculate_position(self, action):
        """Calculates the position for the given action in the menu.
            * get angle
            * get x and y pos
            * return pos
        """

    # end def calculate_position
# end class CircleMenu


class CircleMenuAction(QtGui.QWidget):
    """Represents an action in the menu.
    A CircleMenuAction has the following attributes:
        * icon
        * name
        * function

        """
    def __init__(self, name, function=None, icon=None):
        super(CircleMenuAction, self).__init__()
    # end def __init__
# end class CircleMenuAction

