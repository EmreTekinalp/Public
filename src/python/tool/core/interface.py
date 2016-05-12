"""
@package: core.interface
@brief: Core project agnostic interface
@author: Emre Tekinalp
@contact: e.tekinalp@icloud.com
"""

import os
import sys
import pymel.core as pm
import logging

reload(logging)
logging.basicConfig(format='', level=logging.ERROR)


class AssetInterface(object):

    """Asset interface class reading id node in maya scene."""

    def __init__(self):
        """Initialize AssetInterface class."""
        # vars
        self.id = None

        # methods
        self.get_id_node()
    # end def __init__

    def get_id_node(self):
        """Return id node."""
        if self.id:
            return self.id
        # end if return id node

        self.id = pm.ls('ID')
        if not self.id:
            return logging.error('No ID node found in maya scene!')
        # end if error id node
        return self.id
    # end def get_id_node

    def _get_project_name(self):
        """Retrieve project name."""
        pass
    # end def _get_project_name

    def _get_asset_name(self):
        """Retrieve asset name."""
        pass
    # end def _get_asset_name

    def _get_rig_build_path(self):
        """Retrieve rig build path."""
        pass
    # end def _get_rig_build_path

    def _get_rig_data_path(self):
        """Retrieve rig data path."""
        pass
    # end def _get_rig_data_path
# end class AssetInterface
