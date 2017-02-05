#ifndef OFFSETCURVE_H
#define OFFSETCURVE_H

#include <maya/MPxNode.h>
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
#include <cmath>
#include <vector>

#include <iostream>
using namespace std;


class OffsetCurve : public MPxNode
{
private:
    //no private stuff
public:
						OffsetCurve();
    virtual             ~OffsetCurve();

    static void*        creator();
    static MStatus      initialize();

    virtual MStatus     compute(const MPlug& plug, MDataBlock& dataBlock);
    MVectorArray		parallelFrameNormals(int samples, MVector upvec, MFnNurbsCurve& fnCurve);
    void				calculateRotation(MVector up, MVector forward, double rotation[3]);

public:
    //attributes
    static MTypeId      id;
    //inputs
    static MObject      aInCurve;
    static MObject      aInMatrix;
    static MObject      aOffset;
    static MObject      aInitUpVector;
    static MObject      aInitCurveData;
    //outputs
    static MObject      aOutTranslate;
    static MObject      aOutRotate;
};

#endif
