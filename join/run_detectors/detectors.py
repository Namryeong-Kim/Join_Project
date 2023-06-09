
from typing import Type
from slither.detectors.abstract_detector import AbstractDetector
from slither.slither import Slither
from slither.detectors import all_detectors
import os
import re
import importlib

class RunDetector(Slither):
    available_detector_list = []
    def __init__(self, input_file, detectors=None):
        self._detectors = []
        (_, self.category, self.import_list) = self.get_all_detectors()
        self.selected_detectors = detectors if detectors is not None else []
        self.file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), input_file))
        
        super().__init__(self.file_path)
    
    def get_all_detectors(self):
        detector_list = [key for key in all_detectors.__dict__.keys() if not key.startswith('__')]
        import_list = [value for value in all_detectors.__dict__.values()]

        RunDetector.available_detector_list=detector_list
        category_list = ['Reentrancy','Attributes','CompilerBugs', 'CustomizedRules', 'ERC20','ERC721', 'Functions', 'Operations', 'Shadowing', 'Statements', 'Variables']
        for category in category_list:
            RunDetector.available_detector_list.append(category)
        return RunDetector.available_detector_list, category_list, import_list
    
    def register_detectors(self):
        for detector in self.selected_detectors:
            if detector in self.category:
                if detector == 'Reentrancy':
                    filtered_list = [item for item in self.import_list if '.reentrancy.' in str(item)]
                    for item in filtered_list:
                        self.register_detector(item)
                elif detector == 'Attributes':
                    filtered_list = [item for item in self.import_list if '.attributes.' in item]
                    for item in filtered_list:
                        self.register_detector(item)
                elif detector == "CompilerBugs":
                    filtered_list = [item for item in self.import_list if '.compiler_bugs.' in item]
                    for item in filtered_list:
                        self.register_detector(item)  
                elif detector == "CustomizedRules":
                    filtered_list = [item for item in self.import_list if '.customized_rules.' in item]
                    for item in filtered_list:
                        self.register_detector(item) 
                elif detector == "ERC20":
                    filtered_list = [item for item in self.import_list if '.erc.erc20.' in item]
                    for item in filtered_list:
                        self.register_detector(item)
                elif detector == "ERC721":
                    filtered_list = [item for item in self.import_list if '.erc.erc721' in item]
                    for item in filtered_list:
                        self.register_detector(item)
                elif detector == "Functions":
                    filtered_list = [item for item in self.import_list if '.functions.' in item]
                    for item in filtered_list:
                        self.register_detector(item)
                elif detector == "Operations":
                    filtered_list = [item for item in self.import_list if '.operations.' in item]
                    for item in filtered_list:
                        self.register_detector(item)
                elif detector == "Shadowing":
                    filtered_list = [item for item in self.import_list if '.shadowing.' in item]
                    for item in filtered_list:
                        self.register_detector(item)
                elif detector == "Statements":
                    filtered_list = [item for item in self.import_list if '.statements.' in item]
                    for item in filtered_list:
                        self.register_detector(item)
                elif detector == "Variables":
                    filtered_list = [item for item in self.import_list if '.variables.' in item]
                    for item in filtered_list:
                        self.register_detector(item)
                else:
                    print(f"{detector} is not available")

            else:
                if detector in RunDetector.available_detector_list:
                    print("detect list", RunDetector.available_detector_list)
                    print("import list", self.import_list)
                    if 
                    filtered_list = self.import_list if '.customized_rules.' in item]
                    self.register_detector(filtered_list[0])
                




d = RunDetector('../compile/re-entrancy.sol',['Reentrancy','Dream'])
d.register_detectors()
print(d._detectors)