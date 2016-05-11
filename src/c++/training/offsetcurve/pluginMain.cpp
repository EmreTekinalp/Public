#include "offsetcurve.h"
#include <maya/MFnPlugin.h>


MStatus initializePlugin(MObject obj)
{
    MStatus status;
    MFnPlugin plugin(obj, "Emre Tekinalp", "1.0", "Any");
    status = plugin.registerNode("offsetcurve", OffsetCurve::id,
    							 OffsetCurve::creator,
    							 OffsetCurve::initialize,
    							 MPxNode::kDependNode);
    return status;
}

MStatus uninitializePlugin(MObject obj)
{
    MStatus status;
    MFnPlugin plugin(obj);
    status = plugin.deregisterNode(OffsetCurve::id);
    return status;
}
