class Node:

    node_type = "any"

    def __init__(self, name: str):
        self.node_type = "any"
        self.name = name
        self.num_children = 0
        self.num_symbols = 0
        self.children = []
        self.symbols = []
        self.depth = 0

    def add_child(self, child_node):
        if self.children_full():
            raise ValueError("Cannot add more children, node is full.")
        self.children.append(child_node)

    def add_symbol(self, symbol):
        if self.symbols_full():
            raise ValueError("Cannot add more symbols, node is full.")
        self.symbols.append(symbol)
        symbol.node = self

    def children_full(self):
        return len(self.children) >= self.num_children
    
    def symbols_full(self):
        return len(self.symbols) >= self.num_symbols
    
    def sub_symbols(self):
        sub_symbols = []
        for child in self.children:
            sub_symbols.extend(child.sub_symbols())
        return sub_symbols + self.symbols
    
    def sub_nodes(self):
        sub_nodes = []
        for child in self.children:
            sub_nodes.extend(child.sub_nodes())
        return sub_nodes + [self]
    
    def inputs(self):
        raise NotImplementedError("Subclasses should implement this method.")
    
    def outputs(self):
        raise NotImplementedError("Subclasses should implement this method.")
    
    def is_leaf(self):
        return self.num_children == 0
    
    def to_symbolic_sql(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def __repr__(self):
        prefix = "   " * self.depth + "|--"
        for child in self.children:
            child.depth = self.depth + 1
        return f"{prefix}{self.name}(type={self.node_type}, symbols={self.symbols})\n" + \
               "".join([repr(child) for child in self.children])
