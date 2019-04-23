class BinaryTreeSet:
    """
    An iterative Binary Tree Set.
    Should be fast.
    Order can not change while in the BinaryTreeSet
    """

    def __init__(self):
        # items less than, item, items greater than
        self.tree = []
        self.length = 0

    def add(self, item):
        # O(log n) average
        self.length += 1
        tree = self.tree
        while len(tree) != 0:
            if item < tree[1]:
                tree = tree[0]
            else:
                tree = tree[2]
        tree.append([])
        tree.append(item)
        tree.append([])

    def contains(self, item):
        # O(log n) average
        tree = self.tree
        while len(tree) != 0 and tree[1] is not item:
            if item < tree[1]:
                tree = tree[0]
            else:
                tree = tree[2]
        return len(tree) != 0

    def remove(self, item):
        # O(log n) average
        tree = self.tree
        parent = None
        index = None
        while len(tree) != 0 and tree[1] is not item:
            parent = tree
            if item < tree[1]:
                index = 0
                tree = tree[0]
            else:
                index = 2
                tree = tree[2]

        if len(tree) == 0:
            raise ValueError("This tree does not contain the given item")

        self.length -= 1

        is_leaf = lambda tree_: len(tree_) != 0 and len(tree_[0]) == 0 and len(tree_[2]) == 0

        if is_leaf(tree):  # is leaf node
            if parent is not None:  # not removing from root node
                parent[index] = []
            else:
                self.tree.clear()
        elif is_leaf(tree[0]) and not is_leaf(tree[2]):  # left child is leaf node
            tree[1] = tree[0][1]
            tree[0].clear()
        elif not is_leaf(tree[0]) and is_leaf(tree[2]):  # right child is leaf node
            tree[1] = tree[2][1]
            tree[2].clear()
        else:
            raise NotImplementedError("only leaf nodes and items with one leaf node can be removed at the moment")

    def __len__(self):
        return self.length

    def __str__(self):
        string = "["
        for i in self:
            string += str(i) + ", "
        string = "]"
        return string

    def __iter__(self):
        self.stack = []
        self.current = self.tree
        return self

    def __next__(self):
        while len(self.stack) != 0 or len(self.current) != 0:
            if len(self.current) != 0:
                self.stack.append(self.current)
                self.current = self.current[0]
            else:
                self.current = self.stack.pop(-1)
                to_return = self.current[1]
                self.current = self.current[2]
                return to_return
        raise StopIteration


class BTree:
    """
    Even better than Binary search tree
    """
    def __init__(self):
        raise NotImplementedError()
