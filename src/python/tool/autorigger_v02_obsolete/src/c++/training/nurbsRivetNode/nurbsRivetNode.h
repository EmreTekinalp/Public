#ifndef NURBSRIVETNODE_H
#define NURBSRIVETNODE_H

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnNumericData.h>
#include <maya/MFnMesh.h>
#include <maya/MFnNurbsSurface.h>
#include <maya/MPoint.h>
#include <maya/MPointArray.h>
#include <maya/MVectorArray.h>
#include <maya/MFloatVectorArray.h>
#include <maya/MFloatVector.h>
#include <maya/MFloatArray.h>
#include <maya/MMatrix.h>
#include <maya/MFnMatrixData.h>
#include <maya/MVector.h>
#include <maya/MGlobal.h>
#include <maya/MAngle.h>
#include <cmath>
#include <vector>

#include <iostream>
using namespace std;


class NurbsRivetNode : public MPxNode
{
private:
    //no private stuff
public:
						NurbsRivetNode();
    virtual             ~NurbsRivetNode();

    static void*        creator();
    static MStatus      initialize();

    virtual MStatus     compute(const MPlug& plug, MDataBlock& data);

    double				calculateModulus(double paramU, MFnNurbsSurface& surface, int operatorIndex);
    void				calculateRotation(MVector up, MVector forward, double rotation[3]);
public:
    //attributes
    static MTypeId      id;
    //inputs
    static MObject      aInSurface;
    static MObject      aInMatrix;
    static MObject      aOperator;
    static MObject      aParameterU;
    static MObject      aParameterV;
    static MObject      aInput;
    //outputs
    static MObject      aOutTranslate;
    static MObject      aOutRotateX;
    static MObject      aOutRotateY;
    static MObject      aOutRotateZ;
    static MObject      aOutRotate;
};

#endif
