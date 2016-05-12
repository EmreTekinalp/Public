#ifndef ET_WIREDEFORMER_H
#define ET_WIREDEFORMER_H

#include <maya/MPxDeformerNode.h>
#include <maya/MItGeometry.h>
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
#include <maya/MFnDoubleArrayData.h>
#include <cmath>
#include <vector>

#include <iostream>
using namespace std;


class EtWireDeformer: public MPxDeformerNode
{
private:
    //no private stuff
public:
						EtWireDeformer();
    virtual             ~EtWireDeformer();

    static void*        creator();
    static MStatus      initialize();

    virtual MStatus     deform(MDataBlock& block, MItGeometry& iter, const MMatrix& mat, unsigned int mutiIndex);

    void				closestTangentUAndDistance(MFnNurbsCurve& curveFn, MPoint inPosition, MPoint& position,
    											   MVector normal, MVector tangent, double &paramU, double &distance);

public:
    //attributes
    static MTypeId      id;
    //inputs
    static MObject      aInCurve;
    static MObject      aInCurveMatrix;
    static MObject      aInitCurveData;
    static MObject      aInitUpVector;
    static MObject      aInitUpVectorX;
    static MObject      aInitUpVectorY;
    static MObject      aInitUpVectorZ;
    static MObject      aTwist;
    static MObject      aOffset;
};

#endif
