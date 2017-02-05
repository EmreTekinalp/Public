// Copyright Emre Tekinalp. All rights reserved.
// This is the cc source file of the ecurve deformer.

#include "ecurve.h"
#include <maya/MFnPlugin.h>

MStatus initializePlugin(MObject obj) {
    MStatus status;
    MFnPlugin plugin(obj, "Emre Tekinalp", "1.0", "Any");
    status = plugin.registerNode("ecurve", Ecurve::id, Ecurve::creator,
                                 Ecurve::initialize, MPxNode::kDeformerNode);
    return status;
}

MStatus uninitializePlugin(MObject obj) {
    MStatus status;
    MFnPlugin plugin(obj);
    status = plugin.deregisterNode(Ecurve::id);
    return status;
}
