from join.compile.solc_parse.parser import parse as solc_parse
import sys
from crytic_compile import CryticCompile
import os
import re
from join.compile.solc_parse.parser_function import install_solc
from solc_select.solc_select import switch_global_version


class JoinCompile():
    def __init__(self, target: str):
        # install_solc('0.8.20')
        # switch_global_version('0.8.20', True) -> requirements.txt에 추가
        self.target_path = os.path.abspath(target)
        self.target_list = []
        self.target_versions = []
        self.compilation_units = []

        # for i in self.units.compilation_units:
        #     print(Slither(self.units.compilation_units[i].crytic_compile))
        # super().__init__(self.units)
    def find_all_solidity_files(self, extension):
        sol_files = []
        for root, dirs, files in os.walk(self.target_path):
            for file in files:
                if file.endswith(extension):
                    file_path = os.path.join(root, file)
                    sol_files.append(file_path)
        return sol_files

    def get_versions(self, file):
        PATTERN = re.compile(
            r"pragma solidity\s*(?:\^|>=|<=)?\s*(\d+\.\d+\.\d+)")
        with open(file, encoding="utf8") as file_desc:
            buf = file_desc.read()
            result = PATTERN.findall(buf)
        return result

    def get_files_in_directory(self):
        for root, dirs, files in os.walk(self.target_path):
            for file in files:
                file_path = os.path.join(root, file)
                self.target_list.append(file_path)
        return self.target_list

    def get_crytic_compile_list(self, path):
        self.compilation_units.append(CryticCompile(path))
        return self.compilation_units

    def get_minor_version(versions):
        return sorted(versions)[0]

    def select_compile_version(version):
        try:
            install_solc(version)
            switch_global_version(version, True)
        except:
            print('Failed to switch compile versions')

    def compile(self):
        if os.path.isdir(self.target_path):
            files = self.find_all_solidity_files(self.target_path, '.sol')
            for i, file in files:
                self.target_versions = self.get_versions(file)
                print(self.target_versions)
                selected_version = self.target_versions[i]
                install_solc(selected_version)
            for i, path in self.target_list:
                selected_version = self.target_versions[ i]
                switch_global_version(selected_version, True)
                self.get_crytic_compile_list(path)
            print(self.compilation_units)
        elif (os.path.isfile(self.target_path)):
            if (self.target_path.endswith('.sol')):
                self.units = CryticCompile(self.target_path)
            elif (self.target_path.endswith('.zip')):
                
                self.units = CryticCompile(self.target_path)
            else:
                print('Not supported file type')
                sys.exit(0)
        else:
            # solc_parse(target)
            print('Not supported file type')
            sys.exit(0)

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
s = JoinCompile('./example/')
print(s.get_files_in_directory())
print(s.compile())
print(s.target_list)

