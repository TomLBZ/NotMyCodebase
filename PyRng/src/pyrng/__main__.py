"""Main entry point for PyRng CLI application."""

import sys
from pyrng.cli.parser import parse_args
from pyrng.cli.commands import execute_command


def main() -> int:
    """Main entry point for the PyRng application.
    
    This function is called when the pyrng command is executed.
    It parses command-line arguments and executes the appropriate command.
    
    Returns:
        Exit code (0 for success, non-zero for failure).
    
    Examples:
        >>> # When called from command line:
        >>> # $ pyrng uniform -n 10 --low 0 --high 100
    """
    args = parse_args()
    return execute_command(args)


if __name__ == "__main__":
    sys.exit(main())
