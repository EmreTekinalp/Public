// Copyright Emre Tekinalp. All rights reserved.
// This is the cc source file of the coloratpoint deformer node.

#include "coloratpoint.h"

MTypeId ColorAtPoint::id(0x1371817);
MObject ColorAtPoint::a_blendmesh;

ColorAtPoint::ColorAtPoint() {
}

ColorAtPoint::~ColorAtPoint() {
}

void* ColorAtPoint::creator() {
  return new ColorAtPoint();
}

MStatus ColorAtPoint::initialize() {
  // Create function sets for attributes
  MFnEnumAttribute e_attr;
  MFnTypedAttribute t_attr;
  MFnNumericAttribute n_attr;

  // inMesh
  a_blendmesh = t_attr.create("blendMesh", "blm", MFnData::kMesh);
  t_attr.setReadable(true);
  t_attr.setWritable(true);
  t_attr.setKeyable(false);
  CHECK_MSTATUS(addAttribute(a_blendmesh));

  attributeAffects(a_blendmesh, outputGeom);

  MGlobal::executeCommand("makePaintable -attrType multiFloat -sm deformer coloratpoint weights;");

  return (MS::kSuccess);
}

MStatus ColorAtPoint::deform(MDataBlock& data, MItGeometry& iter,
                             const MMatrix& mat, unsigned int mindex) {
  MStatus status;

  // Get inputGeom
  MArrayDataHandle h_input = data.outputArrayValue(input, &status);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  status = h_input.jumpToElement(0);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  MObject o_inputgeom = h_input.outputValue().child(inputGeom).asMesh();
  if (! o_inputgeom.hasFn(MFn::kMesh)) {
    return MS::kUnknownParameter;
  }

  // Get blendMesh
  MObject o_blendmesh = data.inputValue(a_blendmesh, &status).asMesh();
  CHECK_MSTATUS_AND_RETURN_IT(status);
  if (! o_blendmesh.hasFn(MFn::kMesh)) {
    return MS::kUnknownParameter;
  }

  // Get envelope
  float f_env = data.inputValue(envelope).asFloat();

  MFnMesh fn_blendmesh(o_blendmesh, &status);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  MPointArray pa_blendpoints, pa_finalpoints(iter.count());
  fn_blendmesh.getPoints(pa_blendpoints);

  MColorArray ca_blendpoints;
  status = fn_blendmesh.getVertexColors(ca_blendpoints);
  if (! status) {
      return MS::kUnknownParameter;
  }
  CHECK_MSTATUS_AND_RETURN_IT(status);

  for (; !iter.isDone(); iter.next()) {
    float f_weights = weightValue(data, mindex, iter.index());
    MPoint p_vtx = iter.position();
    p_vtx += (pa_blendpoints[iter.index()] - p_vtx) * f_env * f_weights * ca_blendpoints[iter.index()][0];
    pa_finalpoints[iter.index()] = p_vtx;
  }
  iter.setAllPositions(pa_finalpoints);

  return MS::kSuccess;
}
