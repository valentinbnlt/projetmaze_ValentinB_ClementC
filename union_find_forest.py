"""
title: union find avec des foret
author: qkzk
date: 2021/02/22
"""


class Tree:
    """Simple tree structure"""

    def __init__(self, element, parent=None):
        self.element = element
        self.parent = parent
        self.rank = 0

    def __repr__(self):
        if self.parent is None:
            return f"Tree({self.element})"
        return f"Tree({self.parent}, {self.element})"


class UnionFind:
    """UnionFind with forrest and all possible optimisations"""

    def __init__(self, elements):
        self.elements = elements
        self.tree_elems = {elem: Tree(elem) for elem in self.elements}

    def find(self, element):
        """Returns the representent of given element"""
        if element not in self.tree_elems:
            raise KeyError(f"Can't find {element} in UnionFind {self}")

        tree_element = self.tree_elems[element]
        return self.find_tree(tree_element, elem=element).element

    def find_tree(self, tree_element, elem=None):
        """Returns the root parent Tree of given Tree_element"""
        if tree_element.parent is None:
            if elem is not None:
                self.tree_elems[elem] = tree_element
            return tree_element
        tree_element.parent = self.find_tree(tree_element.parent, elem=elem)
        return tree_element.parent

    def union(self, element_1, element_2):
        """Union betwen classes of element_1 and element_2
        Implementation of union optimisation
        """
        element_1_tree = self.find_tree(self.tree_elems[element_1])
        element_2_tree = self.find_tree(self.tree_elems[element_2])
        if element_1_tree != element_2_tree:
            if element_1_tree.rank < element_2_tree.rank:
                element_1_tree.parent = element_2_tree
                self.tree_elems[element_1] = element_2_tree
                self.tree_elems[element_2] = element_2_tree
            else:
                element_2_tree.parent = element_1_tree
                self.tree_elems[element_2] = element_1_tree
                self.tree_elems[element_1] = element_1_tree
                if element_1_tree.rank == element_2_tree.rank:
                    element_1_tree.rank += 1

    def make_set(self, element):
        """Add an singleton with element to the classes"""
        if element not in self.tree_elems:
            self.tree_elems[element] = Tree(element)

    def number_of_classes(self) -> int:
        """
        Returns the number of classes of the union find

        Watchout: UnionFind is a mutable structure, the result may change
        after every `union` call
        """
        return len(
            {self.find_tree(tree_elem) for tree_elem in self.tree_elems.values()}
        )

    def __repr__(self):
        return str(self.tree_elems)


def test():
    """test all the methods"""

    elems = [1, 2, 3, 4]
    union_find = UnionFind(elems)

    assert union_find.number_of_classes() == 4

    union_find.union(1, 3)
    union_find.union(2, 4)

    assert union_find.find(1) == union_find.find(3)
    assert union_find.find(2) == union_find.find(4)
    assert union_find.find(1) != union_find.find(2)
    assert union_find.find(1) != union_find.find(4)

    assert union_find.number_of_classes() == 2

    union_find.union(3, 2)

    assert union_find.number_of_classes() == 1


if __name__ == "__main__":
    test()
