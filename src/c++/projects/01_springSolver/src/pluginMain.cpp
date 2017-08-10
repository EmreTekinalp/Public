#include "springSolver.h"
#include <maya/MFnPlugin.h>

MStatus initializePlugin(MObject obj) {
    MFnPlugin plugin(obj, "Emre Tekinalp", "1.0", "Any");
    MStatus status = plugin.registerNode("singleSpring",
                                         SpringSolver::id,
                                         SpringSolver::creator,
                                         SpringSolver::initialize,
                                         MPxNode::kDependNode);
    return status;
}

MStatus uninitializePlugin(MObject obj) {
    MFnPlugin plugin(obj);
    MStatus status = plugin.deregisterNode(SpringSolver::id);
    return status;
}
