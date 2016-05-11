"""Created on 2014/02/20
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: Handles interactions between the shotfinaling ui and maya

"""
import os
import sys
from functools import partial
from PySide import QtGui
from maya import cmds, OpenMayaAnim
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'shotFinaling'))
import SFTOOL02_UPDATE as shotfinaling
import floatslidergroup


class MaController():
    """A controller to handle interactions between the shotfinaling ui and maya.
    @param parent: the parent widget for this controller (the shotinfinaling ui)
    """
    def __init__(self, parent):
        self.saved_name = None
        self.parent = parent
    # end def __init__

    def select_object(self, mesh):
        """Selects the given mesh.
        @param mesh: the mesh to select.

        """
        cmds.select(mesh, r=True)
    # end def select_object

    def edit_envelope(self, slider, mesh, table, value):
        """Edits the envelope value.
        @param slider: the envelope slider
        @param mesh: the mesh the envelope refers to
        @param table: the table the slider refers to
        @param value: the value of the slider

        """
        ctl_grp = cmds.listConnections('%s.v' % mesh)[0]
        cmds.setAttr('%s.ENVELOPE' % ctl_grp, value)
        for row in range(table.model().rowCount()):
            index = table.model().index(row, 3)
            btn = table.indexWidget(index)
            btn.setChecked(False)
            self.change_visibility(index, table)
        # end for row in range(table.rowCount())
    # end def edit_envelope

    def select_sculpt_transform(self, index):
        """Selects the transform of the sculpt.
        @param index: the model item index of the sculpt

        """
        cmds.select(index.model().name(index.row()))
    # end def select_sculpt_transform

    def save_name(self, index):
        """Saves the text of the clicked item in a variable to be able to use
        it's old value in the rename process.
        @param index: the model item index of the sculpt

        """
        self.saved_name = index.model().name(index.row())
    # end def save_name

    def rename(self, index):
        """Renames the given item and the corresponding transform.
        @param index: the model item index of the sculpt

        """
        cmds.rename(self.saved_name, index.model().name(index.row()))
    # end def rename

    def change_blend_value(self, index, spinbox, table, value):
        """Changes the blend value of the given slider.
        @param index: the model item index
        @param spinbox: the splinbox of the blendvalue
        @param table: the table the sculpt resides in
        @param value: the value of the spinbox

        """
        cmds.setAttr('%s.blendValue' % index.model().name(index.row()), spinbox.value())
        btn = table.indexWidget(index.model().index(index.row(), 3))
        if spinbox.value() < 1:
            btn.setChecked(False)
        self.change_visibility(index.model().index(index.row(), 3), table)
        cmds.select(self.get_original(index), r=True)
    # end def change_blend_value

    def set_keyframe(self, index):
        """Sets a keyframe on the current frame on the blend value of it's sculpt.
        @param index: the model item index

        """
        cmds.setKeyframe(index.model().name(index.row()), at='blendValue')
    # end def set_keyframe

    def change_visibility(self, index, table):
        """Changes the visibility of the sculpts.
        @param index: the model item index
        @param table: the table, where the visibility is to be changed

        """
        show = False
        for row in range(index.model().rowCount()):
            curindex = index.model().index(row, 3)
            button = table.indexWidget(curindex)
            if button is None:
                continue
            if row == index.row():
                if not button.isChecked():
                    button.setText('Original')
                    button.setStyleSheet('QToolButton{color:#ddd;}')
                    self.show_hide_sculpt(table, curindex, False)
                    show = True
                else:
                    button.setText('Sculpt')
                    button.setStyleSheet('QToolButton{color:#000;}')
                    self.show_hide_sculpt(table, curindex, True)
            else:
                button.setChecked(False)
                button.setText('Original')
                button.setStyleSheet('QToolButton{color:#ddd;}')
                self.show_hide_sculpt(table, curindex, False)
        # end for row in range(index.model().rowCount())
        original = self.get_original(index)
        self.show_original(index, show)
        if not show:
            if len(cmds.ls(sl=True, l=True)) > 0:
                if cmds.ls(sl=True, l=True)[0] != original:
                    cmds.select(original, r=True)
    # end def change_visiblity

    def get_original(self, index):
        """Returns the original mesh by backtracing the connections.
        @param index: the model item index of the sculpt

        """
        name = index.model().name(index.row())
        bls = cmds.listConnections('%s.blendValue' % name, type='blendShape')[0]
        return cmds.listConnections('%s.outputGeometry[0]' % bls)[0]
    # end def get_original

    def show_original(self, index, show):
        """Shows the original mesh of the given obj of the given character.
        @param index: the model item index
        @param show: whether to show or hide the original mesh

        """
        ctl_grp = cmds.listConnections('%s.v' % self.get_original(index), p=True)[0]
        cmds.setAttr(ctl_grp, show)
    # end def show_original

    def show_hide_sculpt(self, table, index, show):
        """Hides the sculpt in the given row of the given table.
        @param table: the table holding the sculpt
        @param index: the model item index
        @param show: whether to show or hide the sculpt

        """
        cmds.setAttr('%s.sculpt' % index.model().name(index.row()), show)
    # end def show_hide_sculpt

    def remove_row(self, index, table, btn):
        """Removes the given row.
        @param index: the model item index
        @param table: the table holding the row
        @todo: remove tabs if empty

        """
        for i in range(index.model().rowCount()):
            wid = table.indexWidget(index.model().index(i, index.column()))
            if wid is btn:
                sculpt = cmds.listConnections('%s.sculpt' % index.model().name(i))[0]
                cmds.select(sculpt, r=True)
                shotfinaling.RemoveShotFinal()
                index.model().removeRow(i)
                break
        # end for i in range(index.model().rowCount())
    # end def remove_row

    def blend_value_callback(self, func, clientData):
        """The function that gets called when the callback is executed on time
        change. It updates the values of the spinboxes according to the
        blendValues of the corresponding sculpts.
        @param func:
        @param clientData:

        """
        try:
            for info in cmds.ls('SF_INFO_NODE*', type='transform'):
                for tab in self.parent.tabs:
                    table = self.parent.tabs[tab][1]
                    model = table.model()
                    for row in range(model.rowCount()):
                        index = model.index(row, 2)
                        wid = table.indexWidget(index)
                        sld, spn, slidergroup = self.get_slider(wid)
                        value = cmds.getAttr('%s.blendValue' % model.name(row))
                        spn.valueChanged.disconnect()
                        sld.valueChanged.disconnect()
                        spn.setValue(value)
                        sld.setValue(value * float(sld.maximum()))
                        spn.valueChanged.connect(partial(self.change_blend_value, index, spn, table))
                        spn.valueChanged.connect(partial(slidergroup.value_changed, spn, sld))
                        sld.valueChanged.connect(partial(slidergroup.value_changed, sld, spn))
                    # end for row in range(model.rowCount())
                # end for tab in self.parent.tabs
            # end for info in cmds.ls('SF_INFO_NODE*', type='transform')
        except Exception as err:
            print 'Shotfinal Error message: %s' % err
    # end def blend_value_callback

    def get_slider(self, widget):
        """Returns the slider widgets inside the given widget.
        @param widget: the widget, to search in
        @return: the slider widget, the spinbox widget and the slidergroup widget

        """
        slider = None
        spinbox = None
        layout = widget.layout()
        for i in range(layout.count()):
            item = layout.itemAt(i).widget()
            if isinstance(item, floatslidergroup.FloatSliderGroup):
                slidergroup = item
                innerlayout = item.layout()
                for j in range(innerlayout.count()):
                    inneritem = innerlayout.itemAt(j).widget()
                    if isinstance(inneritem, QtGui.QSlider):
                        slider = inneritem
                    if isinstance(inneritem, QtGui.QDoubleSpinBox):
                        spinbox = inneritem
                # end for j in range(innerlayout.count())
                break
        # end for i in range(layout.count())
        return slider, spinbox, slidergroup
    # end def get_slider

    def key_callback(self, attributes, clientData):
        """The callback updates the timelines when keys are created, moved or deleted.
        Everything is put into a try statement for general safety reasons
        @param attributes: edited attributes
        @param clientData: additionalData, not used by the onionSkin, so always
                           defaults to None
        @type clientData: None
        """
        try:
            for i in range(attributes.length()):
                attribute = attributes[i]
                keyframe_delta = OpenMayaAnim.MFnKeyframeDelta(attribute)
                animcurve = OpenMayaAnim.MFnAnimCurve(keyframe_delta.paramCurve())
                if 'blendValue' not in animcurve.name():
                    continue
                obj = cmds.listConnections(animcurve.name())[0]
                bls = cmds.listConnections('%s.blendValue' % obj, type='blendShape')[0]
                tab = cmds.listConnections('%s.outputGeometry[0]' % bls)[0]
                table = self.parent.tabs[tab][1]
                model = table.model()
                row = model.findItems(obj, column=0)[0].row()
                index = model.index(row, 6)
                tl = table.indexWidget(index)
                if tl is not None:
                    tl.refresh_buttons(animcurve)
            # end for i in range(attributes.length()-1)
        except Exception as err:
            print 'Shotfinal Error message: %s' % err
    # end def key_callback

    def pan(self):
        """Enters the pan tool."""
        cmds.PanZoomTool()
        cmds.panZoomCtx('PanZoomContext', e=True, panMode=True)
    # end def pan

    def zoom(self):
        """Enters the zoom tool."""
        cmds.PanZoomTool()
        cmds.panZoomCtx('PanZoomContext', e=True, zoomMode=True)
    # end def zoom

    def reset_pan_zoom(self):
        """Resets the pan and zoom attribute of all cameras."""
        for camera in cmds.ls(ca=True):
            cmds.setAttr('%s.panZoomEnabled' % camera, 0)
        cmds.SelectTool()
    # end def reset_pan_zoom
# end class MaController
