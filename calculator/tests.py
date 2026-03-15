import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

try:
    from calculator import main as calc_main
    from calculator.pkg import render as render_utils
except ModuleNotFoundError:
    import main as calc_main
    from pkg import render as render_utils


class TestParseExpression(unittest.TestCase):
    def test_parse_addition_expression(self):
        left, op, right = calc_main.parse_expression("10 + 5")
        self.assertEqual(left, 10.0)
        self.assertEqual(op, "+")
        self.assertEqual(right, 5.0)

    def test_parse_invalid_format_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            calc_main.parse_expression("10 +")

        self.assertIn("Expression must be in the format", str(context.exception))

    def test_parse_unsupported_operator_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            calc_main.parse_expression("10 ^ 5")

        self.assertIn("Unsupported operator", str(context.exception))

    def test_parse_invalid_number_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            calc_main.parse_expression("abc + 5")

        self.assertIn("Both operands must be valid numbers", str(context.exception))


class TestCalculate(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(calc_main.calculate(10, "+", 5), 15)

    def test_subtraction(self):
        self.assertEqual(calc_main.calculate(10, "-", 5), 5)

    def test_multiplication(self):
        self.assertEqual(calc_main.calculate(10, "*", 5), 50)

    def test_division(self):
        self.assertEqual(calc_main.calculate(10, "/", 5), 2)

    def test_modulo(self):
        self.assertEqual(calc_main.calculate(10, "%", 3), 1)

    def test_division_by_zero_raises(self):
        with self.assertRaises(ZeroDivisionError) as context:
            calc_main.calculate(10, "/", 0)

        self.assertIn("Division by zero", str(context.exception))

    def test_modulo_by_zero_raises(self):
        with self.assertRaises(ZeroDivisionError) as context:
            calc_main.calculate(10, "%", 0)

        self.assertIn("Modulo by zero", str(context.exception))


class TestMainFormatAlias(unittest.TestCase):
    def test_format_integer_result(self):
        self.assertEqual(calc_main.format_result(5.0), "5")

    def test_format_float_result(self):
        self.assertEqual(calc_main.format_result(2.5), "2.5")


class TestRenderModule(unittest.TestCase):
    def test_render_format_result_integer(self):
        self.assertEqual(render_utils.format_result(9.0), "9")

    def test_render_format_result_float(self):
        self.assertEqual(render_utils.format_result(9.25), "9.25")

    def test_render_format_error(self):
        self.assertEqual(
            render_utils.format_error("Something went wrong"),
            "Error: Something went wrong",
        )

    def test_render_format_usage_contains_usage(self):
        usage = render_utils.format_usage()
        self.assertIn('Usage: python main.py "<expression>"', usage)

    def test_render_format_usage_contains_example(self):
        usage = render_utils.format_usage()
        self.assertIn('Example: python main.py "10 + 5"', usage)


class TestMainFunction(unittest.TestCase):
    def run_main_with_args(self, args):
        output = io.StringIO()

        with patch("sys.argv", args):
            with redirect_stdout(output):
                with self.assertRaises(SystemExit) as context:
                    calc_main.main()

        return context.exception.code, output.getvalue().strip()

    def test_main_with_valid_expression(self):
        output = io.StringIO()

        with patch("sys.argv", ["main.py", "10 + 5"]):
            with redirect_stdout(output):
                calc_main.main()

        self.assertEqual(output.getvalue().strip(), "15")

    def test_main_with_missing_argument(self):
        exit_code, printed = self.run_main_with_args(["main.py"])

        self.assertEqual(exit_code, 1)
        self.assertIn('Usage: python main.py "<expression>"', printed)
        self.assertIn('Example: python main.py "10 + 5"', printed)

    def test_main_with_invalid_expression(self):
        exit_code, printed = self.run_main_with_args(["main.py", "10 ^ 5"])

        self.assertEqual(exit_code, 1)
        self.assertIn("Error: Unsupported operator", printed)

    def test_main_with_division_by_zero(self):
        exit_code, printed = self.run_main_with_args(["main.py", "10 / 0"])

        self.assertEqual(exit_code, 1)
        self.assertIn("Error: Division by zero is not allowed.", printed)


if __name__ == "__main__":
    unittest.main()