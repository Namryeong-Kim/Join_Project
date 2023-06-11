from join.compile.solc_parse.parser import parse as solc_parse
import sys
from slither.slither import Slither
from crytic_compile import CryticCompile
from pathlib import Path
import os
import importlib.util
import ast
from join.compile.solc_parse.parser_function import install_solc
from solc_select.solc_select import switch_global_version


class Join():
    def __init__(self, target):
        # install_solc('0.8.20')
        # switch_global_version('0.8.20', True)
        self.target = target
        self.target_path = os.path.abspath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), self.target))

        if (os.path.isdir(target)):
            self.units = CryticCompile(self.target_path)
        elif (os.path.isfile(target)):
            if (target.endswith('.sol')):
                self.units = CryticCompile(self.target_path)
            elif (target.endswith('.zip')):
                self.units = CryticCompile(self.target_path)
            else:
                print('Not supported file type')
                sys.exit(0)
        else:
            # solc_parse(target)
            print('Not supported file type')
            sys.exit(0)

        # for i in self.units.compilation_units:
        #     print(Slither(self.units.compilation_units[i].crytic_compile))
        # super().__init__(self.units)

    def import_class_from_path(file_path, class_name):
        spec = importlib.util.spec_from_file_location("module.name", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, class_name)

    def get_files_in_directory(self):
        file_list = []
        for root, dirs, files in os.walk(self.target_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_list.append(file_path)
        return file_list

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


# s = Join('../src/')
s = Join('example/')
print(s.target_path)
print(s.get_files_in_directory())
