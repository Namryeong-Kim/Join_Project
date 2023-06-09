import ast
import difflib
from slither.detectors import all_detectors
import os

class PySimilarity():
    def __init__(self, new_detector:str):
        self.new_detector = new_detector
        self.detectors_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../slither/slither/detectors/"))
        self.new_detector_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../slither/slither/detectors/customized_rules",new_detector))
        self.new_detector_content = self.read_file()

    def get_files_in_directory(self):
        file_list = []
        exclude_patterns = ["all_detectors.py", "abstract_detector.py", "__init__.py"]
        for root, dirs, files in os.walk(self.detectors_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                if exclude_patterns and any(pattern in file for pattern in exclude_patterns):
                    continue
                
                file_list.append(file_path)
        return file_list

    def read_file(self):
        with open(self.new_detector_path, "r") as file:
            return file.read()

    def get_ast(target):
        return ast.parse(target)

    def compare_files(self):
        new_detector_ast = self.get_ast(self.new_detector_content)

        for origin_detector in self.get_files_in_directory():
            origin_detector_ast = self.get_ast(origin_detector)

            diff = difflib.SequenceMatcher(None, ast.dump(new_detector_ast), ast.dump(origin_detector_ast))
            similarity_ratio = diff.ratio()
            print(f"Similarity between {self.new_detector} and {origin_detector}: {similarity_ratio}")

        return similarity_ratio

    def compare_multiple_files(file_list):
        similarity_matrix = {}
        
        for i, file1 in enumerate(file_list):
            similarity_matrix[file1] = {}
            for j, file2 in enumerate(file_list):
                if i == j:
                    similarity_matrix[file1][file2] = 1.0
                elif j < i:
                    similarity_matrix[file1][file2] = similarity_matrix[file2][file1]
                else:
                    similarity = compare_files(file1, file2)
                    similarity_matrix[file1][file2] = similarity
        
        return similarity_matrix


# similarity_matrix = compare_multiple_files(file_list)

# # Print the similarity matrix
# for file1 in file_list:
#     for file2 in file_list:
#         similarity = similarity_matrix[file1][file2]
#         print(f"Similarity between {file1} and {file2}: {similarity}")

file_ = PySimilarity("dream.py")
file_list =file_.get_files_in_directory()
#print(file_.new_detector_content)
print(file_.get_ast(file_.new_detector_content)[0])
