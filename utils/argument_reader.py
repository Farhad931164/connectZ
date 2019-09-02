"""
A simple module to check the command line arguments
"""
import sys


def check_input_file():
    arg_len = len(sys.argv)
    args = sys.argv

    if arg_len == 2:  # only when we have exactly 2 arguments(including script filename)
        return args[1]  # return the input filename

    return None  # all other possible routes come here
