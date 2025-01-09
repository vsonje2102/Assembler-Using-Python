def display_help():
    help_text = """
    Usage: python main.py <file> [-flags]

    <file>       : The input assembly file (.asm).
    -n           : Print the symbol table (similar to `nm`).
    -l           : Generate and save the listing file (p.lst).
    -s           : Print the symbol table to the console.
    -i           : Save the intermediate code to a file.
    -h           : Display this help message.

    Example:
    python main.py input.asm -nlsi
    """
    print(help_text)
    exit(0)