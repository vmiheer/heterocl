# ===----------------------------------------------------------------------=== #
#
# Copyright 2021-2022 The HCL-MLIR Authors.
#
# ===----------------------------------------------------------------------=== #
from ir import intermediate as itmd
from type_rules import *

class TypeInfer(object):
    """A type inference engine for HeteroCL programs.
    """
    def __init__(self):
        self._rules = []
        self._rules.append(add_sub_rule())
        # ...
        self.build_rule_dict()

    def build_rule_dict(self):
        """Build a dictionary of rules, where the key is the operation type
        """
        self._rule_dict = dict()
        for type_rule in self._rules:
            if not isinstance(type_rule, TypeRule):
                raise TypeError(f"type_rule must be a TypeRule, not {type(type_rule)}")
            for op_type in type_rule.OpClass:
                self._rule_dict[op_type] = type_rule

    def infer(self, expr):
        """Infer the type of an expression
        """
        if isinstance(expr, itmd.AddOp):
            self.infer_add(expr)


    def infer_add(self, expr):
        """Infer the type of an add operation
        """
        lhs_type = self.infer(expr.lhs)    
        rhs_type = self.infer(expr.rhs)
        # find the rule set based on the operation type
        if type(expr) not in self._rule_dict:
            raise APIError(f"Typing rules not defined for operation type: {type(expr)}")
        type_rule = self._rule_dict[type(expr)]
        itypes = [lhs_type, rhs_type]
        res_type = type_rule(itypes)
        return res_type