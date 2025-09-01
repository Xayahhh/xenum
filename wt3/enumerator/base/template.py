from wt3.enumerator.base.node import Node

class Template():

    root: Node
    symbols: list

    def __init__(self, root = None):
        self.root = root
        if root is not None:
            self.symbols = root.sub_symbols()
            self.nodes = root.sub_nodes()

    def to_symbolic_sql(self):
        if self.root is None:
            return ""
        return self.root.to_symbolic_sql()
    
    def nodes_by_type(self, node_type: str = "any"):
        return [node for node in self.nodes if node.node_type == node_type or node_type == "any" or node.node_type == "any"]

    def symbols_by_type(self, symbol_type: str = "any"):
        return [symbol for symbol in self.symbols if symbol.symbol_type == symbol_type or symbol_type == "any" or symbol.symbol_type == "any"]

    def __repr__(self):
        return f"Template(root=\n{self.root})"