#pragma once

#include <maya/MPxDeformerNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MTransformationMatrix.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MVector.h>
#include <maya/MGlobal.h>
#include <maya/MQuaternion.h>
#include <maya/MMatrix.h>
#include <iostream>
using std::cerr;
using std::cout;
using std::endl;

class PftCurve : public MPxDeformerNode
{
public:
    PftCurve();
    virtual ~PftCurve();

    virtual MStatus deform(MDataBlock& data, MItGeometry& iterator,
                           const MMatrix& matrix, unsigned int multiIndex);
    static void* creator();
    static MStatus initialize();

    MVector pftAlgorithm(MVector up, MVector tangent);

    static MTypeId id;

    // input parameters
    static MObject upMatrix;
    static MObject outTranslate;
    static MObject outRotateX;
    static MObject outRotateY;
    static MObject outRotateZ;
    static MObject outRotate;
};