// Copyright Emre Tekinalp. All rights reserved.

#include "trigonometry.h"

MTypeId Trigonometry::id(0x1837465);
MObject Trigonometry::a_vector;
MObject Trigonometry::a_degree;
MObject Trigonometry::a_operator;
MObject Trigonometry::a_output;

Trigonometry::Trigonometry() {
}

Trigonometry::~Trigonometry() {
}

void* Trigonometry::creator() {
  return new Trigonometry();
}

MStatus Trigonometry::initialize() {
  MStatus status;
  // Create function sets for attributes
  MFnEnumAttribute e_attr;
  MFnNumericAttribute n_attr;
  MFnCompoundAttribute c_attr;
  MFnMatrixAttribute m_attr;
  MFnUnitAttribute u_attr;

  // vector
  a_vector = n_attr.createPoint("vector", "vec", &status);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  n_attr.setKeyable(true);
  CHECK_MSTATUS(addAttribute(a_vector));

  // degree
  a_degree = n_attr.create("degree", "deg", MFnNumericData::kDouble, 0.0);
  n_attr.setKeyable(true);
  CHECK_MSTATUS(addAttribute(a_degree));

  // operator
  a_operator = e_attr.create("operator", "op");
  e_attr.addField("sine", 0);
  e_attr.addField("cosine", 1);
  e_attr.addField("tangent", 2);
  e_attr.addField("negative sine", 3);
  e_attr.addField("negative cosine", 4);
  e_attr.addField("negative tangent", 5);
  e_attr.setKeyable(true);
  CHECK_MSTATUS(addAttribute(a_operator));

  // output
  a_output = n_attr.createPoint("output", "out");
  n_attr.setHidden(true);
  CHECK_MSTATUS(addAttribute(a_output));

  // affect attributes
  attributeAffects(a_vector, a_output);
  attributeAffects(a_degree, a_output);
  attributeAffects(a_operator, a_output);

  return (MS::kSuccess);
}

MStatus Trigonometry::compute(const MPlug& plug, MDataBlock& data) {
  MStatus status;

  if (plug == a_output) {
    // degree
    double d_degree = data.inputValue(a_degree, &status).asDouble();
    CHECK_MSTATUS_AND_RETURN_IT(status);
    // operator
    int i_operator = data.inputValue(a_operator, &status).asShort();
    CHECK_MSTATUS_AND_RETURN_IT(status);

    MFloatVector fv_outvector;
    if (i_operator == 0) {

    }

    // output
    MDataHandle h_output = data.outputValue(a_output, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    h_output.set(fv_outvector);
    data.setClean(plug);
  }

  return MS::kSuccess;
}
