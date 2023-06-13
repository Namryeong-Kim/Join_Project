import argparse
import logging
import sys
import os
import zipfile
import shutil

from crytic_compile import cryticparser
from crytic_compile.utils.zip import ZIP_TYPES_ACCEPTED

from slither_core import Slither
from slither_core.tools.flattening.flattening import (
    Flattening,
    Strategy,
    STRATEGIES_NAMES,
    DEFAULT_EXPORT_PATH,
)

logging.basicConfig()
logger = logging.getLogger("Slither")
logger.setLevel(logging.INFO)


def parse_args() -> argparse.Namespace:
    """
    Parse the underlying arguments for the program.
    :return: Returns the arguments for the program.
    """
    parser = argparse.ArgumentParser(
        description="Contracts flattening. See https://github.com/crytic/slither/wiki/Contract-Flattening",
        usage="slither-flat filename",
    )

    parser.add_argument(
        "filename", help="The filename of the contract or project to analyze.")

    parser.add_argument(
        "--contract", help="Flatten one contract.", default=None)

    parser.add_argument(
        "--strategy",
        help=f"Flatenning strategy: {STRATEGIES_NAMES} (default: MostDerived).",
        default=Strategy.MostDerived.name,  # pylint: disable=no-member
    )

    group_export = parser.add_argument_group("Export options")

    group_export.add_argument(
        "--dir",
        help=f"Export directory (default: {DEFAULT_EXPORT_PATH}).",
        default=None,
    )

    group_export.add_argument(
        "--json",
        help='Export the results as a JSON file ("--json -" to export to stdout)',
        action="store",
        default=None,
    )

    parser.add_argument(
        "--zip",
        help="Export all the files to a zip file",
        action="store",
        default=None,
    )

    parser.add_argument(
        "--zip-type",
        help=f"Zip compression type. One of {','.join(ZIP_TYPES_ACCEPTED.keys())}. Default lzma",
        action="store",
        default=None,
    )

    group_patching = parser.add_argument_group("Patching options")

    group_patching.add_argument(
        "--convert-external", help="Convert external to public.", action="store_true"
    )

    group_patching.add_argument(
        "--convert-private",
        help="Convert private variables to internal.",
        action="store_true",
    )

    group_patching.add_argument(
        "--convert-library-to-internal",
        help="Convert external or public functions to internal in library.",
        action="store_true",
    )

    group_patching.add_argument(
        "--remove-assert", help="Remove call to assert().", action="store_true"
    )

    group_patching.add_argument(
        "--pragma-solidity",
        help="Set the solidity pragma with a given version.",
        action="store",
        default=None,
    )

    # Add default arguments from crytic-compile
    cryticparser.init(parser)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()


def find_clearinghouse_sol(directory, filename):
    clearinghouse_sol_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == filename:
                clearinghouse_sol_path = os.path.join(root, file)
                clearinghouse_sol_files.append(clearinghouse_sol_path)
    return clearinghouse_sol_files


def find_openzeppelin_folder(directory):
    for root, dirs, files in os.walk(directory):
        if '@openzeppelin' in dirs:
            openzeppelin_path = os.path.join(root, '@openzeppelin')
            return True
    return None


def find_clearinghouse_folder(temp_dir, folder_name):
    clearinghouse_folder = os.path.join(temp_dir, folder_name)

    # Check if the folder exists
    if os.path.exists(clearinghouse_folder) and os.path.isdir(clearinghouse_folder):
        return os.path.abspath(clearinghouse_folder)
    else:
        return None


def extract_zip(zip_file, output_dir):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(output_dir)


def main() -> None:
    args = parse_args()

    # Access the solc_remaps attribute
    if args.filename.endswith('.zip'):
        temp_dir = 'temp'
        os.makedirs(temp_dir, exist_ok=True)
        extract_zip(args.filename, temp_dir)
        extracted_files = os.path.abspath(temp_dir)
        filename = os.path.basename(args.filename)
        filename = filename.replace(".zip", ".sol")
        print("Filename : ", filename)
        clearinghouse_sol_files = find_clearinghouse_sol(
            extracted_files, filename)

        folder_name = filename.split(".")[0]
        print("folderName : ", folder_name)
        clearinghouse_folder_path = find_clearinghouse_folder(
            extracted_files, folder_name)

        if clearinghouse_folder_path:
            print(f"Folder named 'ClearingHouse' found in the directory.")
            print("Absolute path of the ClearingHouse folder:")
            print(clearinghouse_folder_path)
        else:
            print("No folder named 'ClearingHouse' found in the directory.")

        if clearinghouse_sol_files:
            print("ClearingHouse.sol files found in the directory:")
            for file_path in clearinghouse_sol_files:
                args.filename = file_path
                print(file_path)
        else:
            print("No ClearingHouse.sol file found in the directory.")
        args.solc_remaps = '@='+clearinghouse_folder_path+'/@'
    else:
        target_directory = os.path.basename(args.filename).split(".")[0]
        relative_path = args.filename.split(target_directory)[
            0] + target_directory
        openzeppelin_path = find_openzeppelin_folder(relative_path)

        if openzeppelin_path:
            print("The @openzeppelin folder is found at:", openzeppelin_path)
        else:
            print("The @openzeppelin folder is not found in any subdirectory.")
        args.solc_remaps = "@="+relative_path+"/@"

    print("Find Solc:", args.solc_remaps)

    print("Test:", args.filename)

    slither = Slither(args.filename, **vars(args))

    for compilation_unit in slither.compilation_units:

        flat = Flattening(
            compilation_unit,
            external_to_public=args.convert_external,
            remove_assert=args.remove_assert,
            convert_library_to_internal=args.convert_library_to_internal,
            private_to_internal=args.convert_private,
            export_path=args.dir,
            pragma_solidity=args.pragma_solidity,
        )

        try:
            strategy = Strategy[args.strategy]
        except KeyError:
            to_log = f"{args.strategy} is not a valid strategy, use: {STRATEGIES_NAMES} (default MostDerived)"
            logger.error(to_log)
            return
        flat.export(
            strategy=strategy,
            target=args.contract,
            json=args.json,
            zip=args.zip,
            zip_type=args.zip_type,
        )


if __name__ == "__main__":
    main()
