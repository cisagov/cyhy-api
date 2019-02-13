FROM python:3.7-alpine
MAINTAINER Mark Feldhousen <mark.feldhousen@trio.dhs.gov>

ARG CISA_UID=421
ARG INSTALL_IPYTHON="Yes Please"
ARG CISA_SRC="/usr/src"
ENV CISA_HOME="/home/cisa"

RUN addgroup -S -g ${CISA_UID} cisa \
  && adduser -S -u ${CISA_UID} -G cisa cisa \
  && mkdir -p ${CISA_HOME} \
  && chown -R cisa:cisa ${CISA_HOME}

RUN apk update
RUN pip install --upgrade pip

RUN if [ -n "${INSTALL_IPYTHON}" ]; then pip install ipython; fi

WORKDIR ${CISA_SRC}

COPY src cyhy_rest
RUN pip install -e cyhy_rest

USER cisa
WORKDIR ${CISA_HOME}
EXPOSE 5000/tcp
ENTRYPOINT ["cyhy-rest-server"]
