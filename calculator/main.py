import sys

try:
    from .pkg import calculator as calculator_service
    from .pkg import render as render_service
except ImportError:
    from pkg import calculator as calculator_service
    from pkg import render as render_service


# TODO: fix below more elegantly
# Re-export these so existing tests still pass.
parse_expression = calculator_service.parse_expression
calculate = calculator_service.calculate
format_result = render_service.format_result


def main() -> None:
    if len(sys.argv) != 2:
        print(render_service.format_usage())
        sys.exit(1)

    expression = sys.argv[1]

    try:
        left, op, right = calculator_service.parse_expression(expression)
        result = calculator_service.calculate(left, op, right)
        print(render_service.format_result(result))
    except Exception as exc:
        print(render_service.format_error(str(exc)))
        sys.exit(1)


if __name__ == "__main__":
    main()