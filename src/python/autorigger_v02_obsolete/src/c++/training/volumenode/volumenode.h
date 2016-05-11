// This is the offset class header file

#ifndef RAINMAKERPLUGINS_VOLUMENODE_VOLUMENODE_H_
#define RAINMAKERPLUGINS_VOLUMENODE_VOLUMENODE_H_

#include <iostream>
using std::cout;
using std::cerr;
using std::endl;

#include <maya/MPxDeformerNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MMatrix.h>
#include <maya/MFnMatrixData.h>
#include <maya/MPointArray.h>
#include <maya/MFnPointArrayData.h>
#include <maya/MFnMesh.h>
#include <maya/MGlobal.h>
#include <maya/MItGeometry.h>
#include <maya/MItMeshVertex.h>
#include <maya/MIntArray.h>

static const MString nodename = "volume";

class VolumeNode: MPxDeformerNode
{
public:
  VolumeNode(); // constructor function
  ~VolumeNode(); // deconstructor function

  static void* creator(); // creator function
  static MStatus initialize(); // attribute initializer function
  virtual MStatus deform(MDataBlock& data, MItGeometry& iter,
                         const MMatrix& mat, unsigned int multiIndex);
  // attribute declaration
  static MTypeId id;
  static MObject a_volumeinvmatrix;
  static MObject a_falloff;
  static MObject a_multiplier;
  static MObject a_meshdata;
}; // end class OffsetNode

#endif //RAINMAKERPLUGINS_VOLUMENODE_VOLUMENODE_H_
