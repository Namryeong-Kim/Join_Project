from typing import List

from slither_core.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither_core.utils.output import Output
from slither_core.slithir.operations import InternalCall, LibraryCall


class UniswapAddLiquidity(AbstractDetector):
    ARGUMENT = "addLiquidity"
    HELP = "logic check in DEX"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.LOW

    WIKI = "https://github.com/Uniswap/v2-periphery/blob/0335e8f7e1bd1e8d8329fd300aea2ef2f36dd19f/contracts/UniswapV2Router01.sol#L58"
    WIKI_TITLE = "logic example"
    WIKI_DESCRIPTION = "logic example"
    WIKI_EXPLOIT_SCENARIO = ".."
    WIKI_RECOMMENDATION = ".."

    def _detect(self) -> List[Output]:
        set1 = []
        set2 = []
        results = []

        for contract in self.compilation_unit.contracts:
            for function in contract.functions:
                if function.visibility in ['external']:
                    for node in function.nodes:
                        for ir in node.irs:
                            if self.has_value_transfer(ir):
                                set1.append(node.function.name)
                            if self.has_internal_call_with_return(ir):
                                set2.append(node.function.name)

        matches = set(set1) & set(set2)

        for match in matches:
            # results.append(self.generate_result(f"{match}n"))
            results.append(self.generate_result(
                f"{match} is satisfied Business Logic in UniswapV2 AddLiquidity\n"))
        return results

    @staticmethod
    def has_value_transfer(ir):
        if isinstance(ir, LibraryCall):
            for n in ir.function.parameters:
                if (str(n._type) == 'address'):
                    for i in ir.arguments:
                        if str(i) == 'msg.sender':
                            return True

    @staticmethod
    def has_internal_call_with_return(ir):
        if isinstance(ir, InternalCall):
            if (len(ir.function.returns) == 2):
                for n in ir.arguments:
                    if str(n) != 'msg.value':
                        return True
