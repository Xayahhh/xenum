from wt3.enumerator.base.node import Node

class LimitNode(Node):

    num_children = 1
    num_symbols = 1
    node_type = "limit"
    symbol_types = ["func"]

    def __init__(self, name: str):
        super().__init__(name=name)
        self.node_type = "limit"
        self.num_children = 1
        self.num_symbols = 1

    def inputs(self):
        return self.children[0].outputs()
    
    def outputs(self):
        return self.children[0].outputs()
    
    def to_symbolic_sql(self):
        if len(self.symbols) != 1:
            raise ValueError("Limit node must have exactly one symbol.")
        function_symbol = self.symbols[0]
        child_sql = self.children[0].to_symbolic_sql()
        return f"(SELECT * FROM {child_sql} LIMIT {function_symbol.name}) AS {self.name}"
