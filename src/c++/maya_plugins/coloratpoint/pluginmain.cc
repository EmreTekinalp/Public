// Copyright Emre Tekinalp. All rights reserved.
// This is the pluginmain file of the coloratpoint deformer node.

#include "coloratpoint.h"
#include <maya/MFnPlugin.h>

MStatus initializePlugin(MObject obj) {
    MFnPlugin plugin(obj, "Emre Tekinalp", "1.0", "Any");
    MStatus status = plugin.registerNode("coloratpoint",
                                         ColorAtPoint::id,
                                         ColorAtPoint::creator,
                                         ColorAtPoint::initialize,
                                         MPxNode::kDeformerNode);
    return status;
}

MStatus uninitializePlugin(MObject obj) {
    MFnPlugin plugin(obj);
    MStatus status = plugin.deregisterNode(ColorAtPoint::id);
    return status;
}
