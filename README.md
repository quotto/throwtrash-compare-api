# MecabApi

AWS Lambdaで動作させることを前提としたAPIバックエンド

## 構成要素

- コンパイル済みのMecabバイナリ
- ipadic辞書
- ユーザー辞書の元となるcsv
- APIバックエンド用のpythonコードおよびテストコード

## 前提環境

### Mecabバイナリのコンパイル環境

Amazon Linux2のAMIを使用しているためユーザー辞書の生成もそれに準じた環境を想定する。

[amzn-ami-hvm-2018.03.0.20181129-x86_64-gp2](https://console.aws.amazon.com/ec2/v2/home#Images:visibility=public-images;search=amzn2-ami-hvm-2.0.20190313-x86_64-gp2)

### Pythonバージョン

python3.11

## ビルド

### Dockerfile

Dockerによるビルドを行う

1. `app/dataset`にword2vecのモデルファイルを`word2vec.gensim.model`の名前で準備しておく。
2. `docker build -f build/Dockerfile -t throwtrash-compare:prebuild .`
3. `docker build -f Dockerfile .`
