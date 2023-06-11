import argparse
import sys
from solc_select import solc_select
from join.rule_set.rule import RuleSet


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

    # ...

    # parser.add_argument('file_path', help=argparse.SUPPRESS, nargs='?')
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    print(args) 
    return args


def version_info():
    current_version = solc_select.current_version()
    installed_versions = solc_select.installed_versions()
    version_info = f"\nCurrent version: {current_version}\n\nInstalled versions: {installed_versions}\n"
    return version_info


def rule_set_action(action, target):
    if action == 'add':
        instance = RuleSet(target)
        instance.register_detector()
        instance.print_compared_files()
        print(f"Adding ruleset for file: {target}")
    elif action == 'remove':
        instance = RuleSet(target)
        instance.unregister_detector(target)
        print(f"Removing ruleset for file: {target}")


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

    # ...


if __name__ == '__main__':
    main()
