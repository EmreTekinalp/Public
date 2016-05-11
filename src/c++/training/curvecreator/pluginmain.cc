// Copyright Emre Tekinalp. All rights reserved.
// This is the cc source file of the curvecreator deformer.

#include "curvecreator.h"
#include <maya/MFnPlugin.h>

MStatus initializePlugin(MObject obj) {
    MFnPlugin plugin(obj, "Emre Tekinalp", "1.0", "Any");
    MStatus status = plugin.registerNode("curveCreator",
                                         CurveCreator::id,
                                         CurveCreator::creator,
                                         CurveCreator::initialize,
                                         MPxNode::kDeformerNode);
    return status;
}

MStatus uninitializePlugin(MObject obj) {
    MFnPlugin plugin(obj);
    MStatus status = plugin.deregisterNode(CurveCreator::id);
    return status;
}
