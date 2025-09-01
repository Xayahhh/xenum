from wt3.enumerator.base.node import Node

'''
SimpleProjectionNode has a single child and two symbols: 
    a function symbol f 
    a table symbol t.
The SQL representation is:
    SELECT t FROM child_sql AS f

'''

class SimpleProjectionNode(Node):

    num_children = 1
    num_symbols = 1
    node_type = "projection"
    symbol_types = ["attr"]

    def __init__(self, name: str):
        super().__init__(name=name)
        self.node_type = "projection"
        self.num_children = 1
        self.num_symbols = 1
    
    def inputs(self):
        return self.children[0].outputs()
    
    def outputs(self):
        return [self.symbols[0]]

    def to_symbolic_sql(self):
        if len(self.symbols) != 1:
            raise ValueError("SimpleProjection node must have exactly one symbols.")
        table_symbol = self.symbols[0]
        child_sql = self.children[0].to_symbolic_sql()
        return f"(SELECT {table_symbol.name} FROM {child_sql}) AS {self.name}"