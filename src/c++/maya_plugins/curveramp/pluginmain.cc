// Copyright Emre Tekinalp. All rights reserved.

#include "curveramp.h"
#include <maya/MFnPlugin.h>

MStatus initializePlugin(MObject obj) {
    MFnPlugin plugin(obj, "Emre Tekinalp", "1.0", "Any");
    MStatus status = plugin.registerNode("curveRamp",
                                         CurveRamp::id,
                                         CurveRamp::creator,
                                         CurveRamp::initialize,
                                         MPxNode::kDependNode);
    return status;
} // end function initializePlugin

MStatus uninitializePlugin(MObject obj) {
    MFnPlugin plugin(obj);
    MStatus status = plugin.deregisterNode(CurveRamp::id);
    return status;
} // end function uninitializePlugin
