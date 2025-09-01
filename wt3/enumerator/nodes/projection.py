from wt3.enumerator.base.node import Node

'''
ProjectionNode has a single child and two symbols: 
    a function symbol f 
    a table symbol t.
The SQL representation is:
    SELECT f(t) FROM child_sql AS f

'''

class ProjectionNode(Node):

    num_children = 1
    num_symbols = 2
    node_type = "projection"
    symbol_types = ["func", "attr"]

    def __init__(self, name: str):
        super().__init__(name=name)
        self.node_type = "projection"
        self.num_children = 1
        self.num_symbols = 2
    
    def inputs(self):
        return self.children[0].outputs()
    
    def outputs(self):
        return [self.symbols[0]]

    def to_symbolic_sql(self):
        if len(self.symbols) != 2:
            raise ValueError("Projection node must have exactly two symbols.")
        function_symbol = self.symbols[0]
        table_symbol = self.symbols[1]
        child_sql = self.children[0].to_symbolic_sql()
        return f"(SELECT {function_symbol.name}({table_symbol.name}) FROM {child_sql}) AS {self.name}"