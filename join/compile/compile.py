from join.compile.solc_parse.parser import parse as solc_parse
import sys
from slither.slither import Slither

def main():
    target = sys.argv[1]
    solc_parse()
    Slither(target)
    print(Slither.compilation_units)


if __name__ == '__main__':
    main()