from wt3.enumerator.base.node import Node

class SortNode(Node):

    num_children = 1
    num_symbols = 2
    node_type = "sort"
    symbol_types = ["func", "attr"]

    def __init__(self, name: str):
        super().__init__(name=name)
        self.node_type = "sort"
        self.num_children = 1
        self.num_symbols = 2

    def inputs(self):
        return self.children[0].outputs()
    
    def outputs(self):
        return self.children[0].outputs()
    
    def to_symbolic_sql(self):
        if len(self.symbols) != 2:
            raise ValueError("Sort node must have exactly two symbols.")
        function_symbol = self.symbols[0]
        table_symbol = self.symbols[1]
        child_sql = self.children[0].to_symbolic_sql()
        return f"(SELECT * FROM {child_sql} ORDER BY {function_symbol.name}({table_symbol.name})) AS {self.name}"
