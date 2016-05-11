'''
Created on Oct 1, 2014

@author: Emre
'''


import shiboken
from PySide import QtGui, QtCore
from maya import cmds, OpenMayaUI


window_object = "ScrollObject"
window_title = "Scroll"

def getMayaWindow():
    """
    Get the main Maya window as a QtGui.QMainWindow instance
    @return: QtGui.QMainWindow instance of the top level Maya windows
    """
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    if ptr is not None:
        return shiboken.wrapInstance(long(ptr), QtGui.QWidget)


class Scroll(QtGui.QDialog):
    def __init__(self, parent = getMayaWindow()):
        super(Scroll, self).__init__(parent)

        #--- vars
        self.framelist = list()

        #--- methods
        self.__create()
    #END __init__()

    def __setup_ui(self):
        self.setWindowTitle(window_title)
        self.setObjectName(window_object)
        self.setGeometry(600,300,300,400)
        self.setFixedWidth(300)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    #END __setup_ui()

    def setup_layout(self):
        #--- create scroll widget and area and layout
        self.scrollLayout = QtGui.QVBoxLayout()
        self.scrollArea = QtGui.QScrollArea()
        self.scrollWidget = QtGui.QWidget()

        #--- create layouts 
        self.mainLayout = QtGui.QVBoxLayout()
        self.groupLayoutA = QtGui.QVBoxLayout()
        self.groupLayoutB = QtGui.QVBoxLayout()

        #--- create and setup groupbox
        self.groupBoxA = QtGui.QGroupBox('Guides')
        self.groupBoxB = QtGui.QGroupBox('Puppet')
        self.groupBoxA.setFixedWidth(250)
        self.groupBoxB.setFixedWidth(250)

        #--- create custom buttons
        self.createA_btn = CreateButton(self, 'create')
        self.upA_btn = MoveButton(self, 'move up', 1)
        self.downA_btn = MoveButton(self, 'move down', 0)

        self.createB_btn = CreateButton(self, 'create')
        self.upB_btn = MoveButton(self, 'move up', 1)
        self.downB_btn = MoveButton(self, 'move down', 0)

        #--- add widgets to the guide groubox layout
        self.groupLayoutA.addWidget(self.createA_btn)
        self.groupLayoutA.addWidget(self.upA_btn)
        self.groupLayoutA.addWidget(self.downA_btn)

        #--- add widgets to the puppet groubox layout
        self.groupLayoutB.addWidget(self.createB_btn)
        self.groupLayoutB.addWidget(self.upB_btn)
        self.groupLayoutB.addWidget(self.downB_btn)

        #--- set the groubox layout
        self.groupBoxA.setLayout(self.groupLayoutA)
        self.groupBoxB.setLayout(self.groupLayoutB)

        #--- add the groupbox widgets to the mainLayout
#         self.mainLayout.addWidget(self.groupBoxA)
#         self.mainLayout.addWidget(self.groupBoxB)

        self.add_in_here.layout().addWidget(self.groupBoxA)
        self.add_in_here.layout().addWidget(self.groupBoxB)

        #--- add the mainLayout to the scrollwidget
#         self.scrollWidget.setLayout(self.mainLayout)
#         #--- set the scrollwidget to the scrollarea
#         self.scrollArea.setWidget(self.scrollWidget)
#         #--- add the scrollarea to the scrolllayout
#         self.scrollLayout.addWidget(self.scrollArea)
# 
#         #--- set scrolllayout to the main layout
#         self.setLayout(self.scrollLayout)
    #END setup_layout()

    def __create(self):
        self.__setup_ui()
        self.setup_layout()
    #END create()

class CreateButton(QtGui.QPushButton):
    def __init__(self, parent, name):
        super(CreateButton, self).__init__(parent)
        self.parent = parent
        self.setText(name)

    def mousePressEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        self.frame = Frame(self, self.parent.framelist)
        self.parent.framelist.append(self.frame)
        self.parent.groupLayoutA.addWidget(self.frame)
        return self.frame


class EditButton(QtGui.QPushButton):
    def __init__(self, parent, name, label):
        super(EditButton, self).__init__(parent)
        self.setText(name)
        self.parent = parent
        self.label = label

    def mousePressEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        if self.label.text() == 'edit me':
            self.label.setText('changed ma fucker')
        else:
            self.label.setText('edit me')


class MoveButton(QtGui.QPushButton):
    def __init__(self, parent, name, up):
        super(MoveButton, self).__init__(parent)
        self.setText(name)
        self.parent = parent
        self.up = up

        #--- vars
        self.check         = 0
        self.frameSelected = list()

    def mousePressEvent(self, event):
        self.check = 0
        for index, i in enumerate(self.parent.framelist):
            if i.styleSheet() == 'background-color: rgb(60,60,60)':
                self.frameSelected = [i, index]
                self.check = 1

    def mouseReleaseEvent(self, event):
        if not self.check:
            return

        index = self.frameSelected[1]
        if self.up:
            if not index:
                self.parent.vbox.insertWidget(0, self.frameSelected[0])
            else:
                self.parent.vbox.insertWidget(index - 1, self.frameSelected[0])
                self.parent.framelist.pop(index)
                self.parent.framelist.insert(index - 1, self.frameSelected[0])
        else:
            if index == len(self.parent.framelist):
                self.parent.vbox.insertWidget(len(self.parent.framelist), 
                                              self.frameSelected[0])
            else:
                self.parent.vbox.insertWidget(index + 1, self.frameSelected[0])
                self.parent.framelist.pop(index)
                self.parent.framelist.insert(index + 1, self.frameSelected[0])


class Frame(QtGui.QFrame):
    def __init__(self, parent, framelist):
        super(Frame, self).__init__(parent)
        self.framelist = framelist
        self.setupWidget()

    def setupWidget(self):
        hbox = QtGui.QHBoxLayout()
        text = QtGui.QLabel('edit me')
        butt = EditButton(self, 'Edit', text)

        hbox.addWidget(text)
        hbox.addStretch()
        hbox.addWidget(butt)
        self.setLayout(hbox)
        self.setStyleSheet('background-color: rgb(50,50,50)')

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.setStyleSheet('background-color: rgb(60,60,60)')
            sender = self
            for frame in self.framelist:
                if not self == frame:
                    frame.setStyleSheet('background-color: rgb(50,50,50)')
                else:
                    sender = self
            return sender
        if event.button() == QtCore.Qt.RightButton:
            self.setStyleSheet('background-color: rgb(50,50,50)')
            return self

def main(*args, **kwargs):
    if cmds.window(window_object, query=True, exists=True):
        cmds.deleteUI(window_object)

    win = Scroll()
    win.show()
#END main()

main()