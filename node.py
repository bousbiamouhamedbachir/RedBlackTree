class Node:
    NIL = None  # Singleton NIL node

    def __init__(self, key=None, color="red", parent=None, left=None, right=None):
        self.key = key
        self.color = color
        self.parent = parent
        self.left = left if left else Node.NIL
        self.right = right if right else Node.NIL

    def __repr__(self):
        return f"{self.key}({self.color})"

    # ---------------- Rotations ----------------
    def left_rotate(self):
        y = self.right
        if y is None or y == Node.NIL:
            return None
        self.right = y.left
        if y.left != Node.NIL:
            y.left.parent = self
        y.parent = self.parent
        if self.parent:
            if self == self.parent.left:
                self.parent.left = y
            else:
                self.parent.right = y
        y.left = self
        self.parent = y
        return y

    def right_rotate(self):
        x = self.left
        if x is None or x == Node.NIL:
            return None
        self.left = x.right
        if x.right != Node.NIL:
            x.right.parent = self
        x.parent = self.parent
        if self.parent:
            if self == self.parent.left:
                self.parent.left = x
            else:
                self.parent.right = x
        x.right = self
        self.parent = x
        return x

    # ---------------- BST Insertion ----------------
    def insert(self, key):
        if self.key is None:
            self.key = key
            self.color = "black"
            self.left = Node.NIL
            self.right = Node.NIL
            self.parent = None
            return self
        if key < self.key:
            if self.left == Node.NIL:
                self.left = Node(key, parent=self)
                self.left.fix_insert()
                return self.left
            else:
                return self.left.insert(key)
        elif key > self.key:
            if self.right == Node.NIL:
                self.right = Node(key, parent=self)
                self.right.fix_insert()
                return self.right
            else:
                return self.right.insert(key)
        else:
            return None  # Duplicate

    def fix_insert(self):
        k = self
        while k.parent and k.parent.color == "red":
            if k.parent == k.parent.parent.left:
                u = k.parent.parent.right
                if u and u.color == "red":
                    k.parent.color = "black"
                    u.color = "black"
                    k.parent.parent.color = "red"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        k = k.left_rotate()
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    k.parent.parent.right_rotate()
            else:
                u = k.parent.parent.left
                if u and u.color == "red":
                    k.parent.color = "black"
                    u.color = "black"
                    k.parent.parent.color = "red"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        k = k.right_rotate()
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    k.parent.parent.left_rotate()
        # Ensure root black
        root = k
        while root.parent:
            root = root.parent
        root.color = "black"

    # ---------------- BST Search ----------------
    def search(self, key):
        if self == Node.NIL or self.key == key:
            return self
        if key < self.key:
            return self.left.search(key)
        else:
            return self.right.search(key)

    # ---------------- Minimum ----------------
    def minimum(self):
        node = self
        while node.left != Node.NIL:
            node = node.left
        return node

    # ---------------- Transplant ----------------
    def transplant(self, u, v):
        if u.parent is None:
            pass
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    # ---------------- Deletion ----------------
    def delete(self, key):
        z = self.search(key)
        if z == Node.NIL:
            return self
        y = z
        y_original_color = y.color
        if z.left == Node.NIL:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == Node.NIL:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = z.right.minimum()
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                if x:
                    x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == "black" and x:
            self.fix_delete(x)

        # Return current root
        r = self
        while r.parent:
            r = r.parent
        return r

    def fix_delete(self, x):
        while x != self and x.color == "black":
            if x == x.parent.left:
                w = x.parent.right
                if w.color == "red":
                    w.color = "black"
                    x.parent.color = "red"
                    x.parent.left_rotate()
                    w = x.parent.right
                if w.left.color == "black" and w.right.color == "black":
                    w.color = "red"
                    x = x.parent
                else:
                    if w.right.color == "black":
                        w.left.color = "black"
                        w.color = "red"
                        w.right_rotate()
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = "black"
                    w.right.color = "black"
                    x.parent.left_rotate()
                    x = self
            else:
                w = x.parent.left
                if w.color == "red":
                    w.color = "black"
                    x.parent.color = "red"
                    x.parent.right_rotate()
                    w = x.parent.left
                if w.left.color == "black" and w.right.color == "black":
                    w.color = "red"
                    x = x.parent
                else:
                    if w.left.color == "black":
                        w.right.color = "black"
                        w.color = "red"
                        w.left_rotate()
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = "black"
                    w.left.color = "black"
                    x.parent.right_rotate()
                    x = self
        if x:
            x.color = "black"

    # ---------------- In-order ----------------
    def inorder(self):
        if self == Node.NIL or self.key is None:
            return
        self.left.inorder()
        print(f"{self.key}({self.color})", end=" ")
        self.right.inorder()


# Initialize NIL node
Node.NIL = Node(key=None, color="black")
Node.NIL.left = Node.NIL
Node.NIL.right = Node.NIL
