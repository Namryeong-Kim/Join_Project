from crytic_compile.platform.types import Type
from crytic_compile import CryticCompile
from join.compile.solc_parse.parser import parse as solc_parse
from join.compile.compile import Compile
from slither.slither import Slither
import sys
from join.dream import Dream


def main():
    target = sys.argv[1]
    # compile = Compile(target)
    # print(compile.compilation_units[0].compiler_version.version)
    # for compilation_unit in compile.compilation_units:
    #     for contract in compilation_unit.contracts:
    #         for function in contract.functions:
    #             print(f'{contract}.{function}')
    detector = Slither(target)
    detector.register_detector(Dream)
    print(detector.detectors)
    
    

#argparse
#solc parse
#flattening
#compile
#




if __name__ == '__main__':
    main()