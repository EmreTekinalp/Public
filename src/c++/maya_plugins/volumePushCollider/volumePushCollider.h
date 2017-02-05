#ifndef VOLUMEPUSHCOLLIDER_H
#define VOLUMEPUSHCOLLIDER_H

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


class VolumePushCollider : public MPxNode
{
private:
    //no private stuff
public:
                        VolumePushCollider();
    virtual             ~VolumePushCollider();

    static void*        creator();
    static MStatus      initialize();

    virtual MStatus     compute(const MPlug& plug, MDataBlock& dataBlock);

public:
    //attributes
    static MTypeId      id;
    //inputs
    static MObject      aInCollider;
    static MObject      aInVolume;
    //outputs
    static MObject      aOutput;
};

#endif
