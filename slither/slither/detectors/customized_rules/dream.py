from typing import List

from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.utils.output import Output


class Dream(AbstractDetector):
    """
    Detect function named backdoor
    """

    ARGUMENT = "dream"  #slither option
    HELP = "Function named backdoor (detector example)"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = "https://github.com/trailofbits/slither/wiki/Adding-a-new-detector"
    WIKI_TITLE = "Backdoor example"
    WIKI_DESCRIPTION = "Plugin example"
    WIKI_EXPLOIT_SCENARIO = ".."
    WIKI_RECOMMENDATION = ".."

    def _detect(self) -> List[Output]:
        results = []

        for contract in self.compilation_unit.contracts_derived:
            # Check if a function has 'backdoor' in its name
            for f in contract.functions:
                if "DreamPlusAcademy" in f.name: #function name이 일치하면 bug로 판단하도록
                    # Info to be printed
                    info: DETECTOR_INFO = ["DreamPlusAcademy function found in ", f, "\n"]

                    # Add the result in result
                    res = self.generate_result(info)

                    results.append(res)

        return results