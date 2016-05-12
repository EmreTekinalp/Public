// Copyright Emre Tekinalp. All rights reserved.
// This is the cc source file of the curvecreator deformer.

#include "curvecreator.h"

MTypeId CurveCreator::id(0x1233567);
MObject CurveCreator::a_in_curve;
MObject CurveCreator::a_cvs;
MObject CurveCreator::a_degree;

CurveCreator::CurveCreator() {
}

CurveCreator::~CurveCreator() {
}

void* CurveCreator::creator() {
  return new CurveCreator();
}

MStatus CurveCreator::initialize() {
  // Create function sets for attributes
  MFnEnumAttribute e_attr;
  MFnTypedAttribute t_attr;
  MFnNumericAttribute n_attr;

  // inCurve
  a_in_curve = t_attr.create("inCurve", "ic", MFnData::kNurbsCurve);
  t_attr.setReadable(true);
  t_attr.setWritable(true);
  CHECK_MSTATUS(addAttribute(a_in_curve));

  // cvs
  a_cvs = n_attr.create("cvs", "cvs", MFnNumericData::kFloat, 3);
  n_attr.setReadable(true);
  n_attr.setWritable(true);
  n_attr.setKeyable(true);
  CHECK_MSTATUS(addAttribute(a_cvs));

  // degree
  a_degree = n_attr.create("degree", "deg", MFnNumericData::kShort, 3);
  n_attr.setReadable(true);
  n_attr.setWritable(true);
  n_attr.setKeyable(true);
  n_attr.setMin(1);
  n_attr.setMax(7);
  CHECK_MSTATUS(addAttribute(a_degree));

  attributeAffects(inputGeom, outputGeom);
  attributeAffects(a_in_curve, outputGeom);
  attributeAffects(a_cvs, outputGeom);
  attributeAffects(a_degree, outputGeom);

  return (MS::kSuccess);
}

MStatus CurveCreator::deform(MDataBlock& block, MItGeometry& iter,
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

  MFnNurbsCurve fn_inputgeom(o_inputgeom);
  MPointArray pa_initpoints, pa_finalpoints(iter.count());
  status = fn_inputgeom.getCVs(pa_initpoints);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  MDoubleArray da_param(pa_initpoints.length());

  for (; !iter.isDone(); iter.next()) {
  }
  iter.setAllPositions(pa_finalpoints);

  return MS::kSuccess;
}
