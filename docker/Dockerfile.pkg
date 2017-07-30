FROM tesseractshadow/tesseract4cmp

RUN ${SCRIPTS_DIR}/repos_update.sh
RUN ${SCRIPTS_DIR}/compile_leptonica.sh
RUN ${SCRIPTS_DIR}/compile_tesseract.sh
RUN ${SCRIPTS_DIR}/build_deb_pkg.sh

VOLUME /pkg
CMD cp ${PKG_DIR}/* /pkg/