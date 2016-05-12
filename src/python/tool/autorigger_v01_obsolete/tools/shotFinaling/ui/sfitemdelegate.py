"""Created on 2014/02/20
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: Custom item delegates for shotfinaling models

"""
from functools import partial
from PySide import QtCore, QtGui
import floatslidergroup
import timeline


class SFItemDelegate(QtGui.QStyledItemDelegate):
    """The QStyledItemDelegate for the shotfinaling items.
    @param parent: the parent widget
    @param macontroller: the controller for the interactions with maya

    """
    def __init__(self, parent=None, macontroller=None):
        super(SFItemDelegate, self).__init__(parent)
        self.macontroller = macontroller
    # end def __init__

    def paint(self, painter, option, index):
        """Paints specific widgets depending on the column.
        * button to show the keys
        * slider for the blend value
        * button to switch between displaying the original and sculpt
        * delete button
        * timeline
        @param painter: the painter
        @param option: options for the painter
        @param index: the model index

        """
        if index.column() == 1:
            if self.parent().indexWidget(index) is None:
                btn = QtGui.QToolButton()
                btn.setText('Show')
                btn.clicked.connect(partial(self.macontroller.select_sculpt_transform, index))
                self.parent().setIndexWidget(index, btn)
        elif index.column() == 2:
            if self.parent().indexWidget(index) is None:
                blendvalue_widget = self.create_blendvalue_widget(index)
                self.parent().setIndexWidget(index, blendvalue_widget)
        elif index.column() == 3:
            if self.parent().indexWidget(index) is None:
                btn = QtGui.QToolButton()
                btn.setCheckable(True)
                checked = self.parent().model().itemFromIndex(index).data(QtCore.Qt.DisplayRole)
                if checked:
                    btn.setText('Sculpt')
                    btn.setStyleSheet('QToolButton{color:#000;}')
                else:
                    btn.setText('Original')
                    btn.setStyleSheet('QToolButton{color:#ddd;}')
                btn.setChecked(checked)
                btn.clicked.connect(partial(self.macontroller.change_visibility, index, self.parent()))
                self.parent().setIndexWidget(index, btn)
        elif index.column() == 5:
            if self.parent().indexWidget(index) is None:
                btn = QtGui.QToolButton()
                btn.setText('X')
                btn.setStyleSheet('QToolButton{background-color:#900; color:#fff;}'
                                  'QToolButton:hover{background-color:#c00;}'
                                  'QToolButton:pressed{background-color:#f00;}')
                btn.clicked.connect(partial(self.macontroller.remove_row, index, self.parent(), btn))
                self.parent().setIndexWidget(index, btn)
        elif index.column() == 6:
            if self.parent().indexWidget(index) is None:
                tl = timeline.Timeline(table=self.parent(), item=index.model().itemFromIndex(index))
                self.parent().setIndexWidget(index, tl)
                cw = self.parent().columnWidth(6)
                self.parent().horizontalHeader().resizeSection(6, cw+10)
                self.parent().horizontalHeader().resizeSection(6, cw)
        else:
            return QtGui.QStyledItemDelegate.paint(self, painter, option, index)
    # end def paint

    def create_blendvalue_widget(self, index):
        """Creates the blend value widget, consisting of a parent widget,
        a floatslidergroup and a button for keyframing
        @param index: the index of the modelitem
        @return: the blend value's parent widget

        """
        sld_wid = QtGui.QWidget()
        sld_wid.setLayout(QtGui.QHBoxLayout())
        sld_wid.layout().setSpacing(0)
        fsg = floatslidergroup.FloatSliderGroup()
        fsg.set_minimum(0)
        fsg.set_maximum(1)
        fsg.set_decimals(3)
        fsg.set_value(1)
        fsg.setMinimumHeight(36)
        fsg.layout().setSpacing(0)
        fsg.spinbox.valueChanged.connect(partial(self.macontroller.change_blend_value, index, fsg.spinbox, self.parent()))
        key_btn = QtGui.QToolButton()
        key_btn.setIcon(QtGui.QIcon(":/setKeySmall.png"))
        key_btn.clicked.connect(partial(self.macontroller.set_keyframe, index))
        sld_wid.layout().addWidget(fsg)
        sld_wid.layout().addWidget(key_btn)
        return sld_wid
    # end def create_blendvalue_widget

    def createEditor(self, parent, option, index):
        """Saves the original name of the sculpt before editing begins to be able
        to rename the maya object later.
        @param parent: the parent
        @param option: options
        @param index: the model item index

        """
        if index.column() == 0:
            self.macontroller.save_name(index)
        return QtGui.QStyledItemDelegate.createEditor(self, parent, option, index)
    # end def createEditor

    def setModelData(self, editor, model, index):
        """ Sets the model data when editing is finished. If the name has been
        edited, calls the macontroller to rename the sculpt.
        @param editor: the editor widget
        @param model: the model
        @param index: the model item index

        """
        QtGui.QStyledItemDelegate.setModelData(QtGui.QStyledItemDelegate(), editor, model, index)
        if index.column() == 0:
            self.macontroller.rename(index)
    # end def setModelData
# end NodeItemDelegate


class SFItemStaticDelegate(QtGui.QStyledItemDelegate):
    """A QStyledItemDelegate for the shotfinaling items that are not to be
    altered by the user by preventing the editor to be created.
    @param parent: the parent widget

    """
    def __init__(self, parent=None):
        super(SFItemStaticDelegate, self).__init__(parent)
    # end def __init__

    def createEditor(self, parent, option, index):
        """Returns intentionally None, so that the item can't be edited."""
        return None
    # end def createEditor
# end class SFItemStaticDelegate
