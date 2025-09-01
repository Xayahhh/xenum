from wt3.enumerator.base.node import Node

class InputNode(Node):

    num_children = 0
    num_symbols = 1
    node_type = "input"
    symbol_types = ["table"]
    
    def __init__(self, name: str):
        super().__init__(name=name)
        self.node_type = "input"
        self.num_children = 0
        self.num_symbols = 1

    def inputs(self):
        return []
    
    def outputs(self):
        return self.symbols

    def to_symbolic_sql(self):
        if len(self.symbols) != 1:
            raise ValueError("Input node must have at exactly one symbol.")
        table_symbol = self.symbols[0]
        if table_symbol.symbol_type != "table":
            raise ValueError("Input node's symbol must be a table symbol.")
        return f"(SELECT * FROM {table_symbol.name}) AS {self.name}"
