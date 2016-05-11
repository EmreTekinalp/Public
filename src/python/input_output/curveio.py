"""
@package: io.curveio
@brief: Save and load nurbsCurves in json files
@author: Emre Tekinalp
@contact: e.tekinalp@icloud.com
"""


import pymel.core as pm
from input_output import baseio
reload(baseio)


class CurveIO(baseio.BaseIO):
    """IO class for nurbsCurves creating data to be saved as json or xml."""

    def __init__(self):
        """Initialize CurveIO class subclassing from BaseIO."""
        super(CurveIO, self).__init__()
    # end def __init__

    def valid_nodetype(self):
        """Return valid nodetype as string in a list."""
        return ['nurbsCurve']
    # end def valid_nodetype

    def data(self):
        """Setup IO specific data and return the result."""
        curves = dict()
        nrbcurves = pm.ls(type=self.valid_nodetype())
        for crv in nrbcurves:
            if pm.objExists('%s.%s' % (crv, self)):
                curves[crv] = crv.getCVs()
            # end if retrieve tagged curve data
        # end for iterate all curves in scene
        return curves
    # end def data
# end class CurveIO


def create_id_node():
    """Create id node if it does not exist in maya scene."""
    id = None
    if not pm.objExists('ID'):
        id = pm.createNode('transform', n='ID')
    else:
        pm.PyNode('ID')
    # end if create id node

    id_attributes = ['PROJECT_NAME_ID', 'ASSET_NAME_ID',
                     'RIG_BUILD_PATH_ID', 'RIG_DATA_PATH_ID']
    for attr in id_attributes:
        if not pm.objExists('%s.%s' % (id, attr)):
            id.addAttr(attr, dt='string', k=True)
        # end if add attributes
    # end for iterate id attributes
    return id
# end def create_id_node

# create_id_node()
cio = CurveIO()
cio.tag_nodes()
cio.save()
