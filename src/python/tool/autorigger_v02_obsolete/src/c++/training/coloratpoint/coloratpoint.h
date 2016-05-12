// Copyright Emre Tekinalp. All rights reserved.


#ifndef PLUGINS_COLORATPOINT_COLORATPOINT_H_
#define PLUGINS_COLORATPOINT_COLORATPOINT_H_

#include <cmath>
#include <iostream>
using std::cout;
using std::endl;
using std::cerr;

#include <maya/MPxDeformerNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MItMeshPolygon.h>
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
#include <maya/MFnMesh.h>
#include <maya/MFnMatrixData.h>
#include <maya/MColorArray.h>
#include <maya/MVector.h>
#include <maya/MGlobal.h>
#include <maya/MAngle.h>
#include <maya/MQuaternion.h>

class ColorAtPoint : public MPxDeformerNode {
  public:
  ColorAtPoint();
  ~ColorAtPoint();

  static void* creator();
  static MStatus initialize();

  // Compute algorithm and deform given object
  virtual MStatus deform(MDataBlock& data, MItGeometry& iter,
                         const MMatrix& mat, unsigned int mindex);

  // Create an id number for the maya node
  static MTypeId id;
  // Create input attributes
  static MObject a_blendmesh;
};

#endif // PLUGINS_COLORATPOINT_COLORATPOINT_H_
