# based on https://github.com/suzuki-shm/PyomoContainer
From ubuntu:20.04

ENV TOOL_DIR /opt
ENV IPOPT_VERSION 3.14.14
ENV BONMIN_VERSION 1.8.9
ENV COUENNE_VERSION 0.5.8
ENV SCIP_VERSION 9.1.0
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:/lib:/usr/lib:/usr/local/lib
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gfortran \
        file \
        wget \
        git \
        cmake \
        unzip \
        pkg-config \
        zlib1g-dev \
        bison \
        flex \
        libgmp-dev \
        libgsl-dev \
        libcliquer-dev \
        libboost-program-options-dev \
        libboost-serialization-dev \
        libboost-regex-dev \
        libboost-iostreams-dev \
        libtbb-dev \
        libreadline-dev \
        libncurses5-dev \
        glpk-utils \
        liblapack-dev \
        libblas-dev \
        libopenblas-dev \
        coinor-cbc \
        coinor-libcbc-dev \
        python3-dev \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install python packages
RUN pip3 install wheel setuptools && \
    pip3 install jupyterlab

# Install ThirdParty-ASL
WORKDIR ${TOOL_DIR}
RUN git clone https://github.com/coin-or-tools/ThirdParty-ASL.git && \
    cd ${TOOL_DIR}/ThirdParty-ASL && \
    ./get.ASL && \
    ./configure --prefix=/usr/local --enable-static CC=gcc && \
    make && \
    make install && \
    cd ${TOOL_DIR} && \
    rm -rf ${TOOL_DIR}/ThirdParty-ASL

# Install ThirdParty-Mumps
WORKDIR ${TOOL_DIR}
RUN git clone https://github.com/coin-or-tools/ThirdParty-Mumps.git && \
    cd ${TOOL_DIR}/ThirdParty-Mumps && \
    ./get.Mumps && \
    ./configure --prefix=/usr/local --enable-static CC=gcc FC=gfortran && \
    make && \
    make install && \
    cd ${TOOL_DIR} && \
    rm -rf ${TOOL_DIR}/ThirdParty-Mumps

# Install ThirdParty-Metis
WORKDIR ${TOOL_DIR}
RUN git clone https://github.com/coin-or-tools/ThirdParty-Metis.git && \
    cd ${TOOL_DIR}/ThirdParty-Metis && \
    ./get.Metis && \
    ./configure --prefix=/usr/local --enable-static CC=gcc && \
    make && \
    make install && \
    cd ${TOOL_DIR} && \
    rm -rf ${TOOL_DIR}/ThirdParty-Metis

# Install Ipopt
WORKDIR ${TOOL_DIR}
RUN wget https://github.com/coin-or/Ipopt/archive/refs/tags/releases/${IPOPT_VERSION}.zip && \
    unzip ${IPOPT_VERSION}.zip && \
    rm ${IPOPT_VERSION}.zip && \
    cd ${TOOL_DIR}/Ipopt-releases-${IPOPT_VERSION} && \
    ./configure --prefix=/usr/local --enable-static CXX=g++ CC=gcc F77=gfortran && \
    make && \
    make install && \
    cd ${TOOL_DIR} && \
    rm -rf ${TOOL_DIR}/Ipopt-releases-${IPOPT_VERSION}

# Install Bonmin
WORKDIR ${TOOL_DIR}
RUN wget https://github.com/coin-or/Bonmin/archive/refs/tags/releases/${BONMIN_VERSION}.zip && \
    unzip ${BONMIN_VERSION}.zip && \
    rm ${BONMIN_VERSION}.zip && \
    cd ${TOOL_DIR}/Bonmin-releases-${BONMIN_VERSION} && \
    ./configure --prefix=/usr/local --enable-static CXX=g++ CC=gcc F77=gfortran && \
    make && \
    make install && \
    cd ${TOOL_DIR} && \
    rm -rf ${TOOL_DIR}/Bonmin-releases-${BONMIN_VERSION}

# Install Couenne
WORKDIR ${TOOL_DIR}
RUN wget https://github.com/coin-or/Couenne/archive/refs/tags/releases/${COUENNE_VERSION}.zip && \
    unzip ${COUENNE_VERSION}.zip && \
    rm ${COUENNE_VERSION}.zip && \
    cd ${TOOL_DIR}/Couenne-releases-${COUENNE_VERSION} && \
    ./configure --prefix=/usr/local --enable-static CXX=g++ CC=gcc F77=gfortran && \
    make && \
    make install && \
    cd ${TOOL_DIR} && \
    rm -rf ${TOOL_DIR}/Couenne-releases-${COUENNE_VERSION}

# Install SCIP
COPY scipoptsuite-${SCIP_VERSION}.tgz ${TOOL_DIR}
WORKDIR ${TOOL_DIR}
RUN tar zxvf ${TOOL_DIR}/scipoptsuite-${SCIP_VERSION}.tgz && \
    rm ${TOOL_DIR}/scipoptsuite-${SCIP_VERSION}.tgz && \
    cd ${TOOL_DIR}/scipoptsuite-${SCIP_VERSION} && \
    make ZIMPL=false && \
    make install INSTALLDIR=/usr/local && \
    cd ${TOOL_DIR} && \
    rm -rf scipoptsuite-${SCIP_VERSION}
