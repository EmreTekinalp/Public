"""
@package: rigFunctions.tree
@brief: Module with different Tree Object Structures
@author: Emre Tekinalp
@contact: e.tekinalp@icloud.com
"""

import numpy


class BinaryTree(object):

    """Binary Tree Object Structure BTOS."""

    def __init__(self, node):
        """Class constructor to initialize Tree"""
        self.node = node
        self._left = None
        self._right = None
    # end def __init__

    @property
    def left(self):
        """Read only getter function to get left branch"""
        return self._left
    # end def left

    @left.setter
    def left(self, node):
        """Write only setter function to set left branch"""
        if not self._left:
            self._left = BinaryTree(node)
        else:
            t = BinaryTree(node)
            t._left = self._left
            self._left = t
        # end if set left side
    # end def left

    @property
    def right(self):
        """Read only getter function to get right branch"""
        return self._right
    # end def right

    @right.setter
    def right(self, node):
        """Write only setter function to set right branch"""
        if not self._right:
            self._right = BinaryTree(node)
        else:
            t = BinaryTree(node)
            t._right = self._right
            self._right = t
        # end if set right side
    # end def right

    @property
    def value(self):
        """Read only getter function to get node value"""
        return self.node
    # end def value

    @value.setter
    def value(self, node):
        """Write only setter function to set node value"""
        self.node = node
    # end def value
# end class BinaryTree


def find_median(values, function):
    """Find medians of list, store in btos and run function to do something.

    @param values list of sortable values. Note: values list will NOT be sorted!
    @param function method which takes two parameters: tree object and median
                    example:

                    def f(tree, median):
                        '''Do something with the tree object and int median.'''
                        print tree.value, median
                    # end def f

                    find_median([0, 1, 2, 3, 4, 5, 6, 7, 8], f)

    @requires import of numpy to calculate the median

    @todos implement depth level for the search of medians
    """

    tree = BinaryTree([values[0], values[-1]])

    def add(t):
        """Traverse the tree, populate with values and run external function.

        @param t binary tree object
        """

        median = int(numpy.median(t.value))
        if t.value[-1] - t.value[0] == 1:
            return
        # end if break recursion

        # external function call
        function(t, median)

        if median <= 1:
            return
        # end if break recursion
        t.left = [t.value[0], median]
        t.right = [median, t.value[-1]]
        add(t.left)
        add(t.right)
    # end def add
    add(tree)
# end def find_median
