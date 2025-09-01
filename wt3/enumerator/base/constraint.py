
class Constraint:
    def __init__(self, cons_type: str):
        self.cons_type = cons_type
        self.symbols = []

    def __repr__(self):
        return f"Constraint(cons_type={self.cons_type}, symbols={self.symbols})"