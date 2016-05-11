#include "rivetNode.h"
#include <maya/MFnPlugin.h>


MStatus initializePlugin(MObject obj)
{
    MStatus status;
    MFnPlugin plugin(obj, "Emre Tekinalp", "1.0", "Any");
    status = plugin.registerNode("rivetNode",
                                 RivetNode::id,
                                 RivetNode::creator,
                                 RivetNode::initialize,
                                 MPxNode::kDependNode);
    return status;
}

MStatus uninitializePlugin(MObject obj)
{
    MStatus status;
    MFnPlugin plugin(obj);
    status = plugin.deregisterNode(RivetNode::id);
    return status;
}
