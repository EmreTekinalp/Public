// Copyright Emre Tekinalp. All rights reserved.
// Create a curve deformer with sliding and offseting ability.
// There are two different sliding types, a smooth and a linear one.
// Optionally you can use an existing curve as a driver for the deformed one.


#ifndef PLUGINS_CURVECREATOR_CURVECREATOR_H_
#define PLUGINS_CURVECREATOR_CURVECREATOR_H_

#include <cmath>
#include <iostream>
using std::cout;
using std::endl;
using std::cerr;

#include <maya/MPxDeformerNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnPointArrayData.h>
#include <maya/MFnTypedAttribute.h>
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

class CurveCreator : public MPxDeformerNode {
  public:
    CurveCreator();
    ~CurveCreator();

    static void* creator();
    static MStatus initialize();

    // Compute algorithm and deform given object
    virtual MStatus deform(MDataBlock& data,
                           MItGeometry& iter,
                           const MMatrix& mat,
                           unsigned int mindex);
    // Define node attributes
    // Create an id number for the maya node
    static MTypeId id;
    // Create input attributes
    static MObject a_cvs;
    static MObject a_degree;
    static MObject a_in_curve;
};

#endif // PLUGINS_CURVECREATOR_CURVECREATOR_H_
