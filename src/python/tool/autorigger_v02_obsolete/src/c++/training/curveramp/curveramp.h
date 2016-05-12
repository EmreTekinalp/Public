// Copyright Emre Tekinalp. All rights reserved.

#ifndef PLUGINS_CURVERAMP_CURVERAMP_H_
#define PLUGINS_CURVERAMP_CURVERAMP_H_

#include <cmath>
#include <iostream>
using std::cout;
using std::endl;
using std::cerr;

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnPointArrayData.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnNumericData.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MPoint.h>
#include <maya/MPointArray.h>
#include <maya/MVectorArray.h>
#include <maya/MDoubleArray.h>
#include <maya/MFnDoubleArrayData.h>
#include <maya/MFloatVectorArray.h>
#include <maya/MFloatArray.h>
#include <maya/MMatrix.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MVector.h>
#include <maya/MGlobal.h>
#include <maya/MAngle.h>
#include <maya/MRampAttribute.h>

class CurveRamp : public MPxNode {
  public:
    CurveRamp(); // constructor
    ~CurveRamp(); // deconstructor

    static void* creator(); // creator
    static MStatus initialize(); // initialize
    virtual MStatus compute(const MPlug& plug, MDataBlock& data); // compute

    static MTypeId id; // id attribute
    static MObject a_inputcurve; // inputCurve attribute
    static MObject a_inputmatrix; // inputMatrix attribute
    static MObject a_initdata; // initData attribute
    static MObject a_ramp; // ramp attribute
    static MObject a_outposition; // outPosition attribute
}; // end class CurveRamp

#endif // PLUGINS_CURVERAMP_CURVERAMP_H_
