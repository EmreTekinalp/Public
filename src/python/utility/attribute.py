"""
@package: utility.attribute
@brief: Useful methods to access and modify maya attributes
@author: Emre Tekinalp
@contact: e.tekinalp@icloud.com
"""


import pymel.core as pm


def connect_construction_history(connector=None, nodes=[]):
    """Retrieve and connect construction history of specified nodes or all.

    @param connector <string> Control which switches ihi attr of connected node
    @param nodes <list> Nodes to connect their isHistoricallyInteresting attr

    @return pyNode of the connector storing the showHistory attribute
    """

    if not nodes:
        selection = pm.ls(sl=True)
        if selection:
            nodes = selection
        else:
            nodes = pm.ls()
        # end if nodes are selected or select all
    else:
        nodes = [pm.PyNode(node) for node in nodes]
    # end if no nodes specified

    if not connector:
        if not pm.objExists('ConstructionHistory'):
            connector = pm.createNode('transform', n='ConstructionHistory')
        else:
            connector = pm.PyNode('ConstructionHistory')
        # end if create ConstructionHistory
    else:
        connector = pm.PyNode(connector)
    # end if create connector pyNode

    if not pm.objExists('%s.showHistory' % connector):
        connector.addAttr('showHistory', at='short', min=0, max=1)
        connector.showHistory.set(e=True, cb=True)
    # end if create attribute

    for node in nodes:
        if not pm.isConnected(connector.showHistory, node.ihi):
            connector.showHistory >> node.ihi
        # end if no connection has been done
    # end for connect attributes

    return connector
# end def connect_construction_history
