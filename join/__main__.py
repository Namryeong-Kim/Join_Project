from crytic_compile.platform.types import Type
from crytic_compile import CryticCompile
from join.compile.solc_parse.parser import parse as solc_parse
from join.compile.compile import Compile
from slither.slither import Slither
import sys
from join.compile.dream import Dream


from crytic_compile import CryticCompile, InvalidCompilation
from join.compile.solc_parse.parser import parse as solc_parse
import sys

def parse_args(
    detector_classes: List[Type[AbstractDetector]], printer_classes: List[Type[AbstractPrinter]]
) -> argparse.Namespace:
    usage = "slither target [flag]\n"
    usage += "\ntarget can be:\n"
    usage += "\t- file.sol // a Solidity file\n"
    usage += "\t- project_directory // a project directory. See https://github.com/crytic/crytic-compile/#crytic-compile for the supported platforms\n"
    usage += "\t- 0x.. // a contract on mainnet\n"
    usage += f"\t- NETWORK:0x.. // a contract on a different network. Supported networks: {','.join(x[:-1] for x in SUPPORTED_NETWORK)}\n"

    parser = argparse.ArgumentParser(
        description="For usage information, see https://github.com/crytic/slither/wiki/Usage",
        usage=usage,
    )

    parser.add_argument("filename", help=argparse.SUPPRESS)

    cryticparser.init(parser)

    parser.add_argument(
        "--version",
        help="displays the current version",
        version=require("slither-analyzer")[0].version,
        action="version",
    )




def main():
    target = sys.argv[1]
    solc_parse()
#argparse
#solc parse
#flattening
#compile
#




if __name__ == '__main__':
    main()




if __name__ == '__main__':
    main()