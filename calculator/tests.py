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
        # We need to adapt the test because format_result now returns a box
        result = calc_main.format_result(5.0)
        self.assertIn("5", result)
        self.assertIn("+", result)

    def test_format_float_result(self):
        result = calc_main.format_result(2.5)
        self.assertIn("2.5", result)
        self.assertIn("+", result)


class TestRenderModule(unittest.TestCase):
    def test_render_format_result_integer(self):
        result = render_utils.format_result(9.0)
        self.assertIn("9", result)
        self.assertIn("+", result)

    def test_render_format_result_float(self):
        result = render_utils.format_result(9.25)
        self.assertIn("9.25", result)
        self.assertIn("+", result)

    def test_render_format_error(self):
        result = render_utils.format_error("Something went wrong")
        self.assertIn("Error: Something went wrong", result)
        self.assertIn("⚠", result)
        self.assertIn("+", result)

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

        self.assertIn("15", output.getvalue().strip())
        self.assertIn("+", output.getvalue().strip())

    def test_main_with_missing_argument(self):
        exit_code, printed = self.run_main_with_args(["main.py"])

        self.assertEqual(exit_code, 1)
        self.assertIn('Usage: python main.py "<expression>"', printed)
        self.assertIn('Example: python main.py "10 + 5"', printed)

    def test_main_with_invalid_expression(self):
        exit_code, printed = self.run_main_with_args(["main.py", "10 ^ 5"])

        self.assertEqual(exit_code, 1)
        self.assertIn("Error:", printed)
        self.assertIn("Unsupported operator", printed)

    def test_main_with_division_by_zero(self):
        exit_code, printed = self.run_main_with_args(["main.py", "10 / 0"])

        self.assertEqual(exit_code, 1)
        self.assertIn("Error:", printed)
        self.assertIn("Division by zero", printed)


if __name__ == "__main__":
    unittest.main()
