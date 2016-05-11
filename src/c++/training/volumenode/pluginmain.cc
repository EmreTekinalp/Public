// This is the pluginMain file

#include "volumenode.h"
#include <maya/MFnPlugin.h>

MStatus initializePlugin( MObject obj )
{
  MFnPlugin plugin( obj, "EMRE TEKINALP", "1.0", "Any");
  MStatus status = plugin.registerNode(nodename,
                                       VolumeNode::id,
                                       VolumeNode::creator,
                                       VolumeNode::initialize,
                                       MPxNode::kDeformerNode);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  return status;
}

MStatus uninitializePlugin( MObject obj)
{
  MFnPlugin plugin( obj );
  MStatus status = plugin.deregisterNode(VolumeNode::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  return status;
}
