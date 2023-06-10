from crytic_compile.platform.types import Type
from crytic_compile import CryticCompile
from join.compile.solc_parse.parser import parse as solc_parse
from join.compile.compile import Join
from slither.slither import Slither
import sys
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(prog='sikk',description='Join Analyzer')
    parser.add_argument('file_path', help='Path to the target file')
    parser.add_argument('--ruleset', action='store_true', help='select method to use ruleset(add/remove)')
    # subparsers = parser.add_subparsers(dest='command', required=True)

    # # Rule Setting (Add/Remove)
    # rule_parser = subparsers.add_parser('rule-setting')
    # rule_subparsers = rule_parser.add_subparsers(dest='rule_command', required=True)
    # rule_subparsers.add_parser('add-rule', help='Add a rule')
    # rule_subparsers.add_parser('remove-rule', help='Remove a rule')

    # # Detector (Vulnerability/Logic)
    # detect_parser = subparsers.add_parser('detect')
    # detect_subparsers = detect_parser.add_subparsers(dest='detect_command', required=True)
    # vuln_parser = detect_subparsers.add_parser('vuln', help='Vulnerability detector')
    # vuln_parser.add_argument('vuln', choices=['all', 'group', 'specific'], help='Vulnerability detector type')
    # logic_parser = detect_subparsers.add_parser('logic', help='Logic detector')
    # logic_parser.add_argument('logic', choices=['Uniswap', 'Balancer', 'dydx'], help='Logic detector type')

    # # Printer (Contract/Function/Variable/SlithIR)
    # print_parser = subparsers.add_parser('print')
    # print_subparsers = print_parser.add_subparsers(dest='print_command', required=True)
    # print_subparsers.add_parser('contract', help='Print contract')
    # print_subparsers.add_parser('function', help='Print function')
    # print_subparsers.add_parser('variable', help='Print variable')
    # print_subparsers.add_parser('slithir', help='Print SlithIR')

    # parser.add_argument('file_path', help='Path to the target file')

    args = parser.parse_args()

    return args




def main():
    args = parse_arguments()
    if args.command == 'rule-setting':
        print('rule-setting')
    # solc_parse()
#argparse
#solc parse
#flattening
#compile
#




if __name__ == '__main__':
    main()




if __name__ == '__main__':
    main()