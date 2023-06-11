import os
import re
from join.compile.solc_parse.parser_function import install_solc, get_version_list
from crytic_compile import CryticCompile
from solc_select.solc_select import switch_global_version
from pathlib import Path

PATH = os.path.abspath('./example/')


def find_all_solidity_files(directory, extension):
    sol_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                sol_files.append(file_path)
    return sol_files


def get_version(path):
    PATTERN = re.compile(r"pragma solidity\s*(?:\^|>=|<=)?\s*(\d+\.\d+\.\d+)")
    with open(path, encoding="utf8") as file_desc:
        buf = file_desc.read()
        result = PATTERN.findall(buf)

        return result


def get_minor_version(versions):
    return sorted(versions)[0]


def get_crytic_compile_list(files):
    compiled_files = []
    version = '0.8.0'  # default
    for file in files:
        try:
            version = get_version(file)
            if (len(version) > 0):
                select_compile_version(version[0])

            compiled_files.append(CryticCompile(file))
        except:
            print('compile error')

    return compiled_files


def select_compile_version(version):
    print(version)
    try:
        if (check_installed_version(version)):
            switch_global_version(version, True)
        else:
            install_solc(version)
            switch_global_version(version, True)
    except:
        print('Failed to switch compile versions')


def parse_all_version_to_dict():
    version_list = get_version_list()
    versions = version_list.keys()

    minor_versions_dict = {}
    for version in versions:
        minor_version = version.split('.')[1]
        minor_versions_dict[minor_version] = []

    for version in versions:
        minor_version = version.split('.')[1]
        minor_versions_dict[minor_version].append(version)

    return minor_versions_dict


def check_installed_version(version):
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


files = find_all_solidity_files(PATH, '.sol')


compiled_list = get_crytic_compile_list(files)

print(compiled_list)
print(parse_all_version_to_dict())

# print(compiled_list)
# switch_global_version('0.4.24',True)
