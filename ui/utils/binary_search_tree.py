# pos_sistem/utils/binary_search_tree.py

class ProductNode:
    def __init__(self, product):
        self.product = product
        self.left = None
        self.right = None

class ProductBST:
    def __init__(self):
        self.root = None

    def insert(self, product):
        def _insert(node, product):
            if not node:
                return ProductNode(product)
            if product["name"].lower() < node.product["name"].lower():
                node.left = _insert(node.left, product)
            else:
                node.right = _insert(node.right, product)
            return node

        self.root = _insert(self.root, product)

    def search_by_substring(self, substring):
        results = []
        substring = substring.lower()

        def _traverse(node):
            if not node:
                return
            if substring in node.product["name"].lower():
                results.append(node.product)
            _traverse(node.left)
            _traverse(node.right)

        _traverse(self.root)
        return results
