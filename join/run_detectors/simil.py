import logging
import operator
import sys
import traceback

import argparse
from argparse import Namespace

from join.run_detectors.encode import encode_contract, load_and_encode, parse_target
from join.run_detectors.model import load_model
from join.run_detectors.similarity import similarity
from slither.slither import Slither

import os

from join.run_detectors.cache import save_cache
from join.run_detectors.encode import encode_contract, load_contracts
from join.run_detectors.model import train_unsupervised

logger = logging.getLogger("Slither-simil")
logger.setLevel(logging.INFO)  # Set log level to INFO

class Simil:
    @staticmethod
    def test(path, fname, detector, bin='/Users/dlanara/Desktop/immm/JOIN/etherscan_verified_contracts.bin') -> list:
        result = []
        args = Namespace(mode='test', model=bin, filename=path, fname=fname, ntop=10, input=detector)

        try:
            model = args.model
            model = load_model(model)
            filename = args.filename
            contract, fname = parse_target(args.fname)
            infile = args.input
            ntop = args.ntop

            if filename is None or contract is None or fname is None or infile is None:
                print("The test mode requires filename, contract, fname and input parameters.")
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
        args = Namespace(mode='train', model=bin, input = contract, filename=None)

        try:
            last_data_train_filename = "last_data_train.txt"
            model_filename = args.model
            dirname = args.input

            if dirname is None:
                logger.error("The train mode requires the input parameter.")
                sys.exit(-1)
            contracts = load_contracts(dirname)
            logger.info("Saving extracted data into %s", last_data_train_filename)
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
                            cache.append((os.path.split(filename_inner)[-1], contract, function, x))

            logger.info("Starting training")
            model = train_unsupervised(input=last_data_train_filename, model="skipgram")
            logger.info("Training complete")
            logger.info("Saving model")
            model.save_model(model_filename)

            for i, (filename, contract, function, irs) in enumerate(cache):
                cache[i] = ((filename, contract, function), model.get_sentence_vector(irs))

            logger.info("Saving cache in cache.npz")
            save_cache(cache, "cache.npz")
            logger.info("Done!")

        except Exception:  # pylint: disable=broad-except
            logger.error(f"Error in {args.filename}")
            logger.error(traceback.format_exc())
            sys.exit(-1)

simil = Simil()

# def test(path, fname, detector, bin)
# test = simil.test('uni.sol', 'Router.Hi', 'Uniswap')
# [print(t) for t in test]

# def train(bin, contract):
# train = simil.train('model.bin', 'Uniswap')