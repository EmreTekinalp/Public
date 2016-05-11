"""Created on 2014/02/21
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: A group for editing float values, consisting of a slider and a spinbox.

"""
from functools import partial
from PySide import QtGui, QtCore


class FloatSliderGroup(QtGui.QWidget):
    """Provides a float slider group composed of a QDoubleSpinbox and a QSlider."""
    def __init__(self):
        super(FloatSliderGroup, self).__init__()
        self.setLayout(QtGui.QHBoxLayout())
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.spinbox = QtGui.QDoubleSpinBox()
        self.slider.valueChanged.connect(partial(self.value_changed,
                                                 self.slider, self.spinbox))
        self.spinbox.valueChanged.connect(partial(self.value_changed,
                                                 self.spinbox, self.slider))
        self.layout().addWidget(self.spinbox)
        self.layout().addWidget(self.slider)
    # end def __init__

    def value_changed(self, src, target, value):
        """Changes the values of the spinbox and the slider of a float slider.
        @param src: the gui element that was edited by the user
        @param target: The gui element that has to be updated
        @param value: The value of the edited gui element
        @type src: QSlider or QDoubleSpinBox
        @type target: QSlider or QDoubleSpinBox
        @type value: int or float

        """
        if type(src) == QtGui.QSlider:
            value = float(src.value()) / float(src.maximum())
        else:
            value *= target.maximum()
        target.setValue(value)
    # end def value_changed

    def set_minimum(self, minimum):
        """Sets the minimum of slider and spinbox.
        @param minimum: the minimum

        """
        self.spinbox.setMinimum(minimum)
        self.slider.setMinimum(minimum * self.slider.maximum())
    # end def set_minimum

    def set_maximum(self, maximum):
        """Sets the maximum of slider and spinbox.
        @param maximum: the maximum

        """
        self.spinbox.setMaximum(maximum)
        self.slider.setMaximum(maximum * 10 ** self.spinbox.decimals())
    # end def set_maximum

    def set_decimals(self, decimals):
        """Sets the number of decimals the spinbox displays.
        @param decimals: the number of decimals

        """
        self.spinbox.setDecimals(decimals)
    # end def set_decimals

    def set_value(self, value):
        """Sets the value of the spinbox.
        @param value: the value

        """
        self.spinbox.setValue(value)
    # end def set_value
# end class FloatSldierGroup
