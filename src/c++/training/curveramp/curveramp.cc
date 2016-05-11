// Copyright Emre Tekinalp. All rights reserved.

#include "curveramp.h"

MTypeId CurveRamp::id(0x1837422);
MObject CurveRamp::a_inputcurve;
MObject CurveRamp::a_inputmatrix;
MObject CurveRamp::a_initdata;
MObject CurveRamp::a_ramp;
MObject CurveRamp::a_outposition;

CurveRamp::CurveRamp()
{
  // empty constructor
} // end constructor

CurveRamp::~CurveRamp()
{
  // empty deconstructor
} // end deconstructor

void* CurveRamp::creator()
{
  return new CurveRamp();
} // end creator

MStatus CurveRamp::initialize()
{
  // declare variables
  MFnTypedAttribute t_attr;
  MFnMatrixAttribute m_attr;
  MRampAttribute r_attr;
  MFnNumericAttribute n_attr;

  // inputcurve
  a_inputcurve = t_attr.create("inputCurve", "ic", MFnData::kNurbsCurve);
  t_attr.setHidden(true);
  CHECK_MSTATUS(addAttribute(a_inputcurve));

  // inputmatrix
  a_inputmatrix = m_attr.create("inputMatrix", "im");
  m_attr.setHidden(true);
  CHECK_MSTATUS(addAttribute(a_inputmatrix));

  // initdata
  a_initdata = t_attr.create("initCurveData", "icd", MFnData::kDoubleArray);
  t_attr.setHidden(true);
  CHECK_MSTATUS(addAttribute(a_initdata));

  // ramp
  a_ramp = r_attr.createCurveRamp("ramp", "rmp");
  CHECK_MSTATUS(addAttribute(a_ramp));

  // outposition
  a_outposition = n_attr.createPoint("outPosition", "op");
  n_attr.setArray(true);
  n_attr.setHidden(true);
  CHECK_MSTATUS(addAttribute(a_outposition));

  // affect attributes
  attributeAffects(a_inputcurve, a_outposition);
  attributeAffects(a_inputmatrix, a_outposition);
  attributeAffects(a_initdata, a_outposition);
  attributeAffects(a_ramp, a_outposition);

  return (MS::kSuccess);
} // end initialize

MStatus CurveRamp::compute(const MPlug& plug, MDataBlock& data)
{
  MStatus status;

  if (plug == a_outposition)
  {
    // inputcurve
    MObject o_inputcurve = data.inputValue(a_inputcurve, &status).asNurbsCurve();
    CHECK_MSTATUS_AND_RETURN_IT(status);
    if (! o_inputcurve.hasFn(MFn::kNurbsCurve))
    {
      return MS::kUnknownParameter;
    } // end if

    // inputmatrix
    MMatrix m_inputcurve = data.inputValue(a_inputmatrix, &status).asMatrix();
    CHECK_MSTATUS_AND_RETURN_IT(status);

    // outposition
    MArrayDataHandle h_outposition = data.outputArrayValue(a_outposition, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);

    // Get the ramp attributes
    MObject o_this = thisMObject();
    MRampAttribute ra_curve(o_this, a_ramp, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);

    MFnNurbsCurve fn_inputcurve(o_inputcurve);
    MPointArray pa_cvs;
    fn_inputcurve.getCVs(pa_cvs, MSpace::kWorld);
    MDoubleArray da_param(pa_cvs.length());
    float f_value;

    // Check initial curve data attribute for value
    MDataHandle h_initdata = data.inputValue(a_initdata, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    MObject o_initdata = h_initdata.data();
    if (!o_initdata.hasFn(MFn::kDoubleArrayData))
    {
      for (unsigned int d=0; d<pa_cvs.length(); d++)
      {
        fn_inputcurve.getParamAtPoint(pa_cvs[d], da_param[d], MSpace::kTransform);
      } // end for
      // We need to populate the pointArray attribute
      MFnDoubleArrayData fn_initdata;
      MObject o_initdoubledata = fn_initdata.create(da_param);
      h_initdata.set(o_initdoubledata);
    } // end if
    else
    {
      MFnDoubleArrayData fn_initdata(o_initdata);
      da_param = fn_initdata.array();
    } // end else

    for (unsigned int i=0; i<pa_cvs.length(); i++)
    {
      ra_curve.getValueAtPosition((da_param[i] / fn_inputcurve.numSpans()) * i, f_value, &status);
      CHECK_MSTATUS_AND_RETURN_IT(status);
      cout << i << ". " << "f_value: " << f_value << endl;
      fn_inputcurve.getPointAtParam(da_param[i], pa_cvs[i], MSpace::kObject);

      // output results
      h_outposition.jumpToElement(i);
      pa_cvs[i] *= m_inputcurve;
      pa_cvs[i].y += f_value;
      h_outposition.outputValue().set(static_cast<MFloatVector>(pa_cvs[i]));
      data.setClean(plug);
    } // end for
  } // end if
  return MS::kSuccess;
} // end compute
