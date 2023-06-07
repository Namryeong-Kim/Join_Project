from join.compile.solc_parse.parser import parse as solc_parse
import sys
from slither.slither import Slither


class Compile(Slither):
    def __init__(self, target):
        self.target = target
        solc_parse()
        super().__init__(self.target)


