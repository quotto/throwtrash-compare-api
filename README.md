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

python3.7.4

## ビルド・デプロイ手順

1. `pip install -r requirements.txt -t ./package`
2. `./mecab-service/local/libexec/mecab-dict-index -d ./mecab-service/local/lib/mecab/dic/ipadic -u user.dic -f utf-8 -t utf-8 ./user.csv`
3. `zip -r9 ./function.zip mecab-service main.py package`
4. `aws lambda upload-function-code --function-name my-function --zip-file fileb://function.zip`
