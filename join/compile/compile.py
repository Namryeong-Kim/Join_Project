from join.compile.solc_parse.parser import parse as solc_parse
import sys
from crytic_compile import CryticCompile
import os
import re
from solc_select.solc_select import switch_global_version
import join.compile.solc_parse.parser_function as ps


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
        content = ps.get_solidity_source(file)
        sign, version = ps.parse_solidity_version(content)
        print(sign, version)
        return sign, version

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

    def parse(self, file_path):
        sign, version = self.get_versions(file_path)

        if len(version) != 1:
            sign, version = ps.compare_version(sign, version)
        sign = sign[0]
        version = version[0]

        index = ps.find_matching_index(version, version_list)

        if sign == '<':
            version = version_list[index - 1]
        elif sign == '>':
            version = version_list[index + 1]
        elif (sign == '^' or sign == '~'):
            version = ps.get_highest_version(version_list, version)
        elif (sign == '=' or sign == '>=' or sign == '<=') or (not sign and version):
            version = version
        else:
            print("incorrect sign")
            return

    def select_compile_version(version):
        try:
            ps.install_solc(version)
            switch_global_version(version, True)
        except:
            print('Failed to switch compile versions')

    def compile(self):
        if os.path.isdir(self.target_path):
            files = self.find_all_solidity_files('.sol')
            for i, file in files:
                self.target_versions = self.get_versions(file)
                print(self.target_versions)
                selected_version = self.target_versions[i]
                ps.install_solc(selected_version)
            for i, path in self.target_list:
                selected_version = self.target_versions[i]
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
