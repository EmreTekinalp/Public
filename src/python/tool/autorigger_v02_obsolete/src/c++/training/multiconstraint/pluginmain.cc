// Copyright Emre Tekinalp. All rights reserved.

#include "multiconstraint.h"
#include <maya/MFnPlugin.h>

MStatus initializePlugin(MObject obj) {
    MFnPlugin plugin(obj, "Emre Tekinalp", "1.0", "Any");
    MStatus status = plugin.registerNode("multiConstraint",
                                         MultiConstraint::id,
                                         MultiConstraint::creator,
                                         MultiConstraint::initialize,
                                         MPxNode::kDependNode);
    return status;
}

MStatus uninitializePlugin(MObject obj) {
    MFnPlugin plugin(obj);
    MStatus status = plugin.deregisterNode(MultiConstraint::id);
    return status;
}
