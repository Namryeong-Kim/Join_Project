import os
import re
from join.compile.solc_parse.parser_function import install_solc
from crytic_compile import CryticCompile
from solc_select.solc_select import switch_global_version

PATH = os.path.abspath('./example/')


def find_all_solidity_files(directory, extension):
    sol_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                sol_files.append(file_path)
    return sol_files


def get_versions(path):
    PATTERN = re.compile(r"pragma solidity\s*(?:\^|>=|<=)?\s*(\d+\.\d+\.\d+)")
    with open(path, encoding="utf8") as file_desc:
        buf = file_desc.read()
        result = PATTERN.findall(buf)

        return result


def get_minor_version(versions):
    return sorted(versions)[0]


def select_compile_version(version):
    try:
        install_solc(version)
        switch_global_version(version, True)
    except:
        print('Failed to switch compile versions')


files = find_all_solidity_files(PATH, '.sol')
print(files)
compile_list = []
for file in files:
    print(file)
    i = 0
    target_versions = get_versions(file)
    selected_version = target_versions[i]
    install_solc(selected_version)
    switch_global_version(selected_version, True)
    compile_list.append(CryticCompile(file))
    i += 1
print(compile_list)
