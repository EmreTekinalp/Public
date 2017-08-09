"""
@package: utility.control
@brief: Base implementations of the control class
@author: Emre Tekinalp
@contact: etekinalp@rainmaker.com
"""

import pymel.core as pm
from rigging.core import base, interface
from rigging.pandoras_box.utility import utils

reload(base)
reload(interface)
reload(utils)

# constants
node = utils.Node()


class Control(base.Base):

    """Control class inheriting BaseInterface which returns a control object.

    @requires from src.python.core import base, interface
              from src.python.utility import utils
    """

    def __init__(self, side=None, name=None):
        """Initialize Control class"""
        super(Control, self).__init__(side, name)
    # end def __init__

    def create(self, *args, **kwargs):
        """Create a control object"""
        index = self._get_index()
        ci = interface.ControlInterface()
        description = '%s%s' % (self.name, index)
        if args:
            if isinstance(args[0], str):
                description = '%s%s' % (self.name, args[0])
                args = args[1:]
            # end if first argument is a string
        # end if arguments specified
        ci.group = node.transform(description)
        ci.shape = node.goe_locator('%sShape' % description, *args, **kwargs)
        ci.shape.rename('%s%sShape' % (ci.shape.split('Shape')[0],
                                       ci.shape.split('Shape')[1]))
        ci.transform = ci.shape.listRelatives(p=True)[0]
        pm.parent(ci.transform, ci.group)
        ci.shape.attr('ove').set(1)
        if not ci.shape.attr('ovc').get():
            ci.shape.attr('ovc').set(self._get_color())
        # end if no color specified
        self._add_annotation(ci, '%s' % (description))
        return ci
    # end def create

    def _get_index(self, name=None, index='', count=0):
        """Recursively check duplicates in the scene and return index.
        @todo fix index issue.
        """
        ctlname = '%s_%s%s_CTL' % (self.side, self.name, index)
        if not pm.objExists(ctlname):
            return index
        # end if name does not exists
        return self._get_index(ctlname, count + 1, count + 1)
    # end def _get_index

    def _get_color(self):
        """Based on the given side return the proper maya color."""
        if self.side in ['C', 'c']:
            return 17
        elif self.side in ['L', 'l']:
            return 6
        elif self.side in ['R', 'r']:
            return 13
        # end if return maya color value
    # end def _get_color

    def _add_annotation(self, control, name):
        """Implement annotation shape and merge with control shape."""
        control.group.addAttr('label', at='short', min=0, max=1, dv=1, k=True)
        ano = pm.annotate(control.transform, text=name)
        ano.rename('%s_%s_ANOShape' % (self.side, name))
        ano.ove.set(1)
        ano.ovdt.set(2)
        trn = ano.listRelatives(p=True)[0]
        trn.rename('%s_%s_ANO' % (self.side, name))
        trn.tz.set(control.shape.attr('size').get() * 2)
        pm.parent(trn, control.transform)
        control.group.attr('label') >> ano.v
    # end def _add_annotation
# end class Control
