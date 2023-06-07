import sys
import subprocess
import re, os
import json
import requests
import join.compile.solc_parse.parser_env as env
from pyparsing import Regex, Combine, Literal, OneOrMore, Empty
from pathlib import Path
from solc_select.solc_select import verify_checksum, get_url


def get_solidity_source():
    with open(sys.argv[1], 'r') as f:
    #with open(file_path, 'r') as f:
        source_code = f.read()
    return source_code

def get_version_list():
    url = f"https://binaries.soliditylang.org/{env.soliditylang_platform()}/list.json"
    list_json = requests.get(url).content
    releases = json.loads(list_json)["releases"]
    # available_releases = sorted(releases, key=lambda x: [int(v) for v in x.split('.')])
    # print(available_releases)
    return releases

def check_version(version_list, version):
    for v in version:
        if v not in version_list:
            return False   
        else:
            return True

def find_matching_index(versions, version_list):
    for i, v in enumerate(version_list):
        if versions == v:
            return i
    return None


def parse_solidity_version(source_code):
    equal = Literal("=")
    carrot = Literal("^")
    tilde = Literal("~")
    inequality = Literal("<=") | Literal(">=") | Literal("<") | Literal(">")
    combined_inequality = Combine(inequality)

    pragma_pattern = r".*pragma solidity.*"
    pragma_lines = re.findall(pragma_pattern, source_code)
    #print("[Input]:", pragma_lines[0])

    version_condition = Regex(r"\d+\.\d+(\.\d+)?")
    version_with_condition = (carrot | tilde | combined_inequality | equal) + version_condition
    pragma = Literal("pragma") + Literal("solidity") + OneOrMore(version_with_condition)

    sign = []
    version = []
    parsed_results = pragma.parseString(pragma_lines[0])
    try:
        for i, result in enumerate(parsed_results[2:]):
            if i % 2 == 0:
                sign.append(result)
            else:
                version.append(result)
    except:
        pass
    return sign, version


def compare_version(sign_list, version_list):
    min_version = min(version_list)
    min_index = version_list.index(min_version)
    return list([sign_list[min_index]]), list([min_version])


def get_highest_version(version_list, target_version):
    matching_versions = []
    target_major_minor = '.'.join(target_version.split('.')[:2])
    for v in version_list:
        if v.startswith(target_major_minor):
            matching_versions.append(v)
    return matching_versions[0]


def install_solc(version):
    if "VIRTUAL_ENV" in os.environ:
        HOME_DIR = Path(os.environ["VIRTUAL_ENV"])
    else:
        HOME_DIR = Path.home()
    SOLC_SELECT_DIR = HOME_DIR.joinpath(".solc-select")
    ARTIFACTS_DIR = SOLC_SELECT_DIR.joinpath("artifacts")
    artifact_file_dir = ARTIFACTS_DIR.joinpath(f"solc-{version}")

    artifacts = get_version_list()
    url = f"https://binaries.soliditylang.org/{env.soliditylang_platform()}/"+artifacts.get(version)
    Path.mkdir(artifact_file_dir, parents=True, exist_ok=True)
    print(f"Installing solc '{version}'...")
    #urllib.request.urlretrieve(url, artifact_file_dir.joinpath(f"solc-{version}"))

    response = requests.get(url)
    with open(artifact_file_dir.joinpath(f"solc-{version}"), "wb") as file:
        file.write(response.content)

    #verify_checksum(version)
    # Path.chmod(artifact_file_dir.joinpath(f"solc-{version}"), 0o775)

    file_path = artifact_file_dir.joinpath(f"solc-{version}")
    os.chmod(file_path, 0o775)
    print(f"Version '{version}' installed.")
    return True