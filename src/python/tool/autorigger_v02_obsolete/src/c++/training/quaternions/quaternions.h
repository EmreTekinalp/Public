#ifndef QUATERNIONS_H_
#define QUATERNIONS_H_

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNumericData.h>
#include <maya/MFnMesh.h>
#include <maya/MPoint.h>
#include <maya/MPointArray.h>
#include <maya/MVectorArray.h>
#include <maya/MFloatVectorArray.h>
#include <maya/MFloatArray.h>
#include <maya/MMatrix.h>
#include <maya/MFnMatrixData.h>
#include <maya/MVector.h>
#include <maya/MGlobal.h>
#include <maya/MAngle.h>
#include <maya/MQuaternion.h>

#include <complex.h>
#include <cmath>
#include <vector>
#include <iostream>
using namespace std;

class Quaternions : public MPxNode
{
private:
    //no private stuff
public:
						Quaternions();
    virtual             ~Quaternions();

    static void*        creator();
    static MStatus      initialize();

    virtual MStatus     compute(const MPlug& plug, MDataBlock& data);

    void				getQuaternion(MVector& n, float a, MQuaternion& quaternion);
    void				invertQuaternion(MQuaternion& quaternion);

public:
    //attributes
    static MTypeId      id;
    //inputs
    static MObject      aInMatrix;
    //outputs
    static MObject      aOutTranslate;
    static MObject      aOutRotateX;
    static MObject      aOutRotateY;
    static MObject      aOutRotateZ;
    static MObject      aOutRotate;
};

#endif
