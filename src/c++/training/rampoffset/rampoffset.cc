#include "rampoffset.h"

MTypeId RampOffset::id(0x342312);
MObject RampOffset::a_ramptx;
MObject RampOffset::a_rampty;
MObject RampOffset::a_ramptz;
MObject RampOffset::a_mtx;
MObject RampOffset::a_mty;
MObject RampOffset::a_mtz;
MObject RampOffset::a_ramprx;
MObject RampOffset::a_rampry;
MObject RampOffset::a_ramprz;
MObject RampOffset::a_mrx;
MObject RampOffset::a_mry;
MObject RampOffset::a_mrz;
MObject RampOffset::a_rampsx;
MObject RampOffset::a_rampsy;
MObject RampOffset::a_rampsz;
MObject RampOffset::a_msx;
MObject RampOffset::a_msy;
MObject RampOffset::a_msz;
MObject RampOffset::a_outtranslate;
MObject RampOffset::a_outrotate;
MObject RampOffset::a_outscale;


RampOffset::RampOffset()
{
} // end constructor


RampOffset::~RampOffset()
{
} // end deconstructor


void* RampOffset::creator()
{
  return new RampOffset();
} // end creator

MStatus RampOffset::initialize()
{
  MFnNumericAttribute n_attr;
  MRampAttribute r_attr;

  // rampTranslateX
  a_ramptx = r_attr.createCurveRamp("rampTranslateX", "rtx");
  CHECK_MSTATUS(addAttribute(a_ramptx));

  // multiplyTranslateX
  a_mtx = n_attr.create("multiplyTranslateX", "mtx", MFnNumericData::kFloat, 1.0);
  CHECK_MSTATUS(addAttribute(a_mtx));

  // rampty
  a_rampty = r_attr.createCurveRamp("rampTranslateY", "rty");
  CHECK_MSTATUS(addAttribute(a_rampty));

  // multiplyTranslateY
  a_mty = n_attr.create("multiplyTranslateY", "mty", MFnNumericData::kFloat, 1.0);
  CHECK_MSTATUS(addAttribute(a_mty));

  // ramptz
  a_ramptz = r_attr.createCurveRamp("rampTranslateZ", "rtz");
  CHECK_MSTATUS(addAttribute(a_ramptz));

  // multiplyTranslateZ
  a_mtz = n_attr.create("multiplyTranslateZ", "mtz", MFnNumericData::kFloat, 1.0);
  CHECK_MSTATUS(addAttribute(a_mtz));

  // outTranslate
  a_outtranslate = n_attr.createPoint("outTranslate", "ot");
  n_attr.setArray(true);
  n_attr.setHidden(true);
  CHECK_MSTATUS(addAttribute(a_outtranslate));

  // outRotate
  a_outrotate = n_attr.createPoint("outRotate", "or");
  n_attr.setArray(true);
  n_attr.setHidden(true);
  CHECK_MSTATUS(addAttribute(a_outrotate));

  // outScale
  a_outscale = n_attr.createPoint("outScale", "os");
  n_attr.setArray(true);
  n_attr.setHidden(true);
  CHECK_MSTATUS(addAttribute(a_outscale));

  attributeAffects(a_ramptx, a_outtranslate);
  attributeAffects(a_rampty, a_outtranslate);
  attributeAffects(a_ramptz, a_outtranslate);
  attributeAffects(a_mtx, a_outtranslate);
  attributeAffects(a_mty, a_outtranslate);
  attributeAffects(a_mtz, a_outtranslate);

  return MS::kSuccess;
} // end initialize


MStatus RampOffset::compute(const MPlug& plug, MDataBlock& data)
{
  MStatus status;
  // get ramp plugs
  MObject o_this = thisMObject();
  MPlug plug_tx(o_this, a_ramptx);
  MPlug plug_ty(o_this, a_rampty);
  MPlug plug_tz(o_this, a_ramptz);

  MRampAttribute rmp_tx(plug_tx);
  MRampAttribute rmp_ty(plug_ty);
  MRampAttribute rmp_tz(plug_tz);

  float f_tx = data.inputValue(a_mtx, &status).asFloat();
  CHECK_MSTATUS_AND_RETURN_IT(status);
  float f_ty = data.inputValue(a_mty, &status).asFloat();
  CHECK_MSTATUS_AND_RETURN_IT(status);
  float f_tz = data.inputValue(a_mtz, &status).asFloat();
  CHECK_MSTATUS_AND_RETURN_IT(status);

  MArrayDataHandle h_outtranslate = data.outputArrayValue(a_outtranslate, &status);
  float f_position = 0.0;
  float f_vtx, f_vty, f_vtz;
  for (unsigned int i=0; i<h_outtranslate.elementCount(); i++)
  {
    f_position += 1.0 / h_outtranslate.elementCount();
    rmp_tx.getValueAtPosition(f_position, f_vtx, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    rmp_ty.getValueAtPosition(f_position, f_vty, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    rmp_tz.getValueAtPosition(f_position, f_vtz, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    MFloatVector fv_translate(f_vtx * f_tx, f_vty * f_ty, f_vtz * f_tz);

    CHECK_MSTATUS(h_outtranslate.jumpToArrayElement(i));
    h_outtranslate.outputValue().set(fv_translate);
  } // end for

  return MS::kSuccess;
} // end compute
