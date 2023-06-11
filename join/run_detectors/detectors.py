from typing import Dict, List
from slither.slither import Slither
from slither.detectors import all_detectors
import os
import re


class RunDetector(Slither):
    available_detector_list = []

    def __init__(self, input_file, detectors=None):
        self._detectors = []
        (_, self.category, self.import_list) = self.get_all_detectors()
        self.selected_detectors = detectors if detectors is not None else []
        self.file_path = os.path.abspath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), input_file))

        super().__init__(self.file_path)

    def get_all_detectors(self):
        detector_list = [
            key for key in all_detectors.__dict__.keys() if not key.startswith('__')]
        import_list = [value for value in all_detectors.__dict__.values()]
        self.available_detector_list = detector_list
        category_list = ['Reentrancy', 'Attributes', 'CompilerBugs', 'CustomizedRules',
                         'ERC20', 'ERC721', 'Functions', 'Operations', 'Shadowing', 'Statements', 'Variables']
        for category in category_list:
            self.available_detector_list.append(category)
        return self.available_detector_list, category_list, import_list

    def register_detectors(self):
        if not self.selected_detectors:
            for item in self.import_list[8:]:
                self.register_detector(item)
        elif self.selected_detectors:
            for detector in self.selected_detectors:
                if detector in self.category:
                    category = detector.capitalize()
                    filtered_list = [
                        item for item in self.import_list if f'{category}' in str(item)]
                    for item in filtered_list:
                        self.register_detector(item)
                elif detector in self.available_detector_list:
                    filtered_list = [
                        item for item in self.import_list if f'{detector}' in str(item)]
                    for item in filtered_list:
                        self.register_detector(item)
                else:
                    print(f'{detector} is not available')

    def run_detectors(self):
        description = []
        results = super().run_detectors()
        # print(results) #result 요소 중에 description만 뽑고 있는데, 필요한 정보 더 뽑을 수 있음
        for detector_result in results:
            for result in detector_result:
                description.append(result['description'])
        return description

    def run_and_print_detectors(self):
        self.register_detectors()
        results = self.run_detectors()
        for result in results:
            print(result)

# d = RunDetector('./re-entrancy.sol')
# d.register_detectors()
# # print(d._detectors)
# print(d.run_detectors())
