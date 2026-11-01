
# You can change the text color in Python's print() using ANSI escape codes.

def color_text(text, color):
    colors = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m"
    }

    color_code = colors.get(color.lower())

    if color_code is None:
        return text

    return f"{color_code}{text}\033[0m"