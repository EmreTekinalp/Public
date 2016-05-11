#include "locator.h"
#include <maya/MFnPlugin.h>


MStatus initializePlugin( MObject obj )
{
        MStatus   status;
        MFnPlugin plugin( obj, PLUGIN_COMPANY, "6.0", "Any");

        status = plugin.registerNode( "curvedArrows", curvedArrows::id,
                                                 &curvedArrows::creator, &curvedArrows::initialize,
                                                 MPxNode::kLocatorNode );
        if (!status) {
                status.perror("registerNode");
                return status;
        }
        return status;
}

MStatus uninitializePlugin( MObject obj)
{
        MStatus   status;
        MFnPlugin plugin( obj );

        status = plugin.deregisterNode( curvedArrows::id );
        if (!status) {
                status.perror("deregisterNode");
                return status;
        }

        return status;
}
