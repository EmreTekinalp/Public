#ifndef RAMP_OFFSET_H_
#define RAMP_OFFSET_H_

#include <iostream>
using std::cout;
using std::endl;
using std::cerr;

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFloatVector.h>
#include <maya/MFnNumericData.h>
#include <maya/MRampAttribute.h>

class RampOffset : public MPxNode
{
public:
  RampOffset(); // constructor
  ~RampOffset(); // deconstructor

  static void* creator(); // creator
  static MStatus initialize(); // initialize
  virtual MStatus compute(const MPlug& plug, MDataBlock& data); // compute

  // declare attributes
  static MTypeId id;
  static MObject a_ramptx;
  static MObject a_rampty;
  static MObject a_ramptz;
  static MObject a_mtx;
  static MObject a_mty;
  static MObject a_mtz;
  static MObject a_ramprx;
  static MObject a_rampry;
  static MObject a_ramprz;
  static MObject a_mrx;
  static MObject a_mry;
  static MObject a_mrz;
  static MObject a_rampsx;
  static MObject a_rampsy;
  static MObject a_rampsz;
  static MObject a_msx;
  static MObject a_msy;
  static MObject a_msz;
  static MObject a_outtranslate;
  static MObject a_outrotate;
  static MObject a_outscale;
}; // end class RampOffset

#endif // RAMP_OFFSET_H_
