// Copyright Emre Tekinalp. All rights reserved.
// This is the cc source file of the ecurve deformer.

// TODO: Create input for second curve as a driver than saving initCurveData

#include "ecurve.h"

MTypeId Ecurve::id(0x3974620);
MObject Ecurve::a_slide;
MObject Ecurve::a_slider_type;
MObject Ecurve::a_offset;
MObject Ecurve::a_push;
MObject Ecurve::a_in_curve;
MObject Ecurve::a_init_up_vector;
MObject Ecurve::a_init_curve_data;
MObject Ecurve::a_out_translate;
MObject Ecurve::a_out_rotate;

Ecurve::Ecurve() {
}

Ecurve::~Ecurve() {
}

void* Ecurve::creator() {
  return new Ecurve();
}

MStatus Ecurve::initialize() {
  // Create function sets for attributes
  MFnEnumAttribute e_attr;
  MFnTypedAttribute t_attr;
  MFnNumericAttribute n_attr;

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

  // offset
  a_offset = n_attr.create("offset", "off", MFnNumericData::kDouble, 0.0);
  n_attr.setReadable(true);
  n_attr.setKeyable(true);
  CHECK_MSTATUS(addAttribute(a_offset));

  // push
  a_push = n_attr.createPoint("push", "pu");
  n_attr.setKeyable(true);
  n_attr.setReadable(true);
  n_attr.setWritable(true);
  n_attr.setHidden(false);
  CHECK_MSTATUS(addAttribute(a_push));

  // inCurve
  a_in_curve = t_attr.create("inCurve", "ic", MFnData::kNurbsCurve);
  t_attr.setReadable(true);
  t_attr.setWritable(true);
  CHECK_MSTATUS(addAttribute(a_in_curve));

  // initUpVector
  a_init_up_vector = n_attr.createPoint("initUpVector", "iup");
  CHECK_MSTATUS(addAttribute(a_init_up_vector));

  // initCurveData
  a_init_curve_data = t_attr.create("initCurveData", "icd",
                                    MFnData::kDoubleArray);
  t_attr.setKeyable(false);
  t_attr.setReadable(false);
  t_attr.setStorable(true);
  t_attr.setHidden(true);
  CHECK_MSTATUS(addAttribute(a_init_curve_data));

  // outTranslate
  a_out_translate = n_attr.createPoint("outTranslate", "ot");
  n_attr.setArray(true);
  n_attr.setHidden(true);
  CHECK_MSTATUS(addAttribute(a_out_translate));

  // outRotate
  a_out_rotate = n_attr.createPoint("outRotate", "or");
  n_attr.setArray(true);
  n_attr.setHidden(true);
  CHECK_MSTATUS(addAttribute(a_out_rotate));

  // Attribute affects
  attributeAffects(a_slide, outputGeom);
  attributeAffects(a_slider_type, outputGeom);
  attributeAffects(a_push, outputGeom);
  attributeAffects(a_in_curve, outputGeom);
  attributeAffects(a_init_curve_data, outputGeom);

  attributeAffects(a_slide, a_out_translate);
  attributeAffects(a_slider_type, a_out_translate);
  attributeAffects(a_offset, a_out_translate);
  attributeAffects(a_in_curve, a_out_translate);
  attributeAffects(a_init_up_vector, a_out_translate);
  attributeAffects(a_init_curve_data, a_out_translate);

  attributeAffects(a_slide, a_out_rotate);
  attributeAffects(a_slider_type, a_out_rotate);
  attributeAffects(a_offset, a_out_rotate);
  attributeAffects(a_in_curve, a_out_rotate);
  attributeAffects(a_init_up_vector, a_out_rotate);
  attributeAffects(a_init_curve_data, a_out_rotate);

  return (MS::kSuccess);
}

MStatus Ecurve::deform(MDataBlock& block, MItGeometry& iter,
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

  // Get push
  MFloatVector fv_push = block.inputValue(a_push, &status).asFloatVector();
  CHECK_MSTATUS_AND_RETURN_IT(status);

  // Get inCurve
  MObject o_incurve = block.inputValue(a_in_curve).asNurbsCurve();

  // Get initCurveData
  MFloatVector fv_initcurvedata = block.inputValue(a_init_curve_data,
                                                   &status).asFloatVector();
  CHECK_MSTATUS_AND_RETURN_IT(status);

  MFnNurbsCurve fn_inputgeom(o_inputgeom);
  MPointArray pa_initpoints, pa_finalpoints(iter.count());
  status = fn_inputgeom.getCVs(pa_initpoints);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  MDoubleArray da_param(pa_initpoints.length());

  // Get and populate the initCurveData
  MDataHandle h_initcurvedata = block.inputValue(a_init_curve_data, &status);
  MObject o_initcurvedata = h_initcurvedata.data();
  if (!o_initcurvedata.hasFn(MFn::kDoubleArrayData)) {
    for (unsigned int d=0; d < pa_initpoints.length(); d++) {
      status = fn_inputgeom.getParamAtPoint(pa_initpoints[d], da_param[d],
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

  MPointArray pa_incurvepoints;
  if (o_incurve.hasFn(MFn::kNurbsCurve)) {
    MFnNurbsCurve fn_incurve(o_incurve);
    status = fn_incurve.getCVs(pa_incurvepoints);
    CHECK_MSTATUS_AND_RETURN_IT(status);
  }

  double d_rmv, d_result = 0.0000000000;

  for (; !iter.isDone(); iter.next()) {
    if (! i_slidertype) {
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
    // Retrieve the final points for the outputgeom
    status = fn_inputgeom.getPointAtParam(d_result * f_env,
                                          pa_finalpoints[iter.index()],
                                          MSpace::kObject);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    pa_finalpoints[iter.index()] *= m_curve;
  }
  iter.setAllPositions(pa_finalpoints);

  return MS::kSuccess;
}

MVectorArray Ecurve::ParallelFrameNormals(int samples,
                                          MVector upvec,
                                          MFnNurbsCurve& fncurve,
                                          float slider) {
  // Return an array of normals perpendicular to the tangentVector of the curve
  MStatus status;

  MVectorArray va_normals(samples);
  MVector v_tangent, v_cross1, v_cross2;
  MVector vnormal = upvec;
  double d_param;
  vnormal.normalize();

  for (unsigned int n=0; n<samples; n++) {
    d_param = fmod((fncurve.findParamFromLength(fncurve.length()) / samples)
                   * n, fncurve.numSpans()) * slider;
    if (fncurve.form() == 3) {
      d_param = fmod((fncurve.findParamFromLength(fncurve.length()) / samples)
                     * n, fncurve.numSpans());
    }
    v_tangent = fncurve.tangent(d_param, MSpace::kObject);
    v_tangent.normalize();
    v_cross1 = vnormal ^ v_tangent;
    v_cross1.normalize();
    v_cross2 = v_tangent ^ v_cross1;
    v_cross2.normalize();
    vnormal = v_cross2;
    va_normals[n] = v_cross2;
  }
  return va_normals;
}
