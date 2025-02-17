#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo "Usage: analyze.sh bytecode_file datalog_file"
    exit
fi
set -x

CONTRACT_NAME=$(echo $1 | rev | cut -d'/' -f1 | rev | cut -d'.' -f1 )
BASE_CACHE_DIR=".piedpiper_temp"
FACT_CACHE_DIR="$BASE_CACHE_DIR/$CONTRACT_NAME"


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
\rm -rf ${FACT_CACHE_DIR}
$DIR/decompile -o CALL JUMPI SSTORE SLOAD MLOAD MSTORE -d -n -t ${FACT_CACHE_DIR} $1
souffle -F ${FACT_CACHE_DIR} -D ${FACT_CACHE_DIR} $2
#\rm -rf facts-tmp
