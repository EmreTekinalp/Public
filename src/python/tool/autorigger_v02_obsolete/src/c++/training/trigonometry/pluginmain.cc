// Copyright Emre Tekinalp. All rights reserved.

#include "trigonometry.h"
#include <maya/MFnPlugin.h>

MStatus initializePlugin(MObject obj) {
    MFnPlugin plugin(obj, "Emre Tekinalp", "1.0", "Any");
    MStatus status = plugin.registerNode("trigonometry",
                                         Trigonometry::id,
                                         Trigonometry::creator,
                                         Trigonometry::initialize,
                                         MPxNode::kDependNode);
    return status;
}

MStatus uninitializePlugin(MObject obj) {
    MFnPlugin plugin(obj);
    MStatus status = plugin.deregisterNode(Trigonometry::id);
    return status;
}
