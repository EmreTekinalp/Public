#ifndef HI_ON_LO_CURVE_H_
#define HI_ON_LO_CURVE_H_

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
#include <cmath>
#include <vector>

#include <iostream>
using namespace std;


class HiOnLoCurve: public MPxDeformerNode
{
private:
    //no private stuff
public:
    HiOnLoCurve();
    virtual ~HiOnLoCurve();

    static void* creator();
    static MStatus initialize();

    virtual MStatus deform(MDataBlock& data, MItGeometry& iter, const MMatrix& mat, unsigned int multiIndex);

    void GetClosestPoint(MFnNurbsCurve& fnCurve, MPoint inPosition, MPoint& position, double& paramU);
public:
    //attributes
    static MTypeId      id;
    //inputs
    static MObject a_inmatrix_;
    static MObject a_incurve_;
    static MObject a_initcurvedata_;

    //outputs
    static MObject a_outtranslate_;
    static MObject a_outrotatex_;
    static MObject a_outrotatey_;
    static MObject a_outrotatez_;
    static MObject a_outrotate_;
};

#endif
