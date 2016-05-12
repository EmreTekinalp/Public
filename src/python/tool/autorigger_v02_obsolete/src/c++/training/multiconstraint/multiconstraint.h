// Copyright Emre Tekinalp. All rights reserved.

#ifndef PLUGINS_MULTICONSTRAINT_MULTICONSTRAINT_H_
#define PLUGINS_MULTICONSTRAINT_MULTICONSTRAINT_H_

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

class MultiConstraint : public MPxNode {
  public:
    MultiConstraint();
    ~MultiConstraint();

    static void* creator();
    static MStatus initialize();

    // Compute algorithm and deform given object
    virtual MStatus compute(const MPlug& plug, MDataBlock& data);

    // Define node attributes
    // Create an id number for the maya node
    static MTypeId id;
    // Create input attributes
    static MObject a_input;
    static MObject a_inmatrix;
    static MObject a_operator;
    static MObject a_operatormo;
    static MObject a_scale;
    static MObject a_scalemo;
    // Create output attributes
    static MObject a_output;
    static MObject a_outtranslate;
    static MObject a_outrotate;
    static MObject a_outrotatex;
    static MObject a_outrotatey;
    static MObject a_outrotatez;
    static MObject a_outscale;
    static MObject a_outscalex;
    static MObject a_outscaley;
    static MObject a_outscalez;
};

#endif // PLUGINS_MULTICONSTRAINT_MULTICONSTRAINT_H_
