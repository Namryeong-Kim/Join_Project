import ast
import difflib
from slither.detectors import all_detectors
import os

class PySimilarity():
    def __init__(self, new_detector:str):
        self.new_detector = new_detector
        self.detectors_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../slither/slither/detectors/"))
        self.new_detector_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../slither/slither/detectors/customized_rules",new_detector))
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

        return similarity_ratio
    
    def _extract_class_names(self, target):
        file_name = os.path.basename(target)
        file_name_without_extension = os.path.splitext(file_name)[0]
        return file_name_without_extension


file_ = PySimilarity("SuicidalModule.py")
file_list =file_.get_files_in_directory()
file_.compare_files()
