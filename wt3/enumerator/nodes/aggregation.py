from wt3.enumerator.base.node import Node

class AggregationNode(Node):

    num_children = 1
    num_symbols = 6
    node_type = "aggregation"
    symbol_types = ["func", "attr", "func", "attr", "func", "attr"] # --> Projected, Grouped, Filtered

    def __init__(self, name: str):
        super().__init__(name=name)
        self.node_type = "aggregation"
        self.num_children = 1
        self.num_symbols = 6

    def inputs(self):
        return self.children[0].outputs()
    
    def outputs(self):
        return [self.symbols[0]]
    
    def to_symbolic_sql(self):
        if len(self.symbols) != 6:
            raise ValueError("Aggregation node must have exactly six symbols.")
        
        project_func = self.symbols[0]
        project_attr = self.symbols[1]
        filter_func = self.symbols[4]
        filter_attr = self.symbols[5]
        group_func = self.symbols[2]
        group_attr = self.symbols[3]

        child_sql = self.children[0].to_symbolic_sql()
        
        return (f"(SELECT {project_func.name}({project_attr.name}) FROM {child_sql} "
                f"GROUP BY {group_func.name}({group_attr.name}) "
                f"HAVING {filter_func.name}({filter_attr.name})) AS {self.name}")

