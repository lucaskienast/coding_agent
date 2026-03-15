def format_result(result: float) -> str:
    if result.is_integer():
        return str(int(result))
    return str(result)


def format_error(message: str) -> str:
    return f"Error: {message}"


def format_usage() -> str:
    return 'Usage: python main.py "<expression>"\nExample: python main.py "10 + 5"'