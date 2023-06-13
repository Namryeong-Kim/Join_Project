import logging
import operator
import sys
import traceback
import zipfile


from argparse import Namespace

import os

from join.compile.compile import Join
from join.utils.simil.cache import save_cache
from join.utils.simil.encode import encode_contract, load_contracts, parse_target, load_and_encode
from join.utils.simil.model import train_unsupervised, load_model
from join.utils.simil.similarity import similarity

logger = logging.getLogger("Slither-simil")
logger.setLevel(logging.INFO)  # Set log level to INFO


class Simil:
    @staticmethod
    def test(path, fname, detector, bin) -> list:
        result = []
        args = Namespace(mode='test', model=bin, filename=path,
                         fname=fname, ntop=10, input=detector)

        try:
            model = args.model
            model = load_model(model)
            filename = args.filename
            contract, fname = parse_target(args.fname)
            infile = args.input
            ntop = args.ntop

            if filename is None or contract is None or fname is None or infile is None:
                print(
                    "The test mode requires filename, contract, fname and input parameters.")
                sys.exit(-1)

            irs = encode_contract(filename, **vars(args))
            if len(irs) == 0:
                sys.exit(-1)

            y = " ".join(irs[(filename, contract, fname)])

            fvector = model.get_sentence_vector(y)
            cache = load_and_encode(infile, model, **vars(args))
            # save_cache("cache.npz", cache)

            r = {}
            for x, y in cache.items():
                r[x] = similarity(fvector, y)

            r = sorted(r.items(), key=operator.itemgetter(1), reverse=True)
            for x, score in r[:ntop]:
                score = round(score, 3)
                result.append(list(x) + [score])
            return result

        except Exception as e:
            print(f"Error in {args.filename}")
            print(traceback.format_exc())
            sys.exit(-1)

    @staticmethod
    def train(bin, contract):
        args = Namespace(mode='train', model=bin,
                         input=contract, filename=None)

        try:
            last_data_train_filename = "last_data_train.txt"
            model_filename = args.model
            dirname = args.input

            if dirname is None:
                logger.error("The train mode requires the input parameter.")
                sys.exit(-1)
            contracts = load_contracts(dirname)
            logger.info("Saving extracted data into %s",
                        last_data_train_filename)
            cache = []
            with open(last_data_train_filename, "w", encoding="utf8") as f:
                for filename in contracts:
                    # cache[filename] = dict()
                    for (filename_inner, contract, function), ir in encode_contract(
                        filename, **vars(args)
                    ).items():
                        if ir != []:
                            x = " ".join(ir)
                            f.write(x + "\n")
                            cache.append(
                                (os.path.split(filename_inner)[-1], contract, function, x))

            logger.info("Starting training")
            model = train_unsupervised(
                input=last_data_train_filename, model="skipgram")
            logger.info("Training complete")
            logger.info("Saving model")
            model.save_model(model_filename)

            for i, (filename, contract, function, irs) in enumerate(cache):
                cache[i] = ((filename, contract, function),
                            model.get_sentence_vector(irs))

            logger.info("Saving cache in cache.npz")
            save_cache(cache, "cache.npz")
            logger.info("Done!")

        except Exception:  # pylint: disable=broad-except
            logger.error(f"Error in {args.filename}")
            logger.error(traceback.format_exc())
            sys.exit(-1)

    def _check_similar(self, path, detector, contract):
        compile = Join(path)
        functions = []
        bin_path = (os.path.abspath(os.path.join(
            os.path.dirname(os.path.abspath(__file__))))+'/etherscan_verified_contracts.bin')
        zip_path = (os.path.abspath(os.path.join(
            os.path.dirname(os.path.abspath(__file__))))+'/etherscan_verified_contracts.zip')

        for compilation_unit in compile.compilation_units.values():
            for con in compilation_unit.contracts:
                print(con)
                if str(con) == str(contract):
                    for function in con.functions:
                        if function.expressions:
                            functions.append(function.name)
        print(functions)
        detect = []
        result = []
        detect_list = {'addLiquidity': 'UniswapAddLiquidity',
                       'addLiquidityETH': 'UniswapAddLiquidityETH'}

        try:
            if not os.path.exists(bin_path):
                self.extract_zip(zip_path,
                                 os.path.abspath(os.path.join(
                                     os.path.dirname(os.path.abspath(__file__)))))

        except:
            if not os.path.exists('./etherscan_verified_contracts.zip'):
                print('etherscan_verified_contracts.zip not found')
                sys.exit(0)

        for func in functions:
            fname = f'{contract}.{func}'
            results = self.test(compile.target_path, fname, detector, bin_path)
            for r in results:
                if r[3] > 0.96:
                    detector_name = results[0][2]
                    if detector_name in detect_list:
                        detector_value = detect_list[detector_name]
                        result.append(
                            {'target': fname, 'detect': f'{results[0][1]}.{results[0][2]}', 'detector': detector_value, 'score': r[3]})
                    else:
                        result.append(
                            {'target': fname, 'detect': f'{results[0][1]}.{results[0][2]}', 'detector': results[0][2], 'score': r[3]})

        detect.extend(result)
        return detect

    def extract_zip(self, zip_path, extract_path):
        zip_path = os.path.abspath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), zip_path))
        print(zip_path)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

# simil = Simil()

# def test(path, fname, detector, bin)
# test = simil.test('uni.sol', 'Router.Hi', 'Uniswap')
# [print(t) for t in test]

# def train(bin, contract):
# train = simil.train('model.bin', 'Uniswap')

# simil = Simil()
# detect = simil._check_similar('/Users/dlanara/Desktop/immm/code/category/uniswapv2/uniswapv2.sol', 'Uniswap', '/Users/dlanara/Desktop/immm/backup/Uniswap')
# print(detect)
