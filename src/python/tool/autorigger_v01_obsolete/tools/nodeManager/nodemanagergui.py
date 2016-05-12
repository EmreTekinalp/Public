"""
This is the ui for the infoBox
"""

import os
import sys
from PySide import QtGui, QtCore
from maya import cmds, OpenMaya
from tools import infoBox
from fundamentals import node
reload(node)

sys.path.append('C:\Users\Isaac Clark\Documents\GitHub\AutoRigger')
from tools.shotFinaling.ui import pysideconvenience
uifilepath = 'C:/Users/Isaac Clark/Documents/GitHub/AutoRigger/tools/nodeManager/ui/nodemanager.ui'
form_class, base_class = pysideconvenience.load_ui_type(uifilepath)


class NodeManagerUI(base_class, form_class):
    '''
    This displays a ui for the infoBox tool.
    '''
    def __init__(self, parent=pysideconvenience.get_maya_window()):
        super(NodeManagerUI, self).__init__(parent)
        self.setupUi(self)

        #vars
        self.prefix = None
        self.name   = None
        self.suffix = None

        self.composed_name = None
        self.node = None
        self.node_list = list()

        self.attr1 = None
        self.attr2 = None
        self.attr3 = None
        self.attr4 = None
        self.attr5 = None
        self.attr6 = None
        self.attr7 = None
        self.attr8 = None
        self.attr9 = None

        self.value1 = None
        self.value2 = None
        self.value3 = None
        self.value4 = None
        self.value5 = None
        self.value6 = None
        self.value7 = None
        self.value8 = None
        self.value9 = None

        self.lock = list()
        self.code_information = list()

        #methods
        self.__setup()
    #END def __init__()

    def connect_signals(self):
        #--- this method connects the signals
        self.node_CMB.currentIndexChanged.connect(self.change_attributes)
        self.connect(self.create_BTN, QtCore.SIGNAL('released()'), self.create_node)
        self.connect(self.generate_BTN, QtCore.SIGNAL('released()'), self.generate_code)
    #END def connect_signals()

    def setup_dropdown_menu(self):
        #--- this method setups the dropDown menu
        nd = node.Node()
        methods = dir(nd)
        for m in methods:
            if not m.startswith('__'):
                self.node_list.append(m)
        #--- add the method nodes to the dropDown list
        self.node_CMB.addItems(self.node_list)
    #END def setup_dropdown_menu()

    def get_description(self):
        #--- this method gets the proper description
        self.prefix = self.prefix_FIL.text()
        self.name = self.name_FIL.text()
        self.suffix = self.suffix_FIL.text()

        if self.prefix:
            if self.name:
                self.composed_name = self.prefix + '_' + self.name
            else:
                self.composed_name = self.prefix
        else:
            self.composed_name = self.name
    #END def get_description()

    def get_attribute_info(self):
        #--- this method gets the attribute label infos
        self.attr1 = self.attr1_TXT.text()
        self.attr2 = self.attr2_TXT.text()
        self.attr3 = self.attr3_TXT.text()
        self.attr4 = self.attr4_TXT.text()
        self.attr5 = self.attr5_TXT.text()
        self.attr6 = self.attr6_TXT.text()
        self.attr7 = self.attr7_TXT.text()
        self.attr8 = self.attr8_TXT.text()
        self.attr9 = self.attr9_TXT.text()
    #END def get_attribute_info

    def get_value_info(self):
        #--- this method gets the attribute label infos
        self.value1 = self.value1_FIL.text()
        self.value2 = self.value2_FIL.text()
        self.value3 = self.value3_FIL.text()
        self.value4 = self.value4_FIL.text()
        self.value5 = self.value5_FIL.text()
        self.value6 = self.value6_FIL.text()
        self.value7 = self.value7_FIL.text()
        self.value8 = self.value8_FIL.text()
        self.value9 = self.value9_FIL.text()
    #END def get_value_info

    def get_box_info(self):
        #--- this method setups the lock button
        self.get_attribute_info()
        #--- checkbox list
        locks = [self.lock1_BOX, self.lock2_BOX, self.lock3_BOX, self.lock4_BOX,
                 self.lock5_BOX, self.lock6_BOX, self.lock7_BOX, self.lock8_BOX,
                 self.lock9_BOX]
        attrs = [self.attr1, self.attr2, self.attr3, self.attr4, self.attr5, 
                 self.attr6, self.attr7, self.attr8, self.attr9]
        for lock, attr in zip(locks, attrs):
            if lock.isChecked():
                self.lock.append(attr)
    #END def get_box_info()

    def hide_information(self, index=1):
        #--- this method hides unnecessary information
        attrs = [self.attr1_TXT, self.attr2_TXT, self.attr3_TXT, self.attr4_TXT,
                 self.attr5_TXT, self.attr6_TXT, self.attr7_TXT, self.attr8_TXT,
                 self.attr9_TXT]
        value = [self.value1_FIL, self.value2_FIL, self.value3_FIL, self.value4_FIL,
                 self.value5_FIL, self.value6_FIL, self.value7_FIL, self.value8_FIL,
                 self.value9_FIL]
        locks = [self.lock1_BOX, self.lock2_BOX, self.lock3_BOX, self.lock4_BOX,
                 self.lock5_BOX, self.lock6_BOX, self.lock7_BOX, self.lock8_BOX,
                 self.lock9_BOX]        
        for a, v, l in zip(attrs[(index-1):], value[(index-1):], locks[(index-1):]):
            a.hide()
            v.hide()
            l.hide()
    #END def hide_information()

    def show_information(self):
        #--- this method shows all the information
        self.attr1_TXT.show()
        self.attr2_TXT.show()
        self.attr3_TXT.show()        
        self.attr4_TXT.show()
        self.attr5_TXT.show()
        self.attr6_TXT.show()
        self.attr7_TXT.show()        
        self.attr8_TXT.show()
        self.attr9_TXT.show()

        self.value1_FIL.show()
        self.value2_FIL.show()
        self.value3_FIL.show()
        self.value4_FIL.show()
        self.value5_FIL.show()
        self.value6_FIL.show()
        self.value7_FIL.show()
        self.value8_FIL.show()
        self.value9_FIL.show()

        self.lock1_BOX.show()
        self.lock2_BOX.show()
        self.lock3_BOX.show()
        self.lock4_BOX.show()
        self.lock5_BOX.show()
        self.lock6_BOX.show()
        self.lock7_BOX.show()
        self.lock8_BOX.show()
        self.lock9_BOX.show()
    #END show_information

    def clear_all(self):
        #--- this method clears the selections
        #--- clear naming fields
        self.prefix_FIL.clear()
        self.name_FIL.clear()
        self.suffix_FIL.clear()

        #--- clear value fields
        self.value1_FIL.clear()
        self.value2_FIL.clear()
        self.value3_FIL.clear()
        self.value4_FIL.clear()
        self.value5_FIL.clear()
        self.value6_FIL.clear()
        self.value7_FIL.clear()
        self.value8_FIL.clear()
        self.value9_FIL.clear()

        #--- clear checkBoxes
        self.lock1_BOX.setChecked(False)
        self.lock2_BOX.setChecked(False)
        self.lock3_BOX.setChecked(False)
        self.lock4_BOX.setChecked(False)
        self.lock5_BOX.setChecked(False)
        self.lock6_BOX.setChecked(False)
        self.lock7_BOX.setChecked(False)
        self.lock8_BOX.setChecked(False)
        self.lock9_BOX.setChecked(False)

        self.lock = list()
    #END def clear_all

    def change_attributes(self):
        #--- this method changes the attributes
        #--- clear all
        self.clear_all()
        #--- show information
        self.show_information()
        #--- create code info list
        self.code_information = list()
        #--- get current node name an store it
        current_node = self.node_CMB.currentText()
        self.node = current_node
        if current_node == 'blendColors':
            self.attr1_TXT.setText('blender')
            self.attr2_TXT.setText('color1R')
            self.attr3_TXT.setText('color1G')
            self.attr4_TXT.setText('color1B')
            self.attr5_TXT.setText('color2R')
            self.attr6_TXT.setText('color2G')
            self.attr7_TXT.setText('color2B')
            self.hide_information(8)

        elif current_node == 'condition':
            self.get_attribute_info()
            self.attr1_TXT.setText('firstTerm')
            self.attr2_TXT.setText('secondTerm')
            self.attr3_TXT.setText('operation')
            self.attr4_TXT.setText('colorIfTrueR')
            self.attr5_TXT.setText('colorIfTrueG')
            self.attr6_TXT.setText('colorIfTrueB')
            self.attr7_TXT.setText('colorIfFalseR')
            self.attr8_TXT.setText('colorIfFalseG')
            self.attr9_TXT.setText('colorIfFalseB')

        elif current_node == 'distanceBetween':
            self.get_attribute_info()
            self.attr1_TXT.setText('point1')
            self.attr2_TXT.setText('point2')
            self.attr3_TXT.setText('inMatrix1')
            self.attr4_TXT.setText('inMatrix2')
            self.hide_information(5)

        elif current_node == 'eLocator':
            self.get_attribute_info()
            self.attr1_TXT.setText('size')
            self.attr2_TXT.setText('color')
            self.hide_information(3)

        elif current_node == 'follicle':
            self.get_attribute_info()
            self.attr1_TXT.setText('parameterU')
            self.attr2_TXT.setText('parameterV')
            self.attr3_TXT.setText('parent')
            self.attr4_TXT.setText('show')
            self.hide_information(5)

        elif current_node == 'locator':
            self.get_attribute_info()
            self.attr1_TXT.setText('position')
            self.attr2_TXT.setText('rotation')
            self.attr3_TXT.setText('worldSpace')
            self.hide_information(4)

        elif current_node == 'mirrorSwitch':
            self.get_attribute_info()
            self.attr1_TXT.setText('mirror')
            self.attr2_TXT.setText('mirrorAxis')
            self.hide_information(3)

        elif current_node == 'multDoubleLinear':
            self.get_attribute_info()
            self.attr1_TXT.setText('input1')
            self.attr2_TXT.setText('input2')
            self.hide_information(3)

        elif current_node == 'multiplyDivide':
            self.get_attribute_info()
            self.attr1_TXT.setText('operation')
            self.attr2_TXT.setText('input1X')
            self.attr3_TXT.setText('input1Y')
            self.attr4_TXT.setText('input1Z')
            self.attr5_TXT.setText('input2X')
            self.attr6_TXT.setText('input2Y')
            self.attr7_TXT.setText('input2Z')
            self.hide_information(8)

        elif current_node == 'plusMinusAverage':
            self.get_attribute_info()
            self.attr1_TXT.setText('operation')
            self.hide_information(2)

        elif current_node == 'remapValue':
            self.get_attribute_info()
            self.attr1_TXT.setText('inputValue')
            self.attr2_TXT.setText('inputMin')
            self.attr3_TXT.setText('inputMax')
            self.attr4_TXT.setText('outputMin')
            self.attr5_TXT.setText('outputMax')
            self.hide_information(6)

        elif current_node == 'reverse':
            self.get_attribute_info()
            self.attr1_TXT.setText('inputX')
            self.attr2_TXT.setText('inputY')
            self.attr3_TXT.setText('inputZ')
            self.hide_information(4)

        elif current_node == 'transform':
            self.get_attribute_info()
            self.attr1_TXT.setText('position')
            self.attr2_TXT.setText('parent')
            self.hide_information(3)

        else:
            self.get_attribute_info()
            self.hide_information(1)
    #END def change_attributes()

    def create_node(self):
        #--- this method gets the translation values
        nd = node.Node()
        #--- get proper naming
        self.get_description()
        #--- get attribute info
        self.get_attribute_info()
        #--- get value_info
        self.get_value_info()
        #--- get lock info
        self.get_box_info()
        #--- get dropDown info and call node function
        if self.node == 'addDoubleLinear':
            nd.addDoubleLinear(name = self.composed_name, suffix = self.suffix)
        elif self.node == 'addMatrix':
            nd.addMatrix(name = self.composed_name, suffix = self.suffix)
        elif self.node == 'aimConstraint':
            nd.aimConstraint(target = self.value1, 
                             source = self.value2, 
                             name = self.composed_name, 
                             suffix = self.suffix, 
                             aimVector = self.value3, 
                             upVector = self.value4, 
                             worldUpObject = self.value5, 
                             worldUpType = self.value6, 
                             skip = self.value7)
        elif self.node == 'angleBetween':
            nd.angleBetween(name = self.composed_name, suffix = self.suffix)
        elif self.node == 'arrayMapper':
            nd.arrayMapper(name = self.composed_name, suffix = self.suffix)    
        elif self.node == 'blendColors':
            nd.blendColors(name = self.composed_name,
                           suffix = self.suffix,
                           blender = self.value1, 
                           color1R = self.value2, 
                           color1G = self.value3, 
                           color1B = self.value4, 
                           color2R = self.value5, 
                           color2G = self.value6, 
                           color2B = self.value7, 
                           lockAttr = self.lock)
        elif self.node == 'blendTwoAttr':
            nd.blendTwoAttr(name = self.composed_name, suffix = self.suffix)
        elif self.node == 'bump2d':
            nd.bump2d(name = self.composed_name, suffix = self.suffix)            
        elif self.node == 'bump3d':
            nd.bump3d(name=self.composed_name, suffix = self.suffix)            
        elif self.node == 'choice':
            nd.choice(name=self.composed_name, suffix = self.suffix)            
        elif self.node == 'chooser':
            nd.chooser(name=self.composed_name, suffix = self.suffix)            
        elif self.node == 'clamp':
            nd.clamp(name=self.composed_name, suffix = self.suffix)            
        elif self.node == 'closestPointOnMesh':
            nd.closestPointOnMesh(name=self.composed_name, suffix = self.suffix)            
        elif self.node == 'closestPointOnSurface':
            nd.closestPointOnSurface(name=self.composed_name, suffix = self.suffix)            
        elif self.node == 'colorProfile':
            nd.colorProfile(name=self.composed_name, suffix = self.suffix)            
        elif self.node == 'composeMatrix':
            nd.composeMatrix(name=self.composed_name, suffix = self.suffix)            
        elif self.node == 'condition':
            nd.condition(name = self.composed_name, 
                         suffix = self.suffix,
                         firstTerm = self.value1, 
                         secondTerm = self.value2, 
                         operation = self.value3, 
                         colorIfTrueR = self.value4, 
                         colorIfTrueG = self.value5, 
                         colorIfTrueB = self.value6, 
                         colorIfFalseR = self.value7, 
                         colorIfFalseG = self.value8, 
                         colorIfFalseB = self.value9, 
                         lockAttr = self.lock)
        elif self.node == 'contrast':
            nd.contrast(name=self.composed_name, suffix = self.suffix)  
        elif self.node == 'curveInfo':
            nd.curveInfo(name=self.composed_name, suffix = self.suffix)  
        elif self.node == 'decomposeMatrix':
            nd.decomposeMatrix(name=self.composed_name, suffix = self.suffix)  
        elif self.node == 'distanceBetween':
            nd.distanceBetween(name=self.composed_name, 
                               suffix = self.suffix,
                               point1 = self.value1, 
                               point2 = self.value2, 
                               inMatrix1 = self.value3, 
                               inMatrix2 = self.value4, 
                               lockAttr = self.lock)  
        elif self.node == 'doubleSwitch':
            nd.doubleSwitch(name=self.composed_name, suffix = self.suffix)
        elif self.node == 'eLocator':
            nd.eLocator(name=self.composed_name, 
                        suffix = self.suffix,
                        size = self.value1, 
                        color = self.value2, 
                        lockAttr = self.lock)
        elif self.node == 'follicle':
            nd.follicle(name=self.composed_name, 
                        suffix = self.suffix,
                        parameterU = self.value1, 
                        parameterV = self.value2, 
                        parent = self.value3, 
                        show = self.value4, 
                        lockAttr = self.lock)
        elif self.node == 'frameCache':
            nd.frameCache(name=self.composed_name, suffix = self.suffix)
        elif self.node == 'gammaCorrect':
            nd.gammaCorrect(name=self.composed_name, suffix = self.suffix)
        elif self.node == 'heightField':
            nd.heightField(name=self.composed_name, suffix = self.suffix)
        elif self.node == 'hsvToRgb':
            nd.hsvToRgb(name=self.composed_name, suffix = self.suffix)        
        elif self.node == 'inverseMatrix':
            nd.inverseMatrix(name=self.composed_name, suffix = self.suffix)
        elif self.node == 'lightInfo':
            nd.lightInfo(name=self.composed_name, suffix = self.suffix)
        elif self.node == 'locator':
            nd.locator(name=self.composed_name, 
                       suffix = self.suffix,
                       position = self.value1, 
                       rotation = self.value2, 
                       worldSpace = self.value3, 
                       parent = self.value4)
        elif self.node == 'luminance':
            nd.luminance(name=self.composed_name, suffix = self.suffix)
        elif self.node == 'mirrorSwitch':
            nd.mirrorSwitch(name=self.composed_name, 
                            suffix = self.suffix,
                            mirror = self.value1, 
                            mirrorAxis = self.value2,
                            lockAttr = self.lock)
        elif self.node == 'multDoubleLinear':
            nd.multDoubleLinear(name=self.composed_name, 
                                suffix = self.suffix,
                                input1 = self.value1, 
                                input2 = self.value2, 
                                lockAttr = self.lock)    
        elif self.node == 'multiplyDivide':
            nd.multiplyDivide(name=self.composed_name, 
                              suffix = self.suffix,
                              operation = self.value1, 
                              input1X = self.value2, 
                              input1Y = self.value3, 
                              input1Z = self.value4, 
                              input2X = self.value5, 
                              input2Y = self.value6, 
                              input2Z = self.value7, 
                              lockAttr = self.lock)
        elif self.node == 'nearestPointOnCurve':
            nd.nearestPointOnCurve(name=self.composed_name, suffix = self.suffix)
        elif self.node == 'orientConstraint':
            nd.orientConstraint(name=self.composed_name, 
                                suffix = self.suffix,
                                objA = self.value1, 
                                objB = self.value2, 
                                maintainOffset = self.value3)
        elif self.node == 'parentConstraint':
            nd.parentConstraint(name=self.composed_name, 
                                suffix = self.suffix,
                                objA = self.value1, 
                                objB = self.value2, 
                                maintainOffset = self.value3,
                                lock = self.value4)
        elif self.node == 'particleSampler':
            nd.particleSampler(name=self.composed_name, suffix = self.suffix)
        elif self.node == 'place2dTexture':
            nd.place2dTexture(name=self.composed_name, suffix = self.suffix)
        elif self.node == 'place3dTexture':
            nd.place3dTexture(name=self.composed_name, suffix = self.suffix)
        elif self.node == 'plusMinusAverage':
            nd.plusMinusAverage(name=self.composed_name, 
                                suffix = self.suffix,
                                operation = self.value1, 
                                lockAttr = self.lock)
        elif self.node == 'pointConstraint':
            nd.pointConstraint(name=self.composed_name, 
                               suffix = self.suffix,
                               objA = self.value1, 
                               objB = self.value2, 
                               maintainOffset = self.value3,
                               lock = self.value4)        
        elif self.node == 'pointMatrixMult':
            nd.pointMatrixMult(name=self.composed_name, suffix = self.suffix)
        elif self.node == 'pointOnCurveInfo':
            nd.pointOnCurveInfo(name=self.composed_name, suffix = self.suffix)
        elif self.node == 'pointOnPolyConstraint':
            nd.pointOnPolyConstraint(name=self.composed_name, suffix = self.suffix)
        elif self.node == 'pointOnSurfaceInfo':
            nd.pointOnSurfaceInfo(name=self.composed_name, suffix = self.suffix)
        elif self.node == 'poleVectorConstraint':
            nd.poleVectorConstraint(name=self.composed_name, 
                                    suffix = self.suffix,
                                    objA = self.value1, 
                                    objB = self.value2)
        elif self.node == 'projection':
            nd.projection(name=self.composed_name, suffix = self.suffix)
        elif self.node == 'quadSwitch':
            nd.quadSwitch(name=self.composed_name, suffix = self.suffix)
        elif self.node == 'remapColor':
            nd.remapColor(name=self.composed_name, suffix = self.suffix)
        elif self.node == 'remapHsv':
            nd.remapHsv(name=self.composed_name, suffix = self.suffix)
        elif self.node == 'remapValue':
            nd.remapValue(name=self.composed_name, 
                          suffix = self.suffix,
                          inputValue = self.value1, 
                          inputMin = self.value2, 
                          inputMax = self.value3, 
                          outputMin = self.value4, 
                          outputMax = self.value5, 
                          lockAttr = self.lock)
        elif self.node == 'reverse':
            nd.reverse(name=self.composed_name, 
                       suffix = self.suffix,
                       inputX = self.value2, 
                       inputY = self.value2, 
                       inputZ = self.value3, 
                       lockAttr = self.lock)
        elif self.node == 'rgbToHsv':
            nd.rgbToHsv(name=self.composed_name, suffix = self.suffix)        
        elif self.node == 'samplerInfo':
            nd.samplerInfo(name=self.composed_name, suffix = self.suffix) 
        elif self.node == 'scaleConstraint':
            nd.scaleConstraint(name=self.composed_name, 
                               suffix = self.suffix,
                               objA = self.value1, 
                               objB = self.value2,
                               maintainOffset = self.value3) 
        elif self.node == 'setRange':
            nd.setRange(name=self.composed_name, suffix = self.suffix)         
        elif self.node == 'singleSwitch':
            nd.singleSwitch(name=self.composed_name, suffix = self.suffix) 
        elif self.node == 'stencil':
            nd.stencil(name=self.composed_name, suffix = self.suffix)         
        elif self.node == 'surfaceInfo':
            nd.surfaceInfo(name=self.composed_name, suffix = self.suffix)         
        elif self.node == 'surfaceLuminance':
            nd.surfaceLuminance(name=self.composed_name, suffix = self.suffix)
        elif self.node == 'transform':
            nd.transform(name=self.composed_name, 
                         suffix = self.suffix,
                         position = self.value1, 
                         parent = self.value2) 
        elif self.node == 'transposeMatrix':
            nd.transposeMatrix(name=self.composed_name, suffix = self.suffix)
        elif self.node == 'tripleSwitch':
            nd.tripleSwitch(name=self.composed_name, suffix = self.suffix)
        elif self.node == 'unitConversion':
            nd.unitConversion(name=self.composed_name, suffix = self.suffix)
        elif self.node == 'vectorProduct':
            nd.vectorProduct(name=self.composed_name, suffix = self.suffix)

        #--- save the created node information in code
        self.save_code_info()

        #--- clear all fields and checkboxes
        self.clear_all()
    #END def create_node()

    def save_code_info(self):
        #--- this method saves the code information
        sel = cmds.ls(selection = True)
        node_sel = sel[0]
        if self.node in sel[0]:
            node_sel = sel[0]
        elif self.name in sel[0]:
            node_sel = sel[0]
        else:
            print sel[0]
        code = ["cmds.createNode(" + '"' + self.node + '"' + ", name=" + '"' 
                + node_sel + '"' + ")"]
        attributes = list()
        lock = ", lock=True"

        attrs = [self.attr1, self.attr2, self.attr3, self.attr4,
                 self.attr5, self.attr6, self.attr7, self.attr8,
                 self.attr9]
        value = [self.value1, self.value2, self.value3, self.value4,
                 self.value5, self.value6, self.value7, self.value8,
                 self.value9]
        locks = [self.lock1_BOX, self.lock2_BOX, self.lock3_BOX, self.lock4_BOX,
                 self.lock5_BOX, self.lock6_BOX, self.lock7_BOX, self.lock8_BOX,
                 self.lock9_BOX]

        for v, a, l in zip(value, attrs, locks):
            if v:
                if l.isChecked():
                    attr = ("cmds.setAttr(" + '"' + node_sel + "." + a + '", ' 
                            + v + lock + ")")
                    attributes.append(attr)
                else:
                    attr = ("cmds.setAttr(" + '"' + node_sel + "." + a + '", ' 
                            + v + ")")
                    attributes.append(attr)
        self.code_information=[code, attributes]
    #END def save_code_info()

    def generate_code(self):
        #--- this method gets the rotation values
        node = self.code_information
        if not node:
            print 'Cannot create node, no valid specifications were made!'
        print '                '
        print 'GENERATED CODE:'
        print '                '
        try:
            print node[0][0]
            for i in node[1]:
                print i
        except:
            print 'Cannot create node, no valid specifications were made!'            
    #END def generate_code()

    def __setup(self):
        #--- this method setups the ui
        #--- setup dropDown menu
        self.setup_dropdown_menu()
        #--- connect signals
        self.connect_signals()
    #END def __setup()
#END class NodeManagerUI()


def main():
    global et_win
    try:
        et_win.close()
    except:
        pass
    et_win = NodeManagerUI()
    et_win.show()
#END def main()
