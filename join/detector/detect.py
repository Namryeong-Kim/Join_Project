import argparse
from join.compile.compile import Join
import time
from colored import fg, attr
from tabulate import tabulate
from slither.slither import Slither
import subprocess


class Detector:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('target_file', help='Target code for analysis')
        self.parser.add_argument('detect', help='Select mode: print or detect')
        self.parser.add_argument('detection_type', choices=['vuln', 'logic'], help='Select detection type: vuln or logic')
        self.parser.add_argument('--detector', help='Select a Detector')
        
    def main(self):
        args = self.parser.parse_args()
        compile = Join(args.target_file)
        slither = []
        for compilation_unit in compile.compile._compilation_units:
            for contract in compilation_unit.contracts:
                if str(contract) == "Router":
                    for function in contract.functions:
                        if function.expressions:
                            slither.append({"function": function.name})

        if args.detection_type == 'vuln':
            res = self._detect_vulnerability(args.target_file, args.detector)
        elif args.detection_type == 'logic':
            if args.detector == "Uniswap":
                res = self._check_similar(args.target_file, args.detector, contract, slither)
                result = self._detect_logic(args.target_file, args.detector, res)
                print(result)
            elif args.detector == "Balancer":
                print("Balancer does not have a detector yet")
            else:
                print("Error : This is not supported.")
        else:
            print("Error : This is not supported.")
    
    def _detect_vulnerability(self, file, detector):
        cmd = f'slither {file}'
        if detector is not None:
            cmd = f'slither {file} --detect {detector}'

        result = self._execute_slither(cmd)

        return result

    
    def _detect_logic(self, file, detector, res):
        table_data = []
        for function in res:
            cmd = None
            if function['detect_function'] == 'addLiquidity' or function['detect_function'] == 'addLiquidityETH':
                cmd = f'slither {file} --detect {function["detect_function"]}'
            
            if cmd is not None and self._execute_slither(cmd):
                row = [file, f'{function["target_contract"]}.{function["target_function"]}', detector, f'{function["detect_contract"]}.{function["detect_function"]}']
                table_data.append(row)

        headers = ["Target", "Target Info","Detector", "Detector Info"]
        
        return tabulate(table_data, headers=headers, tablefmt="fancy_grid")

              
    @staticmethod
    def _check_similar(path, detector, contract, funcs):
        detect = []
        for func in funcs:
            function = func['function']
            cmd = f'slither-simil test ./etherscan_verified_contracts.bin --filename ./{path} --fname {contract}.{function} --input {detector}'
            output = str(subprocess.run(cmd, shell=True, capture_output=True, text=True).stderr).split('\n')
            result = []
            for i in range(2, len(output)-1):
                res = output[i].split()
                if res[3] == '1.0':
                    detect_contract = f'{res[1]}'
                    detect_function = f'{res[2]}'
                    result.append({'target_contract': contract, 'target_function': function, 'detect_contract': detect_contract, 'detect_function': detect_function})
            detect.extend(result)                       
        return detect

    @staticmethod
    def _execute_slither(cmd):
        execute = str(subprocess.run(cmd, shell=True, capture_output=True, text=True).stderr).split('\n')
        return bool(execute)


start = time.time()
detector = Detector()
detector.main()
end = time.time()
print(f"running time: {end - start:.5f} sec")
