"""
!!!!SHIT WORKS!!!! :)
"""


import shiboken
from PySide import QtGui, QtCore
from maya import cmds, OpenMayaUI


window_object = "TestUIObject"
window_title = "TestUI"

def getMayaWindow():
    """
    Get the main Maya window as a QtGui.QMainWindow instance
    @return: QtGui.QMainWindow instance of the top level Maya windows
    """
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    if ptr is not None:
        return shiboken.wrapInstance(long(ptr), QtGui.QWidget)


class DynamicButton(QtGui.QDialog):
    def __init__(self, parent = getMayaWindow()):
        super(DynamicButton, self).__init__(parent)

        #--- vars
        self.buttons = list()

        #--- methods
        self.__create()
    #END __init__()

    def __setup_ui(self):
        self.setWindowTitle(window_title)
        self.setObjectName(window_object)
        self.setGeometry(600,300,300,200)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    #END __setup_ui()

    def create_button(self):
        self.create_btn = QtGui.QPushButton("create")
        self.create_btn.setObjectName('creator')
    #END create_button()

    def setup_layout(self):
        self.vbox = QtGui.QVBoxLayout()

        self.vbox.addWidget(self.create_btn)
        self.vbox.addStretch()

        self.setLayout(self.vbox)
    #END setup_layout()

    def create_new(self):
        hbox = QtGui.QHBoxLayout()
        text = QtGui.QLabel('changeMe')
        btn = QtGui.QPushButton('pressMe')
        hbox.addWidget(text)
        hbox.addWidget(btn)
        self.vbox.addLayout(hbox)
        #--- add button and label into list and append it
        res = [btn, text]
        self.buttons.append(res)

        #--- connect signal
        btn.clicked.connect(self.change_name)
    #END create_new()

    def change_name(self):
        for i in self.buttons:
            if i[0] == self.sender():
                res = self.add_prompt_dialog()
                i[1].setText(res)
    #END change_name()

    def add_prompt_dialog(self):
        text = None
        result = cmds.promptDialog(title='Create new...',
                                   message='Enter Name:',
                                   button=['OK', 'Cancel'],
                                   defaultButton='OK',
                                   cancelButton='Cancel',
                                   dismissString='Cancel')
        if result == 'OK':
            text = cmds.promptDialog(query=True, text=True)
        return text
    #END add_prompt_dialog()

    def connect_signals(self):
        self.create_btn.clicked.connect(self.create_new)
    #END connect_signals()

    def __create(self):
        #--- setup ui
        self.__setup_ui()

        #--- create button
        self.create_button()

        #--- setup layout
        self.setup_layout()

        #--- connect signals
        self.connect_signals()
    #END __create()
#END DynamicButton()


class DragAndDrop(QtGui.QDialog):
    def __init__(self, parent = getMayaWindow()):
        super(DragAndDrop, self).__init__(parent)

        self.setAcceptDrops(True)

        #--- vars
        self.buttons = list()
        self.framehbox = list()
        self.framelist = list()

        #--- methods
        self.__create()
    #END __init__()

    def __setup_ui(self):
        self.setWindowTitle(window_title)
        self.setObjectName(window_object)
        self.setGeometry(600,300,300,200)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    #END __setup_ui()

    def create_button(self):
        self.create_btn = QtGui.QPushButton("create")
        self.create_btn.setObjectName('creator')
        self.up_btn = QtGui.QPushButton("move up")
        self.down_btn = QtGui.QPushButton("down up")
    #END create_button()

    def setup_layout(self):
        self.vbox = QtGui.QVBoxLayout()

        self.vbox.addWidget(self.create_btn)
        self.vbox.addStretch()
        self.vbox.addWidget(self.up_btn)
        self.vbox.addWidget(self.down_btn)
        self.setLayout(self.vbox)
    #END setup_layout()'

    def create_new(self):
        hbox = QtGui.QHBoxLayout()
        self.hboxf = QtGui.QHBoxLayout()
        text = QtGui.QLabel('changeMe')
        btn = QtGui.QPushButton('pressMe')
        hbox.addWidget(text)
        hbox.addWidget(btn)

        #--- create and setup frame
        self.frame = Frame(self, self.framelist)
        self.frame.setStyleSheet('background-color: rgb(50,50,50)')
        self.frame.setLayout(hbox)
        self.hboxf.addWidget(self.frame)
        self.framehbox.append(self.hboxf)
        self.framelist.append(self.frame)

        self.vbox.insertLayout(1, self.hboxf)
        #--- add button and label into list and append it
        res = [btn, text]
        self.buttons.append(res)

        #--- connect signal
        btn.clicked.connect(self.change_name)
    #END create_new()

    def change_name(self):
        for i in self.buttons:
            if i[0] == self.sender():
                res = self.add_prompt_dialog()
                i[1].setText(res)
    #END change_name()

    def add_prompt_dialog(self):
        text = None
        result = cmds.promptDialog(title='Create new...',
                                   message='Enter Name:',
                                   button=['OK', 'Cancel'],
                                   defaultButton='OK',
                                   cancelButton='Cancel',
                                   dismissString='Cancel')
        if result == 'OK':
            text = cmds.promptDialog(query=True, text=True)
        return text
    #END add_prompt_dialog()

    def move_up(self):
        obj = self.sender()
        idx = self.vbox.indexOf(obj)
        print idx
        old_index = 1
        new_index = 0
        for i, frame in enumerate(self.framelist):
            if frame.styleSheet() == 'background-color: rgb(60,60,60)':
                old_index = i
                new_index = i - 1
        item = self.framelist[old_index]
        self.framelist.pop(old_index)
        self.framelist.insert(new_index, item)
        print self.framelist
#         item = self.framehbox[old_index]
#         self.framehbox.pop(old_index)
#         self.framehbox.insert(new_index, item)
# #         self.framehbox[new_index].addWidget(new_index, self.framelist[new_index])
#         self.vbox.insertLayout(new_index, self.framehbox[new_index])
    #END move_up()

    def deleteItems(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.deleteItems(item.layout())

    def moveLightItem(self, direction):
        # the sender should always be a LightItem instance
        obj = self.sender()
        print "Move LightItem %s in direction %s" % (obj, direction)

        # what is the current index of the widget in the layout?
        idx = self.v_layout.indexOf(obj)
        print 'idx', idx
        if idx == -1:
            print "Widget is not in the layout:", obj
            return

        if direction == QtCore.Qt.Key_Up:
            # next index down
            idx = max(idx-1, 0)

        elif direction == QtCore.Qt.Key_Down:
            # next index up
            idx = min(idx+1, self.v_layout.count()-1)

        else:
            print "Not a key up or down"
            return

        # will insert the widget into a differnt index of the layout
        self.v_layout.insertWidget(idx, obj)

    def move_down(self):
        pass
    #END move_down()

    def connect_signals(self):
        self.create_btn.clicked.connect(self.create_new)
        self.up_btn.clicked.connect(self.move_up)
        self.down_btn.clicked.connect(self.move_down)
    #END connect_signals()

    def __create(self):
        #--- setup ui
        self.__setup_ui()

        #--- create button
        self.create_button()

        #--- setup layout
        self.setup_layout()

        #--- connect signals
        self.connect_signals()
    #END __create()
#END DragAndDrop()


class Frame(QtGui.QFrame):
    def __init__(self, parent, framelist):
        super(Frame, self).__init__(parent)
        self.setMouseTracking(True)
        self.framelist = framelist

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.setStyleSheet('background-color: rgb(60,60,60)')
            for i in self.framelist:
                if not self == i:
                    i.setStyleSheet('background-color: rgb(50,50,50)')

def main(*args, **kwargs):
    if cmds.window(window_object, query=True, exists=True):
        cmds.deleteUI(window_object)

    win = DragAndDrop()
    win.show()
#END main()


class RenderManagement(QtGui.QDialog):
    def __init__(self, parent = getMayaWindow()):
        super(RenderManagement, self).__init__(parent)
        self.v_layout = QtGui.QVBoxLayout(self)

        # Create 5 dynamic items
        for i in xrange(5):
            item = LightItem()
            item.setTitle("LightItem%d" % i)
            self.v_layout.addWidget(item)

            # watch for the moveRequested signal on each item
            item.moveRequested.connect(self.moveLightItem)

    def moveLightItem(self, direction):

        # the sender should always be a LightItem instance
        obj = self.sender()
        print "Move LightItem %s in direction %s" % (obj, direction)

        # what is the current index of the widget in the layout?
        idx = self.v_layout.indexOf(obj)
        print 'idx', idx, direction
        if idx == -1:
            print "Widget is not in the layout:", obj
            return

        if direction == QtCore.Qt.Key_Up:
            # next index down
            idx = max(idx-1, 0)

        elif direction == QtCore.Qt.Key_Down:
            # next index up
            idx = min(idx+1, self.v_layout.count()-1)

        else:
            print "Not a key up or down"
            return

        # will insert the widget into a differnt index of the layout
        print idx, obj
        self.v_layout.insertWidget(idx, obj)


class LightItem(QtGui.QGroupBox):

    # custom signal, emitting the Qt.Key_X
    moveRequested = QtCore.Signal(int)

    def __init__(self):
        super(LightItem, self).__init__()

        # Generic layout of widgets
        self.v_layout = QtGui.QVBoxLayout(self)
        self.v_layout.setContentsMargins(2,2,2,2)

        self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)

        self.left = QtGui.QGroupBox('Left')

        self.lineEdit = QtGui.QLineEdit()
        self.left_layout = QtGui.QVBoxLayout(self.left)
        self.left_layout.addWidget(self.lineEdit)

        self.right = QtGui.QGroupBox('Right')

        self.splitter.addWidget(self.left)
        self.splitter.addWidget(self.right)

        self.v_layout.addWidget(self.splitter)

        # have LightItem watch all events on the QLineEdit, 
        # so that we do not have to subclass QLineEdit
        self.lineEdit.installEventFilter(self)

    def eventFilter(self, obj, event):
        # Only watch for specific Key presses on the QLineEdit
        # Everything else is pass-thru
        if obj is self.lineEdit and event.type() == event.KeyPress:
            key = event.key()
            if key in (QtCore.Qt.Key_Up, QtCore.Qt.Key_Down):
                print "Emitting moveRequested() for obj", obj
                self.moveRequested.emit(event.key())
                return True

        return False

def mainy(*arg, **kwargs):
    manager = RenderManagement()
    if cmds.window(manager.objectName(), exists=True):
        cmds.deleteUI(manager.objectName())
    manager.resize(800,600)
    manager.show()
main()