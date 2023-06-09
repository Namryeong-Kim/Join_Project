import ast
import difflib
import os
from tabulate import tabulate
from colored import fg, attr
from join.run_detectors.detectors import RunDetector

class PySimilarity():
    def __init__(self, new_detector:str):
        self.new_detector = new_detector
        self.detectors_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../slither/slither/detectors/"))
        self.new_detector_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../slither/slither/detectors/customized_rules",new_detector))
        self.example_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "example.sol"))
        self.new_detector_content = self.read_file(self.new_detector_path)

    def get_files_in_directory(self):
        file_list = []
        exclude_patterns = ["all_detectors.py", "abstract_detector.py", "__init__.py", "codex.py","common.py", self.new_detector]
        for root, dirs, files in os.walk(self.detectors_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                if exclude_patterns and any(pattern in file for pattern in exclude_patterns):
                    continue
                file_list.append(file_path)
        return file_list

    def read_file(self, target):
        with open(target, "r") as file:
            return file.read()

    def get_ast(self, target):
        return ast.parse(target)

    def compare_files(self):
        new_detector_ast = self.get_ast(self.new_detector_content)

        for origin_detector in self.get_files_in_directory():
            origin_detector_contents = self.read_file(origin_detector)
            origin_detector_ast = self.get_ast(origin_detector_contents)

            diff = difflib.SequenceMatcher(None, ast.dump(new_detector_ast), ast.dump(origin_detector_ast))
            similarity_ratio = diff.ratio()
            print(f"Similarity between {self.new_detector} and {self._extract_class_names(origin_detector)}: {similarity_ratio}")
            if similarity_ratio > 0.9:
                print(f"{self.new_detector} and {self._extract_class_names(origin_detector)} is similar\nSimilarity Ratio: {similarity_ratio}")
                return self._extract_class_names(origin_detector), origin_detector_contents
    
    def _extract_class_names(self, target):
        file_name = os.path.basename(target)
        file_name_without_extension = os.path.splitext(file_name)[0]
        return file_name_without_extension

    def print_compared_files(self):
        origin_detector, origin_detector_content = self.compare_files()
        origin_result =RunDetector(self.example_path,[self.new_detector])
        origin_result.get_all_detectors()
        origin_result.register_detectors()
        new_result = RunDetector(self.example_path,[origin_detector])
        new_result.get_all_detectors()
        new_result.register_detectors()
        result = [
            ["",self.new_detector[:-3], origin_detector],
            ["Contents", self.new_detector_content, origin_detector_content],
            ["Run Result", origin_result.run_detectors(), new_result.run_detectors()]
        ]
        table = tabulate(result, tablefmt="fancy_grid")
        print(table)
        # print(f"New Detector: {self.new_detector}")
        # print(f"Similar Detector: {self.compare_files()}")
        # print(f"New Detector Contents: {self.new_detector_content}")
        # for self.compare_files() in self.get_files_in_directory():

        # print(f"Similar Detector Contents: {self.read_file(self.compare_files())}")'
        print(f"New Detector Result: ")
        

file_ = PySimilarity("SuicidalModule.py")
file_list =file_.get_files_in_directory()
# file_.compare_files()
file_.print_compared_files()
