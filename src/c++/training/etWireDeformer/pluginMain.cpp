#include "etWireDeformer.h"
#include <maya/MFnPlugin.h>


MStatus initializePlugin(MObject obj)
{
    MStatus status;
    MFnPlugin plugin(obj, "Emre Tekinalp", "1.0", "Any");
    status = plugin.registerNode("etWireDeformer",
                                 EtWireDeformer::id,
                                 EtWireDeformer::creator,
                                 EtWireDeformer::initialize,
                                 MPxNode::kDeformerNode);
    return status;
}

MStatus uninitializePlugin(MObject obj)
{
    MStatus status;
    MFnPlugin plugin(obj);
    status = plugin.deregisterNode(EtWireDeformer::id);
    return status;
}
