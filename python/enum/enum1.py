import enum

class Color(enum.Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

class ColorStr(enum.Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"


def max_length(enum_str):
    return max(len(i.value) for i in enum_str)


def main():
    for color in Color:
        print(color.name, color.value)

    for color in ColorStr:
        print(color.name, color.value)

    print("ColorStr max length of values set", max_length(ColorStr))

if __name__ == "__main__":
    main()