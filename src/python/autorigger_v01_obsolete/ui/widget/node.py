"""Created on 2014/01/21
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: The graphic representation of a node
"""


class Node(object):
    """A basic node object from which all other nodes are inheriting.
     @param model: The data object, that holds all the informations for the node.

    """
    def __init__(self, model):
        super(Node, self).__init__()
        self.model = model
        self.has_changed = False
    # end def __init__
# end class Node
