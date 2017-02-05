#include "curveRivetNode.h"
#include <maya/MFnPlugin.h>


MStatus initializePlugin(MObject obj)
{
    MStatus status;
    MFnPlugin plugin(obj, "Emre Tekinalp", "1.0", "Any");
    status = plugin.registerNode("curveRivetNode",
                                 CurveRivetNode::id,
                                 CurveRivetNode::creator,
                                 CurveRivetNode::initialize,
                                 MPxNode::kDependNode);
    return status;
}

MStatus uninitializePlugin(MObject obj)
{
    MStatus status;
    MFnPlugin plugin(obj);
    status = plugin.deregisterNode(CurveRivetNode::id);
    return status;
}
