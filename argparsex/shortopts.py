import argparse

parser = argparse.ArgumentParser(
    allow_abbrev=False,
    prog='PROG')
parser.add_argument('-x', "--exclude", action='store_true', help="exclude")
parser.add_argument('-y', action='store_true')
parser.add_argument('-z')
print(parser.parse_args(['-xyzZ']))
parser.print_help()
