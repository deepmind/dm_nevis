#!/bin/bash
set -ex

FRAMEWORK=$1
CONFIG=$2
OPTIONS="${@:3}"

eval LSCL_DATA_DIR="~/nevis/nevis_data_dir/stable"
eval LSCL_TENSORBOARD_DIR="~/nevis/tensorboard"

IMG="nevis-${FRAMEWORK}"
docker build -f dockerfile.${FRAMEWORK} . -t "$IMG" --network=host

docker run \
-v ${LSCL_DATA_DIR}:/tmp/nevis_data_dir \
-v ${LSCL_TENSORBOARD_DIR}:/tmp/tensorboard \
-it "$IMG" \
--config=./experiments_${FRAMEWORK}/configs/${CONFIG}.py ${OPTIONS}
