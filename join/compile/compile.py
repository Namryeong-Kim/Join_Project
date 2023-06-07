from join.compile.solc_parse.parser import parse as solc_parse
import sys
from slither.slither import Slither
from crytic_compile. import Type


class Compile:
    def __init__(self, target):
        self.target = target
        solc_parse()
        self.compile = Slither(self.target)
        

    # def solc_parse(self):
    #     solc_parse()
            
    # def compile_and_slither_parse(self):
    #     compile = Slither(self.target)
    #     return compile

        
