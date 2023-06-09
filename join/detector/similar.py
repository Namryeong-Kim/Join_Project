#!/usr/bin/env python3
import logging
import operator
import argparse
import sys
from fastText import load_model
from fastText import train_unsupervised
import numpy as np

from slither.tools.similarity.encode import encode_contract, load_and_encode, parse_target
from slither.tools.similarity.model import load_model
from slither.tools.similarity.similarity import similarity

logger = logging.getLogger("Slither-simil")
modes = ["test", "train"]

class Similar:

    def run(self,arg) -> None:
        self.test(arg)

    def test(self, arg: argparse.Namespace):
        model = 'etherscan_verified_contracts.bin'
        args = argparse.Namespace(
            mode='test',
            model=model,
            filename=arg['path'],
            fname=f"{arg['contract']}.{arg['function']}",
            ext=None,
            nsamples=None,
            ntop=10,
            input=arg['detector'],
            compile_force_framework=None,
            compile_libraries=None,
            compile_remove_metadata=False,
            compile_custom_build=None,
            ignore_compile=False,
            skip_clean=False,
            solc='solc',
            solc_remaps=None,
            solc_args=None,
            solc_disable_warnings=False,
            solc_working_dir=None,
            solc_solcs_select=None,
            solc_solcs_bin=None,
            solc_standard_json=False,
            solc_force_legacy_json=False,
            truffle_ignore_compile=False,
            truffle_build_directory='build/contracts',
            truffle_version=None,
            truffle_overwrite_config=False,
            truffle_overwrite_version=None,
            embark_ignore_compile=False,
            embark_overwrite_config=False,
            brownie_ignore_compile=False,
            dapp_ignore_compile=False,
            etherlime_ignore_compile=False,
            etherlime_compile_arguments=None,
            etherscan_only_source_code=False,
            etherscan_only_bytecode=False,
            etherscan_api_key=None,
            arbiscan_api_key=None,
            polygonscan_api_key=None,
            test_polygonscan_api_key=None,
            avax_api_key=None,
            ftmscan_api_key=None,
            bscan_api_key=None,
            optim_api_key=None,
            etherscan_export_dir='etherscan-contracts',
            waffle_ignore_compile=False,
            waffle_config_file=None,
            npx_disable=False,
            buidler_ignore_compile=False,
            buidler_cache_directory='cache',
            buidler_skip_directory_name_fix=False,
            hardhat_ignore_compile=False,
            hardhat_cache_directory=None,
            hardhat_artifacts_directory=None,
            foundry_ignore_compile=False,
            foundry_out_directory='out'
            )
        model = load_model(model)
        filename = args.filename
        contract, fname = parse_target(args.fname)
        infile = args.input
        ntop = args.ntop

        if filename is None or contract is None or fname is None or infile is None:
            logger.error("The test mode requires filename, contract, fname and input parameters.")
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
        logger.info("Reviewed %d functions, listing the %d most similar ones:", len(r), ntop)
        format_table = "{: <65} {: <20} {: <20} {: <10}"
        logger.info(format_table.format(*["filename", "contract", "function", "score"]))
        for x, score in r[:ntop]:
            score = str(round(score, 3))
            logger.info(format_table.format(*(list(x) + [score])))