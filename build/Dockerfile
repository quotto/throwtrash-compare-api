ARG FUNCTION_DIR="/function"

FROM python:3.11-buster as builder

ARG FUNCTION_DIR

RUN pip install --target ${FUNCTION_DIR} awslambdaric
ENV APP_DIR=${FUNCTION_DIR}/app
RUN mkdir -p ${APP_DIR}
COPY ./app ${APP_DIR}/

COPY ./build /build
WORKDIR /build
RUN apt update -y && apt install -y mecab libmecab-dev mecab-ipadic-utf8 awscli
RUN /usr/lib/mecab/mecab-dict-index -d /usr/share/mecab/dic/ipadic -u ${APP_DIR}/dataset/user.dic -f utf-8 -t utf-8 /build/user.csv
RUN bzip2 -d ${APP_DIR}/dataset/word2vec.gensim.model.tar.bz2 && tar -xvf ${APP_DIR}/dataset/word2vec.gensim.model.tar -C ${APP_DIR}/dataset && rm ${APP_DIR}/dataset/word2vec.gensim.model.tar
RUN pip install pandas && python swap_taigigo.py ${APP_DIR}/dataset/taigigo.csv

FROM python:3.11-slim-buster as runner

ARG FUNCTION_DIR

ENV APP_DIR=${FUNCTION_DIR}/app
ENV FUNCTION_DIR=${FUNCTION_DIR}
ENV MECABRC=/etc/mecabrc

RUN apt update -y && apt install -y mecab libmecab-dev mecab-ipadic-utf8 bzip2

COPY ./Pipfile ./Pipfile.lock /tmp/
WORKDIR /tmp
RUN pip install --upgrade pip && pip install pipenv && pipenv install --system --ignore-pipfile --deploy
COPY --from=builder ${FUNCTION_DIR} ${FUNCTION_DIR}

WORKDIR ${FUNCTION_DIR}
