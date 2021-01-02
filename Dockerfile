FROM python:3.7-buster as builder

COPY ./build /build
WORKDIR /build
RUN apt update -y && apt install -y mecab libmecab-dev mecab-ipadic-utf8 && chmod +x ./generate_user_dict.sh && chmod +x ./generate_user_dict && ./generate_user_dict.sh /tmp/user.dic

FROM python:3.7-slim-buster as runner
RUN apt update -y && apt install -y mecab libmecab-dev mecab-ipadic-utf8 bzip2
COPY ./app /project/app
COPY ./Pipfile ./Pipfile.lock /project/
WORKDIR /project
COPY --from=builder /tmp/user.dic /project/app/dataset
RUN pip install --upgrade pip && pip install pipenv && pipenv install --system --ignore-pipfile --deploy