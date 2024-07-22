#!/bin/sh
docker run \
    --rm --name optjupyter -d -p 8080:8080 \
    -v `pwd`/../workspace:/workspace -w /workspace optimizers:1.1 \
    jupyter-lab --no-browser --port=8080 --ip=0.0.0.0 \
    --allow-root --NotebookApp.token=''
