import ast
import math
import operator
from typing import Dict, Any, Union

# Safe AST Math Evaluator (Zero eval() vulnerability)
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.BitXor: operator.xor,
    ast.BitAnd: operator.and_,
    ast.BitOr: operator.or_,
    ast.LShift: operator.lshift,
    ast.RShift: operator.rshift,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

SAFE_FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log2": math.log2,
    "log10": math.log10,
    "ceil": math.ceil,
    "floor": math.floor,
    "abs": abs,
    "pi": math.pi,
    "e": math.e,
}


def safe_eval(node):
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.BinOp):
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            return SAFE_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported operator: {op_type}")
    elif isinstance(node, ast.UnaryOp):
        operand = safe_eval(node.operand)
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            return SAFE_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type}")
    elif isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in SAFE_FUNCTIONS and callable(SAFE_FUNCTIONS[func_name]):
                args = [safe_eval(arg) for arg in node.args]
                return SAFE_FUNCTIONS[func_name](*args)
            raise ValueError(f"Unsupported function call: {func_name}")
        raise ValueError(f"Unsupported function call type: {type(node.func)}")
    elif isinstance(node, ast.Name):
        if node.id in SAFE_FUNCTIONS:
            return SAFE_FUNCTIONS[node.id]
        raise ValueError(f"Unsupported variable: {node.id}")
    raise ValueError(f"Invalid math expression AST node: {type(node)}")


def calculate_expression(expr_str: str) -> Dict[str, Any]:
    expr_str = expr_str.strip()
    try:
        parsed = ast.parse(expr_str, mode="eval")
        result = safe_eval(parsed.body)
        print(f"🧮 \033[1;36mAERO CALCULATOR\033[0m")
        print("═" * 45)
        print(f" • Expression: \033[1;33m{expr_str}\033[0m")
        print(f" • Result:     \033[1;32m{result}\033[0m")
        if isinstance(result, (int, float)) and result > 1024:
            print(f" • In KB:      {result / 1024:.2f} KB")
            print(f" • In MB:      {result / (1024**2):.2f} MB")
            print(f" • In GB:      {result / (1024**3):.4f} GB")
        print()
        return {"expression": expr_str, "result": result, "error": None}
    except Exception as e:
        print(f"❌ Calculation Error: {e}")
        return {"expression": expr_str, "result": None, "error": str(e)}
