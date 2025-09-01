from wt3.enumerator.base.node import Node

class UnionNode(Node):

    num_children = 2
    num_symbols = 0
    node_type = "union"
    symbol_types = []

    def __init__(self, name: str):
        super().__init__(name=name)
        self.node_type = "union"
        self.num_children = 2
        self.num_symbols = 0

    def inputs(self):
        return self.children[0].outputs() + self.children[1].outputs()
    
    def outputs(self):
        return self.children[0].outputs()

    def to_symbolic_sql(self):
        left_child_sql = self.children[0].to_symbolic_sql()
        right_child_sql = self.children[1].to_symbolic_sql()
        
        return f"({left_child_sql}) UNION ({right_child_sql}) as {self.name}"