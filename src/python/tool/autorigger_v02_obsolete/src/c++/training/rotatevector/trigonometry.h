// Copyright Emre Tekinalp. All rights reserved.

#ifndef PLUGINS_TRIGONOMETRY_TRIGONOMETRY_H_
#define PLUGINS_TRIGONOMETRY_TRIGONOMETRY_H_

#include <cmath>
#include <iostream>
using std::cout;
using std::endl;
using std::cerr;

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnPointArrayData.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNumericData.h>
#include <maya/MItGeometry.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MPoint.h>
#include <maya/MPointArray.h>
#include <maya/MVectorArray.h>
#include <maya/MDoubleArray.h>
#include <maya/MFnDoubleArrayData.h>
#include <maya/MFloatVectorArray.h>
#include <maya/MFloatArray.h>
#include <maya/MMatrix.h>
#include <maya/MFnMatrixData.h>
#include <maya/MVector.h>
#include <maya/MGlobal.h>
#include <maya/MAngle.h>
#include <maya/MQuaternion.h>

class Trigonometry : public MPxNode {
  public:
    Trigonometry();
    ~Trigonometry();

    static void* creator();
    static MStatus initialize();

    // Compute algorithm node
    virtual MStatus compute(const MPlug& plug, MDataBlock& data);

    // Define node attributes
    // Create an id number for the maya node
    static MTypeId id;
    // Create input attributes
    static MObject a_vector;
    static MObject a_degree;
    static MObject a_operator;
    // Create output attributes
    static MObject a_output;
};

#endif // PLUGINS_TRIGONOMETRY_TRIGONOMETRY_H_
