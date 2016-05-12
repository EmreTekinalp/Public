// Copyright Emre Tekinalp. All rights reserved.
// Create a curve deformer with sliding and offseting ability.
// There are two different sliding types, a smooth and a linear one.
// Optionally you can use an existing curve as a driver for the deformed one.


#ifndef PLUGINS_ECURVE_ECURVE_H_
#define PLUGINS_ECURVE_ECURVE_H_

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

class Ecurve : public MPxDeformerNode {
  public:
    Ecurve();
    ~Ecurve();

    static void* creator();
    static MStatus initialize();

    // Compute algorithm and deform given object
    virtual MStatus deform(MDataBlock& block,
                           MItGeometry& iter,
                           const MMatrix& mat,
                           unsigned int mindex);
    // Use paralleFrameTransportation algorithm to compute
    // normal vector of curve and return MVectorArray of new normals
    MVectorArray ParallelFrameNormals(int samples,
                                      MVector upvec,
                                      MFnNurbsCurve& fncurve,
                                      float slider);
    // Calculate the euler rotation values from given up and forward vectors
    // and populate rotation double[3] with new values
    void CalculateRotation(MVector up,
                           MVector forward,
                           double rotation[3]);

    // Define node attributes
    // Create an id number for the maya node
    static MTypeId id;
    // Create input attributes
    static MObject a_slide;
    static MObject a_slider_type;
    static MObject a_offset;
    static MObject a_push;
    static MObject a_in_curve;
    static MObject a_init_up_vector;
    static MObject a_init_curve_data;
    // Create output attributes
    static MObject a_out_translate;
    static MObject a_out_rotate;
};

#endif // PLUGINS_ECURVE_ECURVE_H_
