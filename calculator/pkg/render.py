def format_result(result: float) -> str:
    if result.is_integer():
        s = str(int(result))
    else:
        s = str(result)
    
    padding = 2
    width = len(s) + padding * 2
    line = f"+{'-' * width}+"
    empty = f"|{' ' * width}|"
    content = f"|{' ' * padding}{s}{' ' * padding}|"
    
    return f"{line}\n{empty}\n{content}\n{empty}\n{line}"


def format_error(message: str) -> str:
    # Adding alert signs and ascii box formatting for errors
    alert = "⚠"
    text = f"{alert} Error: {message} {alert}"
    padding = 1
    width = len(text) + padding * 2
    
    line = f"+{'-' * width}+"
    empty = f"|{' ' * width}|"
    content = f"|{' ' * padding}{text}{' ' * padding}|"
    
    return f"{line}\n{empty}\n{content}\n{empty}\n{line}"


def format_usage() -> str:
    return 'Usage: python main.py "<expression>"\nExample: python main.py "10 + 5"'
