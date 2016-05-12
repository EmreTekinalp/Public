#include "quaternions.h"
#include <maya/MFnPlugin.h>


MStatus initializePlugin(MObject obj)
{
    MStatus status;
    MFnPlugin plugin(obj, "Emre Tekinalp", "1.0", "Any");
    status = plugin.registerNode("quaternions",
                                 Quaternions::id,
                                 Quaternions::creator,
                                 Quaternions::initialize,
                                 MPxNode::kDependNode);
    return status;
}

MStatus uninitializePlugin(MObject obj)
{
    MStatus status;
    MFnPlugin plugin(obj);
    status = plugin.deregisterNode(Quaternions::id);
    return status;
}
