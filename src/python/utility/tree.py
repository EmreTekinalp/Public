"""
@package: utility.tree
@brief: Tree structure
@author: Emre Tekinalp
@contact: e.tekinalp@icloud.com
"""


class BinaryTree(object):

    """Binary Tree Object Structure BTOS"""

    def __init__(self, node):
        """Class constructor"""
        self.node = node
        self._left = None
        self._right = None
    # end def __init__

    @property
    def left(self):
        """Getter function to get left"""
        return self._left
    # end def left

    @left.setter
    def left(self, node):
        """Setter function to set left"""
        if not self._left:
            self._left = Tree(node)
        else:
            t = Tree(node)
            t._left = self._left
            self._left = t
        # end if set left side
    # end def left

    @property
    def right(self):
        """Getter function to get right"""
        return self._right
    # end def right

    @right.setter
    def right(self, node):
        """Setter function to set right"""
        if not self._right:
            self._right = Tree(node)
        else:
            t = Tree(node)
            t._right = self._right
            self._right = t
        # end if set right side
    # end def right

    @property
    def value(self):
        """Get node value"""
        return self.node
    # end def value

    @value.setter
    def value(self, node):
        """Set node value"""
        self.node = node
    # end def value

    def __repr__(self):
        """Override and print Tree object structure"""
        return self.value
    # end def __repr__
# end class BinaryTree


def preorder(tree, depth=0):
    if tree:
        depth += 1
        preorder(tree.left, depth)
        preorder(tree.right, depth)
    # end if tree exists
# end def preorder
