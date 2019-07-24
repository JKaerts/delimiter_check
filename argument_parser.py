import argparse
import sys

class CustomFormatter(argparse.RawDescriptionHelpFormatter,
                      argparse.ArgumentDefaultsHelpFormatter):
    pass

def parse_args(args=sys.argv[1:]):
    """Parse arguments"""
    parser = argparse.ArgumentParser(
        description=sys.modules[__name__].__doc__,
        formatter_class=CustomFormatter)
    parser.add_argument("-i",
        metavar="INPUT",
        dest='input_file',
        help="The input file")

    return parser.parse_args(args)

if __name__ == "__main__":
    args = parse_args()
    print(args.input_file)
