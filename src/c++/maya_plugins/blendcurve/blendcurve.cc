// Copyright Emre Tekinalp. All rights reserved.
// This is the cc source file of the ecurve deformer.

// TODO: Create input for second curve as a driver than saving initCurveData

#include "blendcurve.h"

MTypeId BlendCurve::id(0x3145456);
MObject BlendCurve::a_slide;
MObject BlendCurve::a_slider_type;
MObject BlendCurve::a_in_curve;
MObject BlendCurve::a_in_curve_matrix;
MObject BlendCurve::a_init_curve_data;


BlendCurve::BlendCurve() {
}

BlendCurve::~BlendCurve() {
}

void* BlendCurve::creator() {
  return new BlendCurve();
}

MStatus BlendCurve::initialize() {
  // Create function sets for attributes
  MFnEnumAttribute e_attr;
  MFnTypedAttribute t_attr;
  MFnNumericAttribute n_attr;
  MFnMatrixAttribute m_attr;

  // slider
  a_slide = n_attr.create("slide", "sl", MFnNumericData::kDouble, 1.0);
  n_attr.setMin(0.0);
  n_attr.setMax(1.0);
  n_attr.setKeyable(true);
  CHECK_MSTATUS(addAttribute(a_slide));

  // sliderType
  a_slider_type = e_attr.create("sliderType", "st");
  e_attr.addField("smooth", 0);
  e_attr.addField("linear", 1);
  e_attr.setKeyable(true);
  CHECK_MSTATUS(addAttribute(a_slider_type));

  // inCurve
  a_in_curve = t_attr.create("inCurve", "ic", MFnData::kNurbsCurve);
  t_attr.setReadable(true);
  t_attr.setWritable(true);
  CHECK_MSTATUS(addAttribute(a_in_curve));

  // inCurveMatrix
  a_in_curve_matrix = m_attr.create("inCurveMatrix", "icm");
  m_attr.setHidden(true);
  CHECK_MSTATUS(addAttribute(a_in_curve_matrix));

  // initCurveData
  a_init_curve_data = t_attr.create("initCurveData", "icd",
                                    MFnData::kDoubleArray);
  t_attr.setKeyable(false);
  t_attr.setReadable(false);
  t_attr.setStorable(true);
  t_attr.setHidden(true);
  CHECK_MSTATUS(addAttribute(a_init_curve_data));

  // Attribute affects
  attributeAffects(a_slide, outputGeom);
  attributeAffects(a_slider_type, outputGeom);
  attributeAffects(a_in_curve, outputGeom);
  attributeAffects(a_in_curve_matrix, outputGeom);
  attributeAffects(a_init_curve_data, outputGeom);

  return (MS::kSuccess);
}

MStatus BlendCurve::deform(MDataBlock& block, MItGeometry& iter,
                       const MMatrix& mat, unsigned int mindex) {
  MStatus status;

  // Get inputGeom
  MArrayDataHandle h_input = block.outputArrayValue(input, &status);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  status = h_input.jumpToElement(0);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  MObject o_inputgeom = h_input.outputValue().child(inputGeom).asNurbsCurve();
  if (! o_inputgeom.hasFn(MFn::kNurbsCurve)) {
    return MS::kUnknownParameter;
  }

  // Get worldmatrix
  MFnMatrixData md_curve(o_inputgeom);
  MMatrix m_curve = md_curve.matrix();

  // Get envelope
  float f_env = block.inputValue(envelope, &status).asFloat();
  CHECK_MSTATUS_AND_RETURN_IT(status);

  // Get slide
  double d_slide = block.inputValue(a_slide, &status).asDouble();
  CHECK_MSTATUS_AND_RETURN_IT(status);

  // Get sliderType
  int i_slidertype = block.inputValue(a_slider_type, &status).asShort();
  CHECK_MSTATUS_AND_RETURN_IT(status);

  // Get initCurveData
  MMatrix m_incurve = block.inputValue(a_in_curve_matrix, &status).asMatrix();
  CHECK_MSTATUS_AND_RETURN_IT(status);

  // Get inCurve
  MObject o_incurve = block.inputValue(a_in_curve).asNurbsCurve();
  if (! o_incurve.hasFn(MFn::kNurbsCurve)) {
    return MS::kUnknownParameter;
  }

  MFnNurbsCurve fn_incurve(o_incurve);
  MPointArray pa_initpoints, pa_finalpoints(iter.count());
  status = fn_incurve.getCVs(pa_initpoints);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  MDoubleArray da_param(pa_initpoints.length());

  double d_rmv, d_result = 0.0000000000;

  // Get and populate the initCurveData
  MDataHandle h_initcurvedata = block.inputValue(a_init_curve_data, &status);
  MObject o_initcurvedata = h_initcurvedata.data();
  if (!o_initcurvedata.hasFn(MFn::kDoubleArrayData)) {
    for (unsigned int d=0; d < pa_initpoints.length(); d++) {
      status = fn_incurve.getParamAtPoint(pa_initpoints[d], da_param[d],
                                            MSpace::kObject);
      CHECK_MSTATUS_AND_RETURN_IT(status);
    }
    // We need to populate the pointArray attribute
    MFnDoubleArrayData fnda_data;
    MObject o_initdata = fnda_data.create(da_param);
    status = h_initcurvedata.set(o_initdata);
    CHECK_MSTATUS_AND_RETURN_IT(status);
  }
  else {
    MFnDoubleArrayData fnda_data(o_initcurvedata);
    da_param = fnda_data.array();
  }

  for (; !iter.isDone(); iter.next()) {
    // smooth interpolation type
    /*
    if (! i_slidertype) {
      fn_incurve.getParamAtPoint(pa_initpoints[iter.index()],
                                 da_param[iter.index()]);
      // smooth interpolation type
      d_result = da_param[iter.index()] * d_slide;
    }
    else {
      // linear interpolation type
      // d_rmv = low2 + (value - low1) * (high2 - low2) / (high1 - low1)
      // 0.0 + (d_slide - 0.0) * (fn_inputgeom.numSpans() - 0.0) / (1.0 - 0.0)
      // substitute = d_slide * fn_inputgeom.numSpans() / 1.0
      d_rmv = d_slide * fn_inputgeom.numSpans() / 1.00000000;
      d_result = d_rmv - fabs(fn_inputgeom.numSpans() - da_param[iter.index()]);
      if (d_result <= 0.0e-16) {
        d_result = 0.0e-16;
      }
    }
    */
    // Retrieve the final points for the outputgeom
    status = fn_incurve.getPointAtParam(da_param[iter.index()] * d_slide * f_env,
                                        pa_finalpoints[iter.index()],
                                        MSpace::kObject);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    pa_finalpoints[iter.index()] *= m_incurve;
  }
  iter.setAllPositions(pa_finalpoints);

  return MS::kSuccess;
}
