from wt3.enumerator.base.template import Template

class Rule:
    
    def __init__(self, name: str, template1: Template, template2: Template, constraints: list):
        self.name = name
        self.template1 = template1
        self.template2 = template2
        self.sql1 = template1.to_symbolic_sql()
        self.sql2 = template2.to_symbolic_sql()
        self.constraints = constraints

    def to_concrete_sql_pairs(self):
        return (self.sql1, self.sql2, "")

    def __repr__(self):
        return f"\n=======Rule=======\nname={self.name}, \ntemplate1={self.template1}, \ntemplate2={self.template2}, \nconstraints={self.constraints}\n=================="