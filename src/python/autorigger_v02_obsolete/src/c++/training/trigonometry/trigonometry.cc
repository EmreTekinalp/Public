// Copyright Emre Tekinalp. All rights reserved.

#include "trigonometry.h"

MTypeId Trigonometry::id(0x1837465);
MObject Trigonometry::a_ramp;
MObject Trigonometry::a_color;
MObject Trigonometry::a_input;
MObject Trigonometry::a_degree;
MObject Trigonometry::a_operator;
MObject Trigonometry::a_negative;
MObject Trigonometry::a_output;
MObject Trigonometry::a_outvalue;

Trigonometry::Trigonometry() {
}

Trigonometry::~Trigonometry() {
}

void* Trigonometry::creator() {
  return new Trigonometry();
}

MStatus Trigonometry::initialize() {
  // Create function sets for attributes
  MFnEnumAttribute e_attr;
  MFnNumericAttribute n_attr;
  MFnCompoundAttribute c_attr;
  MRampAttribute r_attr;

  // ramp
  a_ramp = r_attr.createCurveRamp("ramp", "rmp");
  CHECK_MSTATUS(addAttribute(a_ramp));

  // color
  a_color = r_attr.createCurveRamp("colorRamp", "cor");
  CHECK_MSTATUS(addAttribute(a_color));

  // degree
  a_degree = n_attr.create("degree", "deg", MFnNumericData::kFloat, 0.0);
  n_attr.setHidden(true);

  // operator
  a_operator = e_attr.create("operator", "op", 0);
  e_attr.addField("sine", 0);
  e_attr.addField("cosine", 1);
  e_attr.addField("tangent", 2);
  e_attr.setKeyable(true);

  // negative
  a_negative = n_attr.create("negative", "neg", MFnNumericData::kBoolean, 0);
  n_attr.setKeyable(true);

  // input
  a_input = c_attr.create("input", "in");
  c_attr.setArray(true);
  c_attr.addChild(a_degree);
  c_attr.addChild(a_operator);
  c_attr.addChild(a_negative);
  CHECK_MSTATUS(addAttribute(a_input));

  // outvalue
  a_outvalue = n_attr.create("outValue", "ov", MFnNumericData::kFloat, 0.0);

  // output
  a_output = c_attr.create("output", "out");
  c_attr.setArray(true);
  c_attr.addChild(a_outvalue);
  CHECK_MSTATUS(addAttribute(a_output));

  // affect attributes
  attributeAffects(a_negative, a_outvalue);
  attributeAffects(a_degree, a_outvalue);
  attributeAffects(a_operator, a_outvalue);
  attributeAffects(a_input, a_outvalue);
  attributeAffects(a_negative, a_output);
  attributeAffects(a_degree, a_output);
  attributeAffects(a_operator, a_output);
  attributeAffects(a_input, a_output);

  return (MS::kSuccess);
}

MStatus Trigonometry::compute(const MPlug& plug, MDataBlock& data) {
  MStatus status;

  if (plug == a_output || plug == a_outvalue) {
    // input
    MArrayDataHandle h_input = data.inputArrayValue(a_input, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    // output
    MArrayDataHandle h_output = data.outputArrayValue(a_output, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);

    for (unsigned int i=0; i<h_input.elementCount(); i++) {
      h_input.jumpToElement(i);
      h_output.jumpToElement(i);
      // degree
      float f_degree = h_input.inputValue(&status).child(a_degree).asFloat();
      CHECK_MSTATUS_AND_RETURN_IT(status);
      // operator
      int i_operator = h_input.inputValue(&status).child(a_operator).asShort();
      CHECK_MSTATUS_AND_RETURN_IT(status);
      // negative
      int i_negative = h_input.inputValue(&status).child(a_negative).asShort();
      CHECK_MSTATUS_AND_RETURN_IT(status);

      float f_outvalue = 0.0;
      if (i_operator == 0) {
        // sine
        f_outvalue = sinf(f_degree);
      }
      if (i_operator == 1) {
        // cosine
        f_outvalue = cosf(f_degree);
      }
      if (i_operator == 2) {
        // tangent
        f_outvalue = tanf(f_degree);
      }
      if (i_negative) {
        f_outvalue *= -1.0;
      }
      h_output.outputValue().child(a_outvalue).set(f_outvalue);
    }

    data.setClean(plug);
  }

  return MS::kSuccess;
}
