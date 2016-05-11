"""
@package: utility.control
@brief: Base implementations of the control class
@author: Emre Tekinalp
@contact: etekinalp@rainmaker.com
"""

from maya import OpenMayaMPx
from plugins.goe_collection import goe_locator
reload(goe_locator)


def initializePlugin(obj):
    """Initialize plugins."""
    plugin = OpenMayaMPx.MFnPlugin(obj, 'Gravity_of_Explosion', '1.0', 'Any')
    try:
        plugin.registerNode(goe_locator.nodename,
                            goe_locator.nodeid,
                            goe_locator.nodeCreator,
                            goe_locator.nodeInitializer,
                            OpenMayaMPx.MPxNode.kLocatorNode,
                            'general/transform/drawdb')
    except:
        raise Exception('Failed to load plugin: %s' % goe_locator.nodename)
# end def initializePlugin()


def uninitializePlugin(obj):
    """Uninitialize plugins."""
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(goe_locator.nodeid)
    except:
        raise Exception('Failed to unload plugin: %s' % goe_locator.nodename)
# end def uninitializePlugin()
