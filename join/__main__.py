import argparse
import sys
from solc_select import solc_select
from join.rule_set.rule import RuleSet
from join.run_detectors.detectors import RunDetector


def parse_arguments():
    usage = 'sikk target [<args>]\n\n'
    usage += 'target can be:\n\t'
    usage += '- file path(.sol file)\n\t'
    usage += '- directory path\n\t\t'
    usage += '- supported platforms: https://github.com/crytic/crytic-compile/#crytic-compile\n\t'
    usage += '- .zip file\n\t'

    parser = argparse.ArgumentParser(
        prog='sikk', usage=usage, formatter_class=argparse.RawTextHelpFormatter)
    # parser.add_argument('file_path', help=argparse.SUPPRESS, nargs='?')
    parser.add_argument(
        "--version", help="displays the current solc version and installed list", action="store_true")

    subparsers = parser.add_subparsers(
        dest='command', required=False)

    # Rule Setting (Add/Remove)
    rule_parser = subparsers.add_parser('ruleset')
    rule_subparsers = rule_parser.add_subparsers(
        dest='rule_command', required=True)
    add_parser = rule_subparsers.add_parser('add', help='Add a rule')
    add_parser.add_argument('file_path', help='Path to the rule file')

    remove_parser = rule_subparsers.add_parser('remove', help='Remove a rule')
    remove_parser.add_argument('rule_name', help='Name of the rule to remove')

    # Detector (Vulnerability/Logic)
    detect_parser = subparsers.add_parser('detect')
    detect_subparsers = detect_parser.add_subparsers(
        dest='detect_command', required=True)
    vuln_parser = detect_subparsers.add_parser(
        'vuln', help='Vulnerability detector, defaults to all')
    vuln_parser.add_argument('target', help='Target Rule', nargs='*')
    vuln_parser.add_argument('file_path', help='Path to the rule file')
    logic_parser = detect_subparsers.add_parser('logic', help='Logic detector')
    logic_parser.add_argument(
        'logic', choices=['Uniswap', 'Balancer', 'dydx'], help='Logic detector type')
    
    # Printer (Contract/Function/Variable/SlithIR)
    print_parser = subparsers.add_parser('print')
    print_subparsers = print_parser.add_subparsers(dest='print_command', required=True)
    print_subparsers.add_parser('contract', help='Print contract')
    print_subparsers.add_parser('function', help='Print function')
    print_subparsers.add_parser('variable', help='Print variable')
    print_subparsers.add_parser('slithir', help='Print SlithIR')

    # Code Similar (Train/Test)
    code_similar_parser = subparsers.add_parser('code-similar')
    code_similar_parser.add_argument('mode', choices=['train', 'test'], help='Code Similar mode')
    code_similar_parser.add_argument('--path', help='Path to the target file')
    code_similar_parser.add_argument('--fname', help='File name of the target file')
    code_similar_parser.add_argument('--detect', help='Directory containing code for detection')
    code_similar_parser.add_argument('--bin', help='Path to the binary file')
    code_similar_parser.add_argument('--contract', help='Directory containing contracts')

    # parser.add_argument('file_path', help=argparse.SUPPRESS, nargs='?')
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    # print(args)
    return args


def version_info():
    current_version = solc_select.current_version()
    installed_versions = solc_select.installed_versions()
    version_info = f"\nCurrent version: {current_version}\n\nInstalled versions: {installed_versions}\n"
    return version_info


def rule_set_action(action, target):
    instance = RuleSet(target)
    if action == 'add':
        instance.register_detector()
        instance.print_compared_files()
        print(f"Adding ruleset for file: {target}")
    elif action == 'remove':
        instance.unregister_detector(target)
        print(f"Removing ruleset for file: {target}")


def detect_vuln_action(target, file_path):
    if not target:
        print("Detecting all vulnerabilities")
        instance = RunDetector(file_path)
        instance.run_and_print_detectors()

    else:
        instance = RunDetector(file_path, target)
        instance.run_and_print_detectors()


def main():
    args = parse_arguments()
    if args.version:
        print(version_info())
    elif args.command == 'ruleset':
        if hasattr(args, 'file_path'):
            target = args.file_path
        elif hasattr(args, 'rule_name'):
            target = args.rule_name
        else:
            print("No target specified.")
            return
        rule_set_action(args.rule_command, target)
    elif args.command == 'detect':
        if args.detect_command == 'vuln':
            detect_vuln_action(args.target, args.file_path)
        elif args.detect_command == 'logic':
            print(args.logic)
        else:
            print("No target specified.")
            return


if __name__ == '__main__':
    main()
