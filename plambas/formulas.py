"""Interpret the scalar MathJSON subset used by monthly SRCLET methods."""
import ast
import math
import operator

Q24 = {
    "id": "q24", "name": "q₂₄", "unit": "L/s/ha", "version": 1,
    "source": "Čadro (2019), 5.1.2.3.2, (37)",
    "latex": r"\frac{10000\cdot D}{86400\cdot d}",
    "expression": ["Divide", ["Multiply", 10000, "D"], ["Multiply", 86400, "d"]],
}

FUNCTIONS = {
    "Add": (2, None, lambda *xs: sum(xs)), "Subtract": (2, 2, operator.sub),
    "Negate": (1, 1, operator.neg), "Multiply": (2, None, lambda *xs: math.prod(xs)),
    "Divide": (2, 2, operator.truediv), "Power": (2, 2, math.pow),
    "Sqrt": (1, 1, math.sqrt), "Root": (2, 2, lambda x, n: math.pow(x, 1/n)),
    "Exp": (1, 1, math.exp), "Ln": (1, 1, math.log), "Log": (1, 2, lambda x, base=10: math.log(x, base)),
    "Sin": (1, 1, math.sin), "Cos": (1, 1, math.cos), "Tan": (1, 1, math.tan),
    "Abs": (1, 1, abs), "Min": (2, None, min), "Max": (2, None, max),
    "Less": (2, 2, operator.lt), "Greater": (2, 2, operator.gt),
    "LessEqual": (2, 2, operator.le), "GreaterEqual": (2, 2, operator.ge),
    "Equal": (2, 2, operator.eq), "NotEqual": (2, 2, operator.ne),
}
CONSTANTS = {"Pi": math.pi, "ExponentialE": math.e, "True": True, "otherwise": True}
ALIASES = {"InvisibleOperator": "Multiply", "Delimiter": "Group", "Set": "Group"}


def walk(node, symbols, *, check=False, depth=0):
    if depth > 64:
        raise ValueError("Formula is too deeply nested.")
    if isinstance(node, dict) and set(node) == {"num"}:
        node = float(node["num"])
    if isinstance(node, (int, float)):
        if not math.isfinite(node):
            raise ValueError("Non-finite number.")
        return float(node)
    if isinstance(node, str):
        if node in CONSTANTS:
            return CONSTANTS[node]
        if node not in symbols:
            raise ValueError(f"Unknown symbol: {node}")
        return 0 if check else symbols[node]
    if not isinstance(node, list) or not node or not isinstance(node[0], str):
        raise ValueError("Incomplete expression.")
    op = ALIASES.get(node[0], node[0])
    args = node[1:]

    def child(arg):
        return walk(arg, symbols, check=check, depth=depth + 1)

    if op == "Group" and len(args) == 1:
        return child(args[0])
    if op == "Which" and len(args) >= 2 and len(args) % 2 == 0:
        for cond, val in zip(args[::2], args[1::2]):
            choice = child(cond)
            if check:
                child(val)
            elif choice:
                return child(val)
        if check:
            return 0
        raise ValueError("No matching case.")
    if op not in FUNCTIONS:
        raise ValueError(f"Unsupported expression: {op}")
    lo, hi, fn = FUNCTIONS[op]
    if len(args) < lo or (hi and len(args) > hi):
        raise ValueError(f"Invalid arguments: {op}")
    values = [child(arg) for arg in args]
    if check:
        return 0
    try:
        value = fn(*values)
        if not math.isfinite(value):
            raise ValueError("Non-finite result.")
        return value
    except (ArithmeticError, ValueError, TypeError) as error:
        raise ValueError(f"{op}: {error}") from error


def symbols_used(expression):
    found = set()
    def collect(node):
        if isinstance(node, str) and node not in CONSTANTS:
            found.add(node)
        elif isinstance(node, list):
            for child in node[1:]:
                collect(child)
    collect(expression)
    return found


def legacy_expression(text):
    """Keep old ASCII expressions editable without executing Python code."""
    ops = {ast.Add: "Add", ast.Sub: "Subtract", ast.Mult: "Multiply", ast.Div: "Divide", ast.Pow: "Power"}
    def convert(node):
        calls = {"min": "Min", "max": "Max", "sqrt": "Sqrt", "exp": "Exp", "abs": "Abs", "log": "Ln"}
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in calls and not node.keywords:
            return [calls[node.func.id], *(convert(arg) for arg in node.args)]
        if isinstance(node, ast.IfExp):
            return ["Which", convert(node.test), convert(node.body), "True", convert(node.orelse)]
        if isinstance(node, ast.Compare) and len(node.ops) == 1:
            relation = {ast.Gt: "Greater", ast.Lt: "Less", ast.GtE: "GreaterEqual", ast.LtE: "LessEqual", ast.Eq: "Equal"}
            if type(node.ops[0]) in relation:
                return [relation[type(node.ops[0])], convert(node.left), convert(node.comparators[0])]
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Constant) and type(node.value) in (float, int):
            return node.value
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return ["Negate", convert(node.operand)]
        if isinstance(node, ast.BinOp) and type(node.op) in ops:
            return [ops[type(node.op)], convert(node.left), convert(node.right)]
        raise ValueError("Unsupported legacy formula.")
    return convert(ast.parse(text.strip().replace("^", "**"), mode="eval").body)
