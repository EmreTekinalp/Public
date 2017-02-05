#include "rampoffset.h"
#include <maya/MFnPlugin.h>


MStatus initializePlugin(MObject obj)
{
  MFnPlugin plugin(obj, "Emre Tekinalp", "1.0", "Any");
  MStatus status = plugin.registerNode("rampOffset",
                                       RampOffset::id,
                                       RampOffset::creator,
                                       RampOffset::initialize,
                                       MPxNode::kDependNode);
  return status;
} // end initializePlugin

MStatus uninitializePlugin(MObject obj)
{
  MFnPlugin plugin(obj);
  MStatus status = plugin.deregisterNode(RampOffset::id);
  return status;
} // end uninitializePlugin
