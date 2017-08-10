#include "pftCurve.h"
#include <maya/MFnPlugin.h>

MStatus initializePlugin(MObject obj) {
    MFnPlugin plugin(obj, "Emre Tekinalp", "1.0", "Any");
    MStatus status = plugin.registerNode("pftCurve",
                                         PftCurve::id,
                                         PftCurve::creator,
                                         PftCurve::initialize,
                                         MPxNode::kDeformerNode);
    return status;
}

MStatus uninitializePlugin(MObject obj) {
    MFnPlugin plugin(obj);
    MStatus status = plugin.deregisterNode(PftCurve::id);
    return status;
}
