"""
@package: test.testbuild
@brief: Test builder file
@author: Emre Tekinalp
@contact: e.tekinalp@icloud.com
"""

import os

from pandoras_box.construct.generic import primitive
from pandoras_box.construct import constructor
reload(constructor)
reload(primitive)


def builder(STAGE):
    """Build the setup"""
    # create basic primitive
    main = primitive.Basic('C', 'main')

    cnst = constructor.Constructor()
    cnst.element = main

    cnst.construct(STAGE)

    adjust()
# end def builder

def adjust():
    """Additional fixes for the setup."""
    pass
# end def adjust

print constructor.__file__
builder(1)
