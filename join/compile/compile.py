from join.compile.solc_parse.parser import parse as solc_parse
import sys
from slither.slither import Slither


class Compile:
    def __init__(self, target):
        self.target = target

    def solc_parse(self):
        solc_parse()
            
    def compile_and_slither_parse(self):
        compile = Slither(self.target)
        print("Contract list: ")
        for contract in compile._compilation_units[0].contracts:
            print(contract)
        print("\nFunction list: ")
        for function in compile._compilation_units[0].functions:
            print(function)
        
