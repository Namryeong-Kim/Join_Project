import sys
import argparse
from compile import Compile
import time
from tabulate import tabulate
from slither.slither import Slither
import subprocess
from join.run_detectors.detectors import RunDetector
from join.run_detectors.simil import Simil


class Detect:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('target_file', help='Target code for analysis')
        self.parser.add_argument('detect', choice = ['detect', 'print'], help='Select mode: print or detect')
        self.parser.add_argument('detection_type', choices=['vuln', 'logic'], help='Select detection type: vuln or logic')
        self.parser.add_argument('--detector', default = '', help='Select a Detector')
        
    def main(self):
        args = self.parser.parse_args()
        compile = Compile(args.target_file)
        info = []
        for compilation_unit in compile._compilation_units:
            for contract in compilation_unit.contracts:
                if str(contract) == "Router":
                    for function in contract.functions:
                        if function.expressions:
                            info.append({"function": function.name})

        if args.detection_type == 'vuln':
            res = self._execute_slither(args.target_file, args.detector)
        elif args.detection_type == 'logic':
            if args.detector == "Uniswap":
                res = self._check_similar(args.target_file, args.detector, contract, info)
                result = self._detect_logic(args.target_file, res)
                print(result)
            else:
                print("Error : This is not supported.")
        else:
            print("Error : This is not supported.")    

    def _detect_logic(self, file, res):
        target_functions = ['addLiquidity', 'addLiquidityETH']
        detectors = []

        for function in res:
            if function['detector'] in target_functions:
                detectors.append(function['detector'])

        if detectors:
            self._execute_slither(file, detectors)
        else:
            print("No matching functions found.")

              
    @staticmethod
    def _check_similar(path, detector, contract, funcs):
        detect = []
        result = []
        for func in funcs:
            function = func['function']
            fname = f'{contract.name}.{function}'
            simil = Simil()
            test = simil.test(path, fname, detector)
            result.append({'target': fname, 'detect': f'{test[0][1]}.{test[0][2]}', 'detector':test[0][2]})
        detect.extend(result)
        return detect

    @staticmethod
    def _execute_slither(path, detector):
        d = RunDetector(path, detector)
        d.register_detectors()
        d.run_detectors()


start = time.time()
detect = Detect()
detect.main()
end = time.time()
print(f"running time: {end - start:.5f} sec")