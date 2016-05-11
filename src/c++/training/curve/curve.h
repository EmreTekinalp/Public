#ifndef CURVE_H
#define CURVE_H

#include <maya/MPxDeformerNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MFnNumericData.h>
#include <maya/MFnMesh.h>
#include <maya/MItMeshVertex.h>
#include <maya/MPoint.h>
#include <maya/MItGeometry.h>
#include <maya/MPointArray.h>
#include <maya/MVectorArray.h>
#include <maya/MFloatVectorArray.h>
#include <maya/MFnTransform.h>
#include <maya/MMatrix.h>
#include <maya/MFnMatrixData.h>
#include <maya/MVector.h>
#include <maya/MGlobal.h>
#include <maya/MAngle.h>
#include <maya/MSelectionList.h>
#include <maya/MDagPath.h>
#include <maya/MFnDagNode.h>
#include <maya/MFnPointArrayData.h>
#include <maya/MFnVectorArrayData.h>
#include <maya/MFnDoubleArrayData.h>
#include <maya/MGLFunctionTable.h>
#include <maya/M3dView.h>
#include <math.h>
#include <vector>

#include <iostream>
using namespace std;

class Curve: public MPxDeformerNode
{
private:
    //no private stuff
public:
                        Curve();
    virtual             ~Curve();

    static void*        creator();
    static MStatus      initialize();

    virtual MStatus     deform(MDataBlock& data, MItGeometry& iter, const MMatrix& mat, unsigned int multiIndex);

    MVectorArray		parallelFrameNormals(int samples, MVector upvec, MFnNurbsCurve& fnCurve, float slider);
    void				calculateTwist(MVector& tangent, double twist);
    void 				calculateRotation(MVector up, MVector forward, double rotation[3]);
    void				getClosestPoint(MFnNurbsCurve& fnCurve, MPoint inPosition, MPoint& position, double& paramU);
public:
    //attributes
    static MTypeId      id;
    //inputs
    static MObject      aInMatrix;
    static MObject      aInCurve;
    static MObject      aInCurveMatrix;
    static MObject      aInitCurveData;
    static MObject      aInitUpVector;
    static MObject      aInitDeltaData;
    static MObject      aInitParamData;
    static MObject      aSlider;
    static MObject      aSliderType;
    static MObject      aOffset;
    //outputs
    static MObject      aOutTranslate;
    static MObject      aOutRotateX;
    static MObject      aOutRotateY;
    static MObject      aOutRotateZ;
    static MObject      aOutRotate;
};

#endif
