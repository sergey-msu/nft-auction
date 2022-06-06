#!/bin/bash
set -e

FIFT_PATH="/opt/ton/crypto/fift"
FUNC_PATH="/opt/liteclient-build/crypto/func"
FIFT_EXE_PATH="/opt/liteclient-build/crypto/fift"
TESTS_PATH="tests"
OUT_PATH="../out"

export FIFTPATH=$FIFT_PATH/lib

# build project

$FUNC_PATH \
   -SPA contracts/stdlib.fc \
        contracts/op-codes.fc \
        contracts/utils.fc \
        contracts/nft-collection.fc \
   -o $OUT_PATH/nft-collection-code.fif

$FUNC_PATH \
   -SPA contracts/stdlib.fc \
        contracts/op-codes.fc \
        contracts/utils.fc \
        contracts/nft-item.fc \
   -o $OUT_PATH/nft-item-code.fif

$FUNC_PATH \
   -SPA contracts/stdlib.fc \
        contracts/op-codes.fc \
        contracts/utils.fc \
        contracts/nft-marketplace.fc \
   -o $OUT_PATH/nft-marketplace-code.fif

$FUNC_PATH \
   -SPA contracts/stdlib.fc \
        contracts/op-codes.fc \
        contracts/utils.fc \
        contracts/nft-sale.fc \
   -o $OUT_PATH/nft-sale-code.fif

$FUNC_PATH \
   -SPA contracts/stdlib.fc \
        contracts/op-codes.fc \
        contracts/utils.fc \
        contracts/nft-auction.fc \
   -o $OUT_PATH/nft-auction-code.fif

# run tests

$FIFT_EXE_PATH -s $TESTS_PATH/unit/test-01-ignore-bounced.fif
$FIFT_EXE_PATH -s $TESTS_PATH/unit/test-02-init.fif
$FIFT_EXE_PATH -s $TESTS_PATH/unit/test-03-auction-cancel.fif


