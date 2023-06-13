from slither_core.detectors import all_detectors
from join.compile.compile import Join


class RunDetector(Join):
    available_detector_list = []

    def __init__(self, input_file, detectors=None):
        self._detectors = []
        self.target = input_file
        (_, self.category, self.import_list) = self.get_all_detectors()
        self.selected_detectors = detectors if detectors is not None else []
        super().__init__(input_file)

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
        values = list(self.compilation_units.values())
        for instance in values:
            if not self.selected_detectors:
                for item in self.import_list[8:]:
                    instance.register_detector(item)
            elif self.selected_detectors:
                for detector in self.selected_detectors:
                    if detector in self.category:
                        category = detector.capitalize()
                        filtered_list = [
                            item for item in self.import_list if f'{category}' in str(item)]
                        for item in filtered_list:
                            instance.register_detector(item)
                    elif detector in self.available_detector_list:
                        filtered_list = [
                            item for item in self.import_list if f'{detector}' in str(item)]
                        for item in filtered_list:
                            instance.register_detector(item)
                    else:
                        print(f'{detector} is not available')
                        exit(0)
            else:
                print('No available detectors')

    def print_detectors(self):
        description = []
        res = []
        values = list(self.compilation_units.values())
        for instance in values:
            results = instance.run_detectors()
            if not results:
                print('No results')
            # print(results)  # result 요소 중에 description만 뽑고 있는데, 필요한 정보 더 뽑을 수 있음
            else:
                for detector_result in results:
                    for result in detector_result:
                        # res.append(result['description'])
                        # res.append(result['markdown'])
                        # res.append(result['first_markdown_element'])
                        description.append(result['description'])
                res.append(description)
        return res

    def run_and_print_detectors(self):
        self.register_detectors()
        results = self.print_detectors()
        for result in results:
            for item in result:
                print(item)


# d = RunDetector('./re-entrancy.sol', ['Dream'])
# d.run_and_print_detectors()
