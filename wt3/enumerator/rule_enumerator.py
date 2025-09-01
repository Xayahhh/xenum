from wt3.enumerator.template_enumerator import TemplateEnumerator
from wt3.enumerator.helpers import NameGenerator, partition_list
from wt3.enumerator.base.rule import Rule
from wt3.enumerator.config import MAX_OPERATORS
from wt3.verifier.sql_verifier import SQLVerifier

class RuleEnumerator:

    def __init__(self, max_operators: int = MAX_OPERATORS):
        self.max_operators = max_operators
        self.name_generator = NameGenerator()
        self.verifier = SQLVerifier()

    def enumerate(self):
        tenum1 = TemplateEnumerator(self.max_operators)
        for template1 in tenum1.enumerate():
            tenum2 = TemplateEnumerator(self.max_operators, tenum1.name_generator)
            for template2 in tenum2.enumerate():
                last_result: bool = None
                constraint_enumerator = self.enumerate_constraints(template1, template2)
                while True:
                    try:
                        constraints = constraint_enumerator.send(last_result)
                    except StopIteration:
                        break
                    if not constraints:
                        continue
                    rule = Rule(
                        name=self.name_generator.generate_name("rule"),
                        template1=template1,
                        template2=template2,
                        constraints=constraints
                    )
                    print(f"Enumerated rule: {rule}")
                    last_result = self.verifier.verify(*rule.to_concrete_sql_pairs())
                    if last_result:
                        yield rule

    def enumerate_table_constraints(self, template1, template2):
        t1_table_symbols = template1.symbols_by_type("table")
        t2_table_symbols = template2.symbols_by_type("table")
        
        for ctable_num in range(1, len(t1_table_symbols) + 1):
            can_eq = False
            concrete_tables = t1_table_symbols[:ctable_num]
            for t1_partition in partition_list(t1_table_symbols, ctable_num):
                for t2_partition in partition_list(t2_table_symbols, ctable_num):
                    concrete_table_mapping = {}
                    for i, part in enumerate(t1_partition):
                        for symbol in part:
                            concrete_table_mapping[symbol] = concrete_tables[i]
                    for i, part in enumerate(t2_partition):
                        for symbol in part:
                            concrete_table_mapping[symbol] = concrete_tables[i]

                    cur_can_eq = yield [f"TableEq({v},{k})" for k, v in concrete_table_mapping.items() if v != k]
                    if cur_can_eq:
                        can_eq = True
            if not can_eq:
                break

    def enumerate_attr_constraints(self, template1, template2):
        t1_attr_symbols = template1.symbols_by_type("attr")
        t2_attr_symbols = template2.symbols_by_type("attr")
        
        attr_num = len(t1_attr_symbols)
        for t1_partition in partition_list(t1_attr_symbols, attr_num):
            for t2_partition in partition_list(t2_attr_symbols, attr_num):
                attr_mapping = {}
                for i, part in enumerate(t1_partition):
                    for symbol in part:
                        attr_mapping[symbol] = t1_attr_symbols[i]
                for i, part in enumerate(t2_partition):
                    for symbol in part:
                        attr_mapping[symbol] = t1_attr_symbols[i]

                cur_can_eq = yield [f"AttrEq({v},{k})" for k, v in attr_mapping.items() if v != k]


    def enumerate_function_constraints(self, template1, template2):
        t1_func_symbols = template1.symbols_by_type("func")
        t2_func_symbols = template2.symbols_by_type("func")
        
        func_num = len(t1_func_symbols)
        for t1_partition in partition_list(t1_func_symbols, func_num):
            for t2_partition in partition_list(t2_func_symbols, func_num):
                func_mapping = {}
                for i, part in enumerate(t1_partition):
                    for symbol in part:
                        func_mapping[symbol] = t1_func_symbols[i]
                for i, part in enumerate(t2_partition):
                    for symbol in part:
                        func_mapping[symbol] = t1_func_symbols[i]

                cur_can_eq = yield [f"FuncEq({v},{k})" for k, v in func_mapping.items() if v != k]

    def enumerate_ic_constraints(self, template1, template2):
        yield []

    def enumerate_constraints(self, template1, template2):
        table_constraints_enumerator = self.enumerate_table_constraints(template1, template2)
        last_table_result = None
        # enumerate possible table constraints
        while True:
            try:
                table_constraints = table_constraints_enumerator.send(last_table_result)
            except StopIteration:
                break
            
            attr_constraints_enumerator = self.enumerate_attr_constraints(template1, template2)
            last_attr_result = None
            # enumerate attr constraints
            while True:
                try:
                    attr_constraints = attr_constraints_enumerator.send(last_attr_result)
                except StopIteration:
                    break
            
                # enumerate possible IC constraints
                ic_constraints_enumerator = self.enumerate_ic_constraints(template1, template2)
                last_ic_result = None
                while True:
                    try:
                        ic_constraints = ic_constraints_enumerator.send(last_ic_result)
                    except StopIteration:
                        break

                    # enumerate possible function constraints
                    function_constraints_enumerator = self.enumerate_function_constraints(template1, template2)
                    last_function_result = None

                    while True:
                        try:
                            function_constraints = function_constraints_enumerator.send(last_function_result)
                        except StopIteration:
                            break
                        last_function_result = yield table_constraints + attr_constraints + ic_constraints + function_constraints
                        if last_function_result:
                            last_ic_result = True
                    
                    if last_ic_result:
                        last_attr_result = True

                if last_attr_result:
                    last_table_result = True
        