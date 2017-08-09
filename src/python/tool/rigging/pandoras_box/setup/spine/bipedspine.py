"""
@package: utility.node
@brief: Base implementations of the node interfaces
@author: Emre Tekinalp
@contact: e.tekinalp@icloud.com
"""

import pymel.core as pm
from maya import cmds
from rigging.core import interface
from rigging.pandoras_box.utility import guide, control, utils

reload(control)
reload(guide)
reload(interface)
reload(utils)


# constants
node = utils.Node()


class BipedSpine(interface.RigInterface):

    """A biped spine component.

    This class is using pymel instead of python as well it is making use of the
    DropBox class, which should be used to store and retrieve any kind of data
    """

    def __init__(self, name=None, side=None):
        """Initialize the BipedSpine."""
        super(BipedSpine, self).__init__(side, name)
        # vars
        self.guides = utils.DropBox()
        self.rig = utils.DropBox()
    # end def __init__

    def guide(self):
        """Create spine guides."""
        self._create_guide_controls()
    # end def guides

    def _create_guide_controls(self):
        """Create guide controls."""
        bp = guide.BluePrint(self.side, self.name)
        spine_guides = list()
        for n in range(5):
            ctl = bp.create_control()
            ctl.group.ty.set(n * 3)
            if n:
                pm.parent(ctl.group, spine_guides[-1].transform)
            # end if parent control
            setattr(self.guides, 'spine%s' % n, ctl)
            spine_guides.append(ctl)
        # end for iterate 5 elements
        bp.name = '%sChest' % self.name
        chest = bp.create_control()
        pm.parent(chest.group, spine_guides[-1].transform)
        chest.group.t.set(0, 4, 0)
        self.guides.spine = spine_guides
        self.guides.chest = chest
    # end def _create_guide_controls

    def puppet(self):
        """Create spine puppet."""
        self._create_ribbon()
        self._create_puppet_controls()
    # end def puppet

    def _create_ribbon(self):
        """Create the ribbon spine based on the guides."""
        ribboncrv = pm.curve(p=[ctl.position() for ctl in self.guides.spine],
                             n='%s_%sRibbon_CRV' % (self.side, self.name), d=3)
        ribboncrv.listRelatives(ad=True)[0].rename('%sShape' % ribboncrv)
        crva = pm.curve(d=1, p=[ctl.position() for ctl in self.guides.spine])
        crvb = crva.duplicate()[0]
        crva.tx.set(-1)
        crvb.tx.set(1)
        nrbname = '%s_%sRibbon_NRB' % (self.side, self.name)
        loft = pm.loft(crva, crvb, n=nrbname, ch=False)[0]
        self.ribbon = pm.rebuildSurface(loft, su=0, sv=0, ch=False)
        pm.delete(crva, crvb)
    # end def _create_ribbon()

    def _create_puppet_controls(self):
        """Create spine controls based on the guides."""
        ctl = control.Control(self.side, self.name)
        # cog control
        self.rig.cog_a = ctl.create('CogA', size=7, shape=12, ovc=4)
        self.rig.cog_b = ctl.create('CogB', size=6, shape=0, ovc=25)
        # pelvis control
        self.rig.pelvis = ctl.create('Pelvis', size=3, shape=11,
                                     ovc=22, orientation=7)
        # fk controls
        self.rig.fk_base = ctl.create('BaseFk', size=4, shape=13, ovc=14)
        self.rig.fk_mid = ctl.create('MidFk', size=3, shape=13, ovc=14)
        self.rig.fk_top = ctl.create('TopFk', size=3, shape=13, ovc=14)
        # ik controls
        self.rig.ik_base = ctl.create('BaseIk', size=5, shape=0, ovc=22)
        self.rig.ik_mid = ctl.create('MidIk', size=0.4, shape=30, ovc=4,
                                     localPosition=[0, 0, -5])
        self.rig.ik_top = ctl.create('TopIk', size=5, shape=0, ovc=22)

        # TMP TEST reposition
        self.rig.fk_mid.group.t.set(self.guides.spine2.position())
        self.rig.fk_top.group.t.set(self.guides.spine4.position())

        self.rig.ik_mid.group.t.set(self.guides.spine2.position())
        self.rig.ik_top.group.t.set(self.guides.spine4.position())
    # end def _create_puppet_controls()
# end class BipedSpine

cmds.file(new=True, f=True)
spine = BipedSpine('spine')
spine.create_guide()
spine.create_puppet()
