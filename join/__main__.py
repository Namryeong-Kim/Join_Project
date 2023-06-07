from crytic_compile.platform.types import Type
from crytic_compile import CryticCompile
from join.compile.solc_parse.parser import parse as solc_parse
from join.compile.compile import Compile
import sys

# def parse_args(
#     detector_classes: List[Type[AbstractDetector]], printer_classes: List[Type[AbstractPrinter]]
# ) -> argparse.Namespace:
#     usage = "slither target [flag]\n"
#     usage += "\ntarget can be:\n"
#     usage += "\t- file.sol // a Solidity file\n"
#     usage += "\t- project_directory // a project directory. See https://github.com/crytic/crytic-compile/#crytic-compile for the supported platforms\n"
#     usage += "\t- 0x.. // a contract on mainnet\n"
#     usage += f"\t- NETWORK:0x.. // a contract on a different network. Supported networks: {','.join(x[:-1] for x in SUPPORTED_NETWORK)}\n"

#     parser = argparse.ArgumentParser(
#         description="For usage information, see https://github.com/crytic/slither/wiki/Usage",
#         usage=usage,
#     )

#     parser.add_argument("filename", help=argparse.SUPPRESS)

#     cryticparser.init(parser)

#     parser.add_argument(
#         "--version",
#         help="displays the current version",
#         version=require("slither-analyzer")[0].version,
#         action="version",
#     )



def main():
    target = sys.argv[1]
    compile = Compile(target)
    for compilation_unit in compile.compile._compilation_units:
        for contract in compilation_unit.contracts:
            for function in contract.functions:
                print(f'{contract}.{function}')
    
    

#argparse
#solc parse
#flattening
#compile
#




if __name__ == '__main__':
    main()