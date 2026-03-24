"""Debug AST transformation."""

import ast
import operator

SAFE_OPERATORS = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.And: lambda a, b: a and b,
    ast.Or: lambda a, b: a or b,
}

class LogicTransformer(ast.NodeTransformer):
    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name):
            new_node = ast.Subscript(
                value=node.value,
                slice=ast.Index(value=ast.Constant(node.attr)),
                ctx=node.ctx
            )
            return ast.copy_location(new_node, node)
        return node

expr = "0.99 <= low_idle.lambda <= 1.01 and low_idle.co < 0.3 and low_idle.hc < 60"
expr = expr.replace('&&', ' and ').replace('||', ' or ')

# Convert attribute access to subscript so 'lambda' keyword doesn't cause SyntaxError
import re
expr = re.sub(r'([a-zA-Z_]\w*)\.(\w+)', r"\1['\2']", expr)

tree = ast.parse(expr, mode='eval')
print("Original AST:")
print(ast.dump(tree, indent=2))

transformer = LogicTransformer()
tree = transformer.visit(tree)
ast.fix_missing_locations(tree)

print("\nTransformed AST:")
print(ast.dump(tree, indent=2))

# Compile and test
code = compile(tree, '<logic>', 'eval')
context = {
    'low_idle': {'lambda': 1.0, 'co': 0.1, 'hc': 20},
    'calculated_lambda': 1.0,
    'measured_lambda': 1.0
}
result = eval(code, {"__builtins__": {}}, context)
print("\nEvaluation result:", result)
