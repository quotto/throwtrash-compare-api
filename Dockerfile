FROM python:3.7-buster as builder

COPY ./build /build
WORKDIR /build
RUN apt update -y && apt install -y mecab libmecab-dev mecab-ipadic-utf8 && chmod +x ./generate_user_dict.sh && ./generate_user_dict.sh /tmp/user.dict

FROM python:3.7-slim-buster as runner
COPY ./app /project/app
COPY ./Pipfile ./Pipfile.lock /project/
WORKDIR /project
COPY --from=builder /tmp/user.dict /project/app/dataset
RUN apt update -y && apt install -y mecab libmecab-dev mecab-ipadic-utf8 && pip install --upgrade pip && pip install pipenv && pipenv install --system --ignore-pipfile --deploy