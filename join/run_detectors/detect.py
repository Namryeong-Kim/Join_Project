import time
from tabulate import tabulate
from slither.slither import Slither
import subprocess
from join.run_detectors.simil import Simil
from arg import parse_arguments
from compile import Compile


class Detect:
    def __init__(self, args):
        self.args = args

    def main(self):
        args = self.args

        compile = Compile(args.file_path)
        info = []
        for compilation_unit in compile._compilation_units:
            for contract in compilation_unit.contracts:
                if str(contract) == "Router":
                    for function in contract.functions:
                        if function.expressions:
                            info.append({"function": function.name})

        if args.detect_command == 'vuln':
            res = self._detect_vulnerability(args.file_path, args.vuln)
        elif args.detect_command == 'logic':
            res = self._check_similar(args.file_path, args.logic, contract, info)
            result = self._detect_logic(args.file_path, args.logic, res)
            print(result)
        else:
            print("Error: This is not supported.")

    def _detect_vulnerability(self, file, detector):
        if str(detector) == 'all':
            cmd = f'slither {file}'
        else:
            cmd = f'slither {file} --detect {detector}'

        result = self._execute_slither(cmd)

        return result

    def _detect_logic(self, file, detector, res):
        table_data = []
        for function in res:
            cmd = None
            if function['detector'] == 'addLiquidity' or function['detector'] == 'addLiquidityETH':
                cmd = f'slither {file} --detect {function["detector"]}'

            if cmd is not None and self._execute_slither(cmd):
                row = [function['target'], function['detect'], function['score']]
                table_data.append(row)

        headers = ["target", "detect", "score"]

        return tabulate(table_data, headers=headers, tablefmt="fancy_grid")

    @staticmethod
    def _check_similar(path, detector, contract, funcs):
        detect = []
        result = []
        for func in funcs:
            function = func['function']
            fname = f'{contract.name}.{function}'
            simil = Simil()
            bin = '/Users/dlanara/Desktop/immm/JOIN/etherscan_verified_contracts.bin'
            results = simil.test(path, fname, detector, bin)
            for r in results:
                if r[3] == 1.0:
                    result.append({'target': fname, 'detect': f'{results[0][1]}.{results[0][2]}', 'detector': results[0][2], 'score': r[3]})
        detect.extend(result)
        return detect

    @staticmethod
    def _execute_slither(cmd):
        execute = str(subprocess.run(cmd, shell=True, capture_output=True, text=True).stderr).split('\n')
        return bool(execute)


# Parse arguments
args = parse_arguments()

start = time.time()
detect = Detect(args)
detect.main()
end = time.time()
print(f"Running time: {end - start:f} sec")
