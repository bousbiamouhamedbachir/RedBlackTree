import tkinter as tk
from tkinter import messagebox
# Ensure this matches your file name. 
# It assumes the class 'Node' is inside 'node.py'
from node import Node  

class RBTreeGUI:
    def __init__(self, root):
        self.root_window = root
        self.root_window.title("Red-Black Tree Visualizer")
        self.root_window.geometry("1200x700")

        # Create the initial empty node (Sentinel logic handling)
        self.tree_root = Node(key=None, color="black")

        # Visualization configurations
        self.node_radius = 18
        self.y_spacing = 60

        self._setup_ui()

    def _setup_ui(self):
        # --- Main Container ---
        main_container = tk.Frame(self.root_window)
        main_container.pack(fill=tk.BOTH, expand=True)

        # --- Canvas Area (Left) ---
        canvas_wrapper = tk.Frame(main_container, bd=2, relief=tk.SUNKEN)
        canvas_wrapper.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.v_scroll = tk.Scrollbar(canvas_wrapper, orient=tk.VERTICAL)
        self.h_scroll = tk.Scrollbar(canvas_wrapper, orient=tk.HORIZONTAL)
        
        self.canvas = tk.Canvas(canvas_wrapper, bg="#f5f5f5", 
                                xscrollcommand=self.h_scroll.set, 
                                yscrollcommand=self.v_scroll.set)
        
        self.v_scroll.config(command=self.canvas.yview)
        self.h_scroll.config(command=self.canvas.xview)

        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # --- Control Panel (Right) ---
        control_frame = tk.Frame(main_container, width=280, bg="#e0e0e0", padx=15, pady=15)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        control_frame.pack_propagate(False)

        # Input
        tk.Label(control_frame, text="Red-Black Tree Operations", bg="#e0e0e0", font=("Arial", 12, "bold")).pack(pady=(0, 20))
        tk.Label(control_frame, text="Integer Value:", bg="#e0e0e0").pack(anchor="w")
        
        self.entry_val = tk.Entry(control_frame, font=("Arial", 12))
        self.entry_val.pack(fill=tk.X, pady=5)
        self.entry_val.bind('<Return>', lambda e: self.insert_node())

        # Buttons
        self._make_btn(control_frame, "Insert", self.insert_node, "green")
        self._make_btn(control_frame, "Delete", self.delete_node, "red")
        self._make_btn(control_frame, "Search", self.search_node, "blue")
        
        tk.Frame(control_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=20)
        
        self._make_btn(control_frame, "Clear Tree", self.clear_tree, "gray")
        self._make_btn(control_frame, "Center View", self.center_view, "black")

        # --- Status Bar ---
        self.status_var = tk.StringVar()
        self.status_var.set("Ready. Tree is empty.")
        status_bar = tk.Label(self.root_window, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor="w", bg="#dcdcdc")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _make_btn(self, parent, text, cmd, color):
        btn = tk.Button(parent, text=text, command=cmd, bg="white", fg=color, font=("Arial", 10, "bold"))
        btn.pack(fill=tk.X, pady=5)

    # ------------------ Logic & Updates ------------------

    def get_input(self):
        try:
            val = self.entry_val.get()
            if not val: return None
            return int(val)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid integer.")
            return None

    def _update_root(self):
        """
        CRITICAL FIX: logic in node.py rotates nodes, changing the hierarchy.
        We must walk UP from the current self.tree_root to find the actual 
        top of the tree (parent is None).
        """
        if self.tree_root is None: return

        # If the current tracked root has a parent, it's no longer the root.
        # Walk up until we find the node with no parent.
        while self.tree_root.parent is not None:
            self.tree_root = self.tree_root.parent
        
        # Note: In node.py, Empty nodes have key=None. Real nodes have key=Integer.

    def insert_node(self):
        val = self.get_input()
        if val is not None:
            # 1. Perform Insert
            self.tree_root.insert(val)
            
            # 2. Update Root Reference (Rotations might have changed it)
            self._update_root()
            
            # 3. GUI Feedback
            self.entry_val.delete(0, tk.END)
            self.status_var.set(f"Inserted: {val}")
            self.draw_tree()

    def delete_node(self):
        val = self.get_input()
        if val is not None:
            # 1. Perform Delete
            # Your delete method returns a node reference, but we must also ensure global root tracking
            self.tree_root.delete(val)
            
            # 2. Update Root Reference
            self._update_root()

            # 3. GUI Feedback
            self.entry_val.delete(0, tk.END)
            self.status_var.set(f"Deleted: {val}")
            self.draw_tree()

    def search_node(self):
        val = self.get_input()
        if val is not None:
            self._update_root() # Just in case
            res = self.tree_root.search(val)
            if res != Node.NIL and res.key is not None:
                self.status_var.set(f"Found {val} [Color: {res.color}]")
                self.draw_tree(highlight_key=val)
            else:
                self.status_var.set(f"Node {val} not found.")

    def clear_tree(self):
        self.tree_root = Node(key=None, color="black")
        self.draw_tree()
        self.status_var.set("Tree cleared.")

    # ------------------ Drawing Logic ------------------

    def draw_tree(self, highlight_key=None):
        self.canvas.delete("all")
        
        # Handle Empty Tree
        if self.tree_root.key is None:
            self.canvas.create_text(400, 100, text="Tree is Empty", fill="gray", font=("Arial", 16))
            return

        # 1. Calculate Positions (Smart Layout to avoid overlaps)
        # We start X very large to allow scrolling
        start_x = 2000
        start_y = 50
        positions = {}
        
        self._calculate_positions(self.tree_root, start_x, start_y, 0, positions)

        # 2. Draw Lines (Connections)
        for node, (x, y) in positions.items():
            if node.left != Node.NIL and node.left.key is not None:
                lx, ly = positions[node.left]
                self.canvas.create_line(x, y, lx, ly, width=2, fill="#555")
            if node.right != Node.NIL and node.right.key is not None:
                rx, ry = positions[node.right]
                self.canvas.create_line(x, y, rx, ry, width=2, fill="#555")

        # 3. Draw Nodes
        for node, (x, y) in positions.items():
            self._draw_circle(x, y, node, highlight=(node.key == highlight_key))

        # 4. Update Scroll Region
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def center_view(self):
        self.canvas.xview_moveto(0.5)
        self.canvas.yview_moveto(0)

    def _calculate_positions(self, node, x, y, level, positions):
        """ Recursively determine coordinates """
        # Safety check for NIL or broken nodes
        if node is None or node == Node.NIL or node.key is None:
            return

        positions[node] = (x, y)

        # Calculate dynamic width based on depth
        # Deeper levels have smaller gaps, but we set a minimum of 35px
        width = max(35, 400 // (2 ** level))

        self._calculate_positions(node.left, x - width, y + self.y_spacing, level + 1, positions)
        self._calculate_positions(node.right, x + width, y + self.y_spacing, level + 1, positions)

    def _draw_circle(self, x, y, node, highlight=False):
        r = self.node_radius
        bg_color = "black" if node.color == "black" else "#e74c3c" # Red
        outline = "yellow" if highlight else "black"
        width = 4 if highlight else 1

        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=bg_color, outline=outline, width=width)
        self.canvas.create_text(x, y, text=str(node.key), fill="white", font=("Arial", 10, "bold"))

if __name__ == "__main__":
    root = tk.Tk()
    app = RBTreeGUI(root)
    root.mainloop()
