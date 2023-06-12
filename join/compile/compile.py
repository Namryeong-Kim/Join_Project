import os
from crytic_compile import CryticCompile
from solc_select.solc_select import switch_global_version
from pathlib import Path
import join.compile.solc_parse.parser_function as ps
import sys
from slither.core.slither_core import SlitherCore
from join.compile.solc_parse.parser import parse as solc_parse



class JoinCompile(SlitherCore):
    def __init__(self, target: str):
        self.target_path = os.path.abspath(target)
        super().__init__()
        
        if os.path.isdir(self.target_path):
            self.target_list = self.find_all_solidity_files('.sol')
            crytic_compile=self.get_crytic_compile_list()
            self._crytic_compile = crytic_compile

        elif (os.path.isfile(self.target_path)):
            if (self.target_path.endswith('.sol')):
                solc_parse(self.target_path)
                crytic_compile = CryticCompile(self.target_path)
                self._crytic_compile = crytic_compile
            elif (self.target_path.endswith('.zip')):

                crytic_compile = CryticCompile(self.target_path)
                self._crytic_compile = crytic_compile
            else:
                print('Not supported file type')
                sys.exit(0)
        else:
            print('Not supported file type')
            sys.exit(0)

    def find_all_solidity_files(self, extension: str):
        target_list = []
        for root, dirs, files in os.walk(self.target_path):
            for file in files:
                if file.endswith(extension):
                    file_path = os.path.join(root, file)
                    target_list.append(file_path)
        return target_list

    def get_versions(self, file):
        content = ps.get_solidity_source(file)
        sign, version = ps.parse_solidity_version(content)
        return sign, version

    def select_compile_version(self, version):
        try:
            if (self.check_installed_version(version)):
                switch_global_version(version, True)
            else:
                ps.install_solc(version)
                switch_global_version(version, True)
        except:
            print('Failed to switch compile versions')

    def parse_all_version_to_dict(self):
        version_list = ps.get_version_list()
        versions = version_list.keys()

        minor_versions_dict = {}
        for version in versions:
            minor_version = version.split('.')[1]
            minor_versions_dict[minor_version] = []

        for version in versions:
            minor_version = version.split('.')[1]
            minor_versions_dict[minor_version].append(version)

        return minor_versions_dict

    def check_installed_version(self, version):
        if "VIRTUAL_ENV" in os.environ:
            HOME_DIR = Path(os.environ["VIRTUAL_ENV"])
        else:
            HOME_DIR = Path.home()
        SOLC_SELECT_DIR = HOME_DIR.joinpath(".solc-select")
        ARTIFACTS_DIR = SOLC_SELECT_DIR.joinpath("artifacts")

        for _, _, files in os.walk(ARTIFACTS_DIR):
            for file in files:
                installed_version = file.split('-')[1]
                if (installed_version == version):
                    return True
        return False
    
    def parse(self, file_path):
        sign, version = self.get_versions(file_path)
        version_list = ps.get_version_list()

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
        return version
        
    def get_crytic_compile_list(self):
        compilation_units = []
        version = '0.8.0'  # default
        print(self.target_list)
        for file in self.target_list:
            try:
                version = self.parse(file)
                if (len(version) > 0):
                    self.select_compile_version(version)
                compilation_units.append(CryticCompile(file))
            except:
                print('compile error')

        return compilation_units
    

target = sys.argv[1]
file = JoinCompile(target)
print(file._crytic_compile)
