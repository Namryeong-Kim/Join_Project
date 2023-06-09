from slither import Slither
from slither.detectors import all_detectors

slither = Slither('re-entrancy.sol') # slither
slither.register_detector(all_detectors.ReentrancyEth)

results = slither.run_detectors()
for detector_result in results:
    for result in detector_result:
        print(result['description'])
