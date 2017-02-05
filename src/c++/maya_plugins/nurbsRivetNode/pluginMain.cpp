#include "nurbsRivetNode.h"
#include <maya/MFnPlugin.h>


MStatus initializePlugin(MObject obj)
{
    MStatus status;
    MFnPlugin plugin(obj, "Emre Tekinalp", "1.0", "Any");
    status = plugin.registerNode("nurbsRivetNode",
                                 NurbsRivetNode::id,
                                 NurbsRivetNode::creator,
                                 NurbsRivetNode::initialize,
                                 MPxNode::kDependNode);
    return status;
}

MStatus uninitializePlugin(MObject obj)
{
    MStatus status;
    MFnPlugin plugin(obj);
    status = plugin.deregisterNode(NurbsRivetNode::id);
    return status;
}
