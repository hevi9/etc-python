import sys

INFO = dict()
with open("INFO") as f:
    exec(f.read(), INFO)
    del INFO["__builtins__"]


def do_help():
    """ print usage """
    print("Commands:")
    for cmd in sorted([i for i in globals().keys() if i.startswith("do_")]):
        print(" ", cmd[3:], "-", globals()[cmd].__doc__.strip())
    print("INFO:")
    for key, value in INFO.items():
        print(" ", key, "=", value)


def do_control():
    """ make debian control file"""
    print("""Package: {name}
Version: {version}
Section: games
Maintainer: {author}
Architecture: all
Depends: python3
Description: {title}
""".format(**INFO))


def main(args=sys.argv[1:]):
    globals()["do_" + args[0]]()


if __name__ == "__main__":
    main()
