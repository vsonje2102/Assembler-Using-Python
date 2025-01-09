from helper.entries import ErrorEntry
class AVLNode:
    def __init__(self, key, data):
        self.key = key  # Unique key for the entry (e.g., Symbol_Name)
        self.data = data  # Associated data object (e.g., SymbolEntry)
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, root, key, data,error_table,flag=1):
        if not root:
            return AVLNode(key, data)

        if key < root.key:
            root.left = self.insert(root.left, key, data,error_table)
        elif key > root.key:
            root.right = self.insert(root.right, key, data,error_table)
        else:
            if flag == 1: 
                error_entry = ErrorEntry(
                Error_no=len(error_table) + 1,
                Error_Message=f"Symbol '{key}' already exists in the symbol table.",
                Address=root.data.Address
                )
                error_table.append(error_entry)
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Balancing the tree
        if balance > 1 and key < root.left.key:
            return self.rotate_right(root)
        if balance < -1 and key > root.right.key:
            return self.rotate_left(root)
        if balance > 1 and key > root.left.key:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        if balance < -1 and key < root.right.key:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def search(self, root, key):
        if not root:
            return None
        if root.key == key:
            return root
        elif key < root.key:
            return self.search(root.left, key)
        else:
            return self.search(root.right,key)

    def in_order(self, root):
        if root:
            self.in_order(root.left)
            print(f"Key {root.key}, Data: {root.data}")
            self.in_order(root.right)
