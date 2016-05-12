"""
@package: utility.blueprint
@brief: Base implementations of the bluePrint class
@author: Emre Tekinalp
@contact: etekinalp@rainmaker.com
"""

import pymel.core as pm
from rigging.core import base
from rigging.pandoras_box.utility import control, utils

reload(base)
reload(control)
reload(utils)

# constants
node = utils.Node()


class BluePrint(base.Base):

    """Base class of creating bluePrints."""

    def __init__(self, side=None, name=None):
        """Initialize BluePrint class"""
        super(BluePrint, self).__init__(side, name)
    # end def __init__

    def create_control(self, *args, **kwargs):
        """Create and return one control object including group."""
        node.side = self.side
        if args:
            if args[0] == 'help':
                return node.goe_locator(help)
            # end if args is help
        # end if args
        top_grp = self._create_top_group()
        ctl = control.Control(self.side, self.name).create()
        ctl.tag('BLUEPRINT')
        top_grp.attr('annotation') >> ctl.group.attr('label')
        pm.parent(ctl.group, top_grp)
        return ctl
    # end def _create_control

    def _create_top_group(self):
        """Create top group of the blueprint setup."""
        if not pm.objExists('%s_%sBlueprint_GRP' % (self.side, self.name)):
            node.suffix = 'GRP'
            grp = node.transform('%sBlueprint' % self.name)
            self._lock_attributes(grp)
            grp.addAttr('annotation', at='short', min=0, max=1, dv=1, k=True)
            return grp
        # end if create top group
        return pm.PyNode('%s_%sBlueprint_GRP' % (self.side, self.name))
    # end def _create_top_group

    def _lock_attributes(self, node):
        """Lock all attributes."""
        for at in 'trsv':
            node.attr(at).lock()
            if node.attr(at).isCompound():
                for axis in 'xyz':
                    node.attr('%s%s' % (at, axis)).setKeyable(False)
                # end for iterate axis
            # end if attr is compound
            node.attr(at).setKeyable(False)
        # end for iterate transforms
    # end def _lock_attributes
# end class Blueprint
