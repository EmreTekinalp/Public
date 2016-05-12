// This is the VolumeNodeNode source file

#include "volumenode.h"

// volumeNode
MTypeId VolumeNode::id(0x3848523);
MObject VolumeNode::a_volumeinvmatrix;
MObject VolumeNode::a_falloff;
MObject VolumeNode::a_multiplier;
MObject VolumeNode::a_meshdata;

VolumeNode::VolumeNode()
{
  // empty constructor function
} // end constructor

VolumeNode::~VolumeNode()
{
  // empty deconstructor function
} // end deconstructor

void* VolumeNode::creator()
{
  // creator function to recreate node
  return new VolumeNode();
} // end creator

MStatus VolumeNode::initialize()
{
  MStatus status;
  // declare attributes
  MFnMatrixAttribute m_attr;
  MFnNumericAttribute n_attr;
  MFnTypedAttribute t_attr;
  MFnCompoundAttribute c_attr;

  // volumeInverseMatrix
  a_volumeinvmatrix = m_attr.create("volumeInverseMatrix", "vim");
  CHECK_MSTATUS(addAttribute(a_volumeinvmatrix));

  // falloff
  a_falloff = n_attr.create("falloff", "fof", MFnNumericData::kFloat, 1.0);
  CHECK_MSTATUS(n_attr.setKeyable(true));
  CHECK_MSTATUS(addAttribute(a_falloff));

  // multiplier
  a_multiplier = n_attr.create("multiplier", "mlt", MFnNumericData::kFloat, 1.0);
  CHECK_MSTATUS(n_attr.setKeyable(true));
  CHECK_MSTATUS(addAttribute(a_multiplier));

  // meshdata
  a_meshdata = t_attr.create("meshdata", "md", MFnData::kPointArray);
  CHECK_MSTATUS(t_attr.setHidden(true));
  CHECK_MSTATUS(addAttribute(a_meshdata));

  // affect attributes
  CHECK_MSTATUS(attributeAffects(a_volumeinvmatrix, outputGeom));
  CHECK_MSTATUS(attributeAffects(a_falloff, outputGeom));
  CHECK_MSTATUS(attributeAffects(a_multiplier, outputGeom));
  CHECK_MSTATUS(attributeAffects(a_meshdata, outputGeom));

  return status;
} // end initialize

MStatus VolumeNode::deform(MDataBlock& data, MItGeometry& iter,
                           const MMatrix& mat, unsigned int multiIndex)
{
  MStatus status;

  MArrayDataHandle h_input = data.inputArrayValue(input, &status);
  h_input.jumpToElement(multiIndex);
  MObject o_inputgeom = h_input.inputValue(&status).child(inputGeom).asMesh();
  CHECK_MSTATUS_AND_RETURN_IT(status);
  MFnMesh fn_inputgeom(o_inputgeom);

  // store init mesh vertex data in array attribute
  MDataHandle h_meshdata = data.inputValue(a_meshdata, &status);
  MObject o_meshdata = h_meshdata.data();
  MPointArray pa_meshdata;
  if (! o_meshdata.hasFn(MFn::kPointArrayData)) {
    iter.position();
    MFnPointArrayData pad_meshdata;
    iter.allPositions(pa_meshdata);
    MObject od_meshdata = pad_meshdata.create(pa_meshdata, &status);
    h_meshdata.set(od_meshdata);
  }
  else {
    MFnPointArrayData pad_meshdata(o_meshdata);
    pa_meshdata = pad_meshdata.array();
  } // end if

  MItMeshVertex it_inputgeom(o_inputgeom);
  MMatrix m_vim = data.inputValue(a_volumeinvmatrix, &status).asMatrix();
  MMatrix m_invim = m_vim.inverse();
  float f_falloff = data.inputValue(a_falloff, &status).asFloat();
  float f_multiplier = data.inputValue(a_multiplier, &status).asFloat();
  MPointArray pa_points;
  int i_prev;
  iter.allPositions(pa_points);
  for (; !iter.isDone(); iter.next()) {
    MVector v_vtx = ((iter.position() * mat) * m_vim) * f_falloff;
    MIntArray ia_adjacent;
    MVector v_normal;
    if (v_vtx.length() <= 1.0) {
      fn_inputgeom.getVertexNormal(iter.index(), v_normal, MSpace::kWorld);
      pa_points[iter.index()] -= (v_normal * (1.0 - v_vtx.length())) * f_multiplier;
      // get adjacent vertices of the current vertex
      it_inputgeom.setIndex(iter.index(), i_prev);
      it_inputgeom.getConnectedVertices(ia_adjacent);
      } // end for
    if (ia_adjacent.length() < 5) {
      for (int i=0; i < ia_adjacent.length(); i++) {
          pa_points[ia_adjacent[i]] = pa_points[ia_adjacent[i]] - ((v_normal * (1.0 - v_vtx.length())) * 0.25);
        }
    } // end if
  } // end for
  iter.setAllPositions(pa_points);

  return MS::kSuccess;
} // end compute
