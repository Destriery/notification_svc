import sys

from .babel import Babel

def execute_from_command_line(argv):
    try:
        method_name = argv[1]
    except IndexError:
        print(f'Usage: {argv[0]} [method_name] [*args]\n\nerror: "method_name" was not specified')
        sys.exit()

    if 'babel_' in method_name:
        Babel(argv[1:])