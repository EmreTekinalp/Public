#include "volumePushCollider.h"
#include <maya/MFnPlugin.h>


MStatus initializePlugin(MObject obj)
{
    MStatus status;
    MFnPlugin plugin(obj, "Emre Tekinalp", "1.0", "Any");
    status = plugin.registerNode("volumePushCollider",
    							 VolumePushCollider::id,
    							 VolumePushCollider::creator,
    							 VolumePushCollider::initialize,
    							 MPxNode::kDependNode);
    return status;
}

MStatus uninitializePlugin(MObject obj)
{
    MStatus status;
    MFnPlugin plugin(obj);
    status = plugin.deregisterNode(VolumePushCollider::id);
    return status;
}
