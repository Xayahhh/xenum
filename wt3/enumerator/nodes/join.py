from wt3.enumerator.base.node import Node

class JoinNode(Node):

    num_children = 2
    num_symbols = 2
    node_type = "join"
    symbol_types = ["func", "attr"]

    def __init__(self, name: str):
        super().__init__(name=name)
        self.node_type = "join"
        self.num_children = 2
        self.num_symbols = 2

    def inputs(self):
        inputs = []
        for child in self.children:
            inputs.extend(child.outputs())
        return inputs
    
    def outputs(self):
        return self.inputs()

    def to_symbolic_sql(self):
        if len(self.symbols) != 2:
            raise ValueError("Join node must have exactly two symbols.")
        function_symbol = self.symbols[0]
        table_symbol = self.symbols[1]
        left = self.children[0].to_symbolic_sql()
        right = self.children[1].to_symbolic_sql()
        return f"(SELECT * FROM {left} JOIN {right} ON {function_symbol.name}({table_symbol.name})) AS {self.name}"