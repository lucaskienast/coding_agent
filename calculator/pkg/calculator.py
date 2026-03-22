import operator


OPERATIONS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "%": operator.mod,
}


def parse_expression(expression: str) -> tuple[float, str, float]:
    parts = expression.strip().split()

    if len(parts) != 3:
        raise ValueError(
            'Expression must be in the format: "<number> <operator> <number>"'
        )

    left_str, op, right_str = parts

    if op not in OPERATIONS:
        raise ValueError(
            f"Unsupported operator: {op}. Supported operators: {', '.join(OPERATIONS.keys())}"
        )

    try:
        left = float(left_str)
        right = float(right_str)
    except ValueError as exc:
        raise ValueError("Both operands must be valid numbers.") from exc

    return left, op, right


def calculate(left: float, op: str, right: float) -> float:
    if op == "/" and right == 0:
        raise ZeroDivisionError("Division by zero is not allowed.")

    if op == "%" and right == 0:
        raise ZeroDivisionError("Modulo by zero is not allowed.")

    return OPERATIONS[op](left, right)
