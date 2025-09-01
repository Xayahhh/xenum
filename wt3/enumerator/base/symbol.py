
SYMBOL_TYPES = [
    "any",
    "table",
    "attr",
    "func",
    ""
]

class Symbol:

    def __init__(self, name: str, symbol_type: str = "any"):
        if symbol_type not in SYMBOL_TYPES:
            raise ValueError(f"Invalid symbol type: {symbol_type}. Must be one of {SYMBOL_TYPES}.")
        self.name = name
        self.symbol_type = symbol_type
        self.node = None

    def possible_sources(self):
        if self.node is None:
            raise ValueError("Symbol is not associated with any node.")
        if self.symbol_type != "attr":
            raise ValueError("Symbol is not attr.")
        if self.node.node_type == "aggregation" and self == self.node.symbols[5]:
            return self.node.outputs()
        return self.node.inputs()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name