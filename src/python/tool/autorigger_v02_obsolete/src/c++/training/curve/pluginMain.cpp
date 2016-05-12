#include "curve.h"
#include <maya/MFnPlugin.h>


MStatus initializePlugin(MObject obj)
{
    MStatus status;
    MFnPlugin plugin(obj, "Emre Tekinalp", "1.0", "Any");
    status = plugin.registerNode("etcurve",
                                 Curve::id,
                                 Curve::creator,
                                 Curve::initialize,
                                 MPxNode::kDeformerNode);
    return status;
}

MStatus uninitializePlugin(MObject obj)
{
    MStatus status;
    MFnPlugin plugin(obj);
    status = plugin.deregisterNode(Curve::id);
    return status;
}
