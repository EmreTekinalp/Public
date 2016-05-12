// Copyright Emre Tekinalp. All rights reserved.
// This is the cc source file of the ecurve deformer.

#include "blendcurve.h"
#include <maya/MFnPlugin.h>

MStatus initializePlugin(MObject obj) {
    MStatus status;
    MFnPlugin plugin(obj, "Emre Tekinalp", "1.0", "Any");
    status = plugin.registerNode("blendcurve", BlendCurve::id, BlendCurve::creator,
                                 BlendCurve::initialize, MPxNode::kDeformerNode);
    return status;
}

MStatus uninitializePlugin(MObject obj) {
    MStatus status;
    MFnPlugin plugin(obj);
    status = plugin.deregisterNode(BlendCurve::id);
    return status;
}
