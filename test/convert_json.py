import json
import solc
from crytic_compile import CryticCompile, compile_all
from crytic_compile.platform import Type
# def create_json(files):
#     sources = {file: {"content": open(file).read()} for file in files}

#     data = {
#         "language": "Solidity",
#         "sources": sources,
#         "settings": {
#             "outputSelection": {
#                 "*": {
#                     "*": ["*"]
#                 }
#             }
#         }
#     }

#     return data

# 파일 경로 리스트 예제
# files = [
#     "/Users/sikk/project_dream/join/join/test/reentrancy.sol",
#     "/Users/sikk/project_dream/join/join/test/example_code/dos.sol",
# ]

# json_data = create_json(files)

# # JSON 형태로 출력
# print(json.dumps(json_data, indent=2))

# # JSON 데이터 생성
# json_data = create_json(files)

# # JSON 파일을 저장할 경로
# json_path = "example.json"

# # JSON 데이터를 파일로 저장
# with open(json_path, 'w') as f:
#     json.dump(json_data, f)
# files = ["/Users/sikk/project_dream/join/join/test/example_code/","/Users/sikk/project_dream/join/join/test/example_code/reentrancy.sol"]

# # compilations = compile_all(files, solc_standard_json=True)

# # crytic_compile = CryticCompile(files, solc_standard_json=True)
# results=CryticCompile(files[0], platform=Type.SOLC_STANDARD_JSON)

directory_path = "/Users/sikk/project_dream/Join_Project/test/example_code/"
compilations = compile_all(directory_path, solc_standard_json=True)
print(compilations[0].src_content)
#print(compilations[1].filenames)