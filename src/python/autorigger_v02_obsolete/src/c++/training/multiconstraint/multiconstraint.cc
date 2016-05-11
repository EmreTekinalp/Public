// Copyright Emre Tekinalp. All rights reserved.

#include "multiconstraint.h"

MTypeId MultiConstraint::id(0x4848487);
MObject MultiConstraint::a_input;
MObject MultiConstraint::a_inmatrix;
MObject MultiConstraint::a_operator;
MObject MultiConstraint::a_operatormo;
MObject MultiConstraint::a_scale;
MObject MultiConstraint::a_scalemo;

MObject MultiConstraint::a_output;
MObject MultiConstraint::a_outtranslate;
MObject MultiConstraint::a_outrotate;
MObject MultiConstraint::a_outrotatex;
MObject MultiConstraint::a_outrotatey;
MObject MultiConstraint::a_outrotatez;
MObject MultiConstraint::a_outscale;
MObject MultiConstraint::a_outscalex;
MObject MultiConstraint::a_outscaley;
MObject MultiConstraint::a_outscalez;

MultiConstraint::MultiConstraint() {
}

MultiConstraint::~MultiConstraint() {
}

void* MultiConstraint::creator() {
  return new MultiConstraint();
}

MStatus MultiConstraint::initialize() {
  // Create function sets for attributes
  MFnEnumAttribute e_attr;
  MFnNumericAttribute n_attr;
  MFnCompoundAttribute c_attr;
  MFnMatrixAttribute m_attr;
  MFnUnitAttribute u_attr;

  // inmatrix
  a_inmatrix = m_attr.create("inMatrix", "inm");
  m_attr.setHidden(true);

  // operator
  a_operator = e_attr.create("constraint", "cnt");
  e_attr.addField("Point", 0);
  e_attr.addField("Orient", 1);
  e_attr.addField("Parent", 2);
  e_attr.setKeyable(true);

  // operatormo
  a_operatormo = n_attr.create("constraintMaintainOffset", "cmo",
                               MFnNumericData::kBoolean);
  n_attr.setKeyable(true);

  // scale
  a_scale = n_attr.create("addScaleConstraint", "scn",
                          MFnNumericData::kBoolean);
  n_attr.setKeyable(true);

  // scalemo
  a_scalemo = n_attr.create("addScaleMaintainOffset", "smo",
                            MFnNumericData::kBoolean);
  n_attr.setKeyable(true);

  // input
  a_input = c_attr.create("input", "in");
  c_attr.setArray(true);
  c_attr.setKeyable(true);
  c_attr.addChild(a_inmatrix);
  c_attr.addChild(a_operator);
  c_attr.addChild(a_operatormo);
  c_attr.addChild(a_scale);
  c_attr.addChild(a_scalemo);
  CHECK_MSTATUS(addAttribute(a_input));

  // outtranslate
  a_outtranslate = n_attr.createPoint("outTranslate", "ot");
  n_attr.setHidden(true);

  // outrotate
  a_outrotatex = u_attr.create("outRotateX", "orx",
                               MFnUnitAttribute::kAngle, 0.0);
  u_attr.setWritable(false);
  u_attr.setStorable(false);
  u_attr.setHidden(true);
  CHECK_MSTATUS(addAttribute(a_outrotatex));

  a_outrotatey = u_attr.create("outRotateY", "ory",
                               MFnUnitAttribute::kAngle, 0.0);
  u_attr.setWritable(false);
  u_attr.setStorable(false);
  u_attr.setHidden(true);
  CHECK_MSTATUS(addAttribute(a_outrotatey));

  a_outrotatez = u_attr.create("outRotateZ", "orz",
                               MFnUnitAttribute::kAngle, 0.0);
  u_attr.setWritable(false);
  u_attr.setStorable(false);
  u_attr.setHidden(true);
  CHECK_MSTATUS(addAttribute(a_outrotatez));

  a_outrotate = n_attr.create("outRotate", "or",
                              a_outrotatex, a_outrotatey, a_outrotatez);
  n_attr.setWritable(false);
  n_attr.setStorable(false);
  n_attr.setHidden(true);
  CHECK_MSTATUS(addAttribute(a_outrotate));

  a_outscale = n_attr.createPoint("outScale", "os");
  n_attr.setWritable(false);
  n_attr.setStorable(false);
  n_attr.setHidden(true);
  CHECK_MSTATUS(addAttribute(a_outscale));

  // output
  a_output = c_attr.create("output", "out");
  c_attr.setArray(true);
  c_attr.addChild(a_outtranslate);
  c_attr.addChild(a_outrotate);
  c_attr.addChild(a_outscale);
  CHECK_MSTATUS(addAttribute(a_output));

  // affect attributes
  attributeAffects(a_input, a_output);
  attributeAffects(a_input, a_outtranslate);
  attributeAffects(a_input, a_outrotate);
  attributeAffects(a_input, a_outscale);

  attributeAffects(a_inmatrix, a_outtranslate);
  attributeAffects(a_inmatrix, a_outrotate);
  attributeAffects(a_inmatrix, a_outscale);

  attributeAffects(a_operator, a_outtranslate);
  attributeAffects(a_operator, a_outrotate);
  attributeAffects(a_operator, a_outscale);

  attributeAffects(a_operatormo, a_outtranslate);
  attributeAffects(a_operatormo, a_outrotate);
  attributeAffects(a_operatormo, a_outscale);

  attributeAffects(a_scale, a_outtranslate);
  attributeAffects(a_scale, a_outrotate);
  attributeAffects(a_scale, a_outscale);

  attributeAffects(a_scalemo, a_outtranslate);
  attributeAffects(a_scalemo, a_outrotate);
  attributeAffects(a_scalemo, a_outscale);

  return (MS::kSuccess);
}

MStatus MultiConstraint::compute(const MPlug& plug, MDataBlock& data) {
  MStatus status;

  if (plug == a_output || plug == a_outtranslate ||
      plug == a_outrotate || plug == a_outscale) {
    // input
    MArrayDataHandle h_input = data.inputArrayValue(a_input, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);

    // output
    MArrayDataHandle h_output = data.outputArrayValue(a_output, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);

    cout << h_input.elementCount() << endl;
    for (unsigned int i=0; i<h_input.elementCount(); i++) {
      h_input.jumpToElement(i);
      cout << i << endl;
      // inMatrix
      MMatrix m_matrix = h_input.inputValue().child(a_inmatrix).asMatrix();
//      // operator
//      int i_operator = data.inputValue(a_operator, &status).asShort();
//      CHECK_MSTATUS_AND_RETURN_IT(status);
//      // operatormo
//      int i_operatormo = data.inputValue(a_operatormo, &status).asShort();
//      CHECK_MSTATUS_AND_RETURN_IT(status);

      h_output.jumpToElement(i);
      MTransformationMatrix tm_inmatrix(m_matrix);

      // outtranslate
      MDataHandle h_outtranslate = h_output.outputValue().child(a_outtranslate);
      MFloatVector fv_translation = tm_inmatrix.translation(MSpace::kWorld);
      h_outtranslate.set(fv_translation);

      // outrotate
      MDataHandle h_outrotate = h_output.outputValue().child(a_outrotate);
      double d_rotation[3];
      MFloatVector fa_rotation;
      MTransformationMatrix::RotationOrder rot_order = MTransformationMatrix::kXYZ;
      tm_inmatrix.getRotation(d_rotation, rot_order, MSpace::kWorld);
      h_outrotate.set(d_rotation[0], d_rotation[1], d_rotation[2]);

//      // outscale
//      MDataHandle h_outscale = h_output.outputValue().child(a_outscale);
//      double d_scale[3];
//      tm_inmatrix.getScale(d_scale, MSpace::kWorld);
//      h_outscale.set(d_scale[0], d_scale[1], d_scale[2]);
    }
    data.setClean(plug);
  }

  return MS::kSuccess;
}
