from join.compile.solc_parse.parser import parse as solc_parse
import sys
from slither.slither import Slither
from crytic_compile import CryticCompile, InvalidCompilation
from pathlib import Path
from slither.detectors.examples.backdoor import Backdoor
import os
import importlib.util
class Join(Slither):
    def __init__(self, target):
        self.target = target
        if(os.path.isdir(target)):
            self.units = CryticCompile(target)
        else: 
            #solc_parse(target)
            self.units = CryticCompile(target)

        print(self.units)
        for i in self.units.compilation_units:
            print(Slither(self.units.compilation_units[i].crytic_compile))
        super().__init__(self.units)

    def functions(self):
        result = []
        for unit in self.compilation_units:
            for func in unit.functions:
                result.append(func)

        return result
            
    def ir(self):
        for contract in self.contracts:
            print(contract)
            for function in contract.functions:
                for node in function.nodes:
                    print(node)

s = Join('/Users/sikk/project_dream/Join_Project/join/src/')
# s = Join('../re-entrancy.sol')
def import_class_from_path(file_path, class_name):
    spec = importlib.util.spec_from_file_location("module.name", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, class_name)

file_path = "../example-detector.py"  # Provided file path
class_name = "Backdoor"  # Provided class name

# Import the class from the file
Backdoor = import_class_from_path(file_path, class_name)

# Now you can use Example
for unit in s.compilation_units:
    print(unit)
s.register_detector(Backdoor)
result =s.run_detectors()
print(result)

