from wt3.enumerator.base.node import Node
from wt3.enumerator.base.symbol import Symbol
from wt3.enumerator.base.template import Template
from wt3.enumerator.helpers import NameGenerator
from wt3.enumerator.config import *

class TemplateEnumerator:

    def __init__(self, max_operators: int, name_generator: NameGenerator = None):
        self.max_operators = max_operators
        # self.templates = []
        if name_generator is None:
            self.init_name_generator = NameGenerator()
        else:
            self.init_name_generator = name_generator
        self.name_generator = None
    def enumerate(self):
        for cls in NODE_CLASSES:
            self.name_generator = self.init_name_generator.copy()
            if cls.num_children > self.max_operators:
                continue
            n: Node = cls(self.name_generator.generate_name(cls.node_type))
            for i in cls.symbol_types:
                n.add_symbol(Symbol(self.name_generator.generate_name(i[0]), i))
            if n.num_children == 0:
                template = Template(root=n)
                yield template
            elif n.num_children == 1:
                child_enumerator = TemplateEnumerator(self.max_operators - 1, self.name_generator)
                for child_template in child_enumerator.enumerate():
                    n.add_child(child_template.root)
                    template = Template(root=n)
                    self.name_generator = child_enumerator.name_generator
                    yield template
                    n.children.clear()  # Reset children for next iteration
            elif n.num_children == 2:
                saved_name_generator = self.name_generator.copy()
                for i in range(1, self.max_operators - 1):
                    child_enumerator1 = TemplateEnumerator(i, saved_name_generator)
                    for child_template1 in child_enumerator1.enumerate():
                        child_enumerator2 = TemplateEnumerator(self.max_operators - 1 - i, child_enumerator1.name_generator)
                        for child_template2 in child_enumerator2.enumerate():
                            n.add_child(child_template1.root)
                            n.add_child(child_template2.root)
                            template = Template(root=n)
                            self.name_generator = child_enumerator2.name_generator
                            yield template
                            n.children.clear()  # Reset children for next iteration