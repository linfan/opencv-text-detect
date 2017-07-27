FROM ubuntu:16.04

ADD pkg/*.deb /pkg/

RUN apt-get update && \
    apt-get install -y python3 \
                       python3-pip \
                       libpng12-dev \
                       libjpeg8-dev \
                       libtiff5-dev \
                       zlib1g-dev \
                       gdebi-core && \
    gdebi -n /pkg/libjpeg62-turbo_*.deb && \
    gdebi -n /pkg/libwebp6_*.deb && \
    gdebi -n /pkg/libgif7_*.deb && \
    gdebi -n /pkg/liblept5_*.deb && \
    gdebi -n /pkg/libleptonica-dev_*.deb && \
    gdebi -n /pkg/leptonica-latest_*.deb && \
    gdebi -n /pkg/tesseract-latest_*.deb

RUN pip3 install opencv-python opencv-contrib-python flask
ENV LD_LIBRARY_PATH /usr/local/lib:/usr/lib:/lib:/lib64
