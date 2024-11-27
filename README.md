# Lambda Dockerのテスト

## 参考文献

コンテナイメージで Python Lambda 関数をデプロイする  
<https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-image.html>

Dockerを活用したLambdaの開発＆本番環境のおすすめ構成  
<https://zenn.dev/konan/articles/efd004b1810463>

AWS Lambda 関数を Docker コンテナを使ってビルド & デプロイ  
<https://qiita.com/sasaco/items/b65ce36c05c50a74ac3e>

pythonのイメージ  
<https://gallery.ecr.aws/lambda/python>

## docker imageの作成とテスト

```bush
docker build --platform linux/amd64 -t docker-lambda:test -f Dockerfile .
docker run --platform linux/amd64 -p 9000:8080 docker-lambda:test
```

別のターミナルから以下のコマンドを実行

```bush
curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```

以下のレスポンスが返ってくる

```bush
"Hello from AWS Lambda using Python3.12.7 (main, Oct 14 2024, 11:21:50) [GCC 11.4.1 20230605 (Red Hat 11.4.1-2)]! librosa version: 0.10.2.post1"
```

## イメージのデプロイ

aws cliのインストール
<https://awscli.amazonaws.com/AWSCLIV2.msi>

```bash
aws --version
aws-cli/2.17.20 Python/3.11.6 Windows/10 exe/AMD64 prompt/off
```

Amazon ECR レジストリに Docker CLI を認証

```bush
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin ○○.dkr.ecr.ap-northeast-1.amazonaws.com
WARNING! Your password will be stored unencrypted in /home/cloudshell-user/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
aws ecr create-repository --repository-name hello-world --region ap-northeast-1 --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
{
    "repository": {
        "repositoryArn": "arn:aws:ecr:ap-northeast-1:○○:repository/hello-world",
        "registryId": "○○",
        "repositoryName": "hello-world",
        "repositoryUri": "○○.dkr.ecr.ap-northeast-1.amazonaws.com/hello-world",
        "createdAt": "2024-11-18T16:22:03.112000+00:00",
        "imageTagMutability": "MUTABLE",
        "imageScanningConfiguration": {
            "scanOnPush": true
        },
        "encryptionConfiguration": {
            "encryptionType": "AES256"
        }
    }
}
```

前のステップの出力から repositoryUri をコピーします。

```bush
docker tag docker-lambda:test ○○.dkr.ecr.ap-northeast-1.amazonaws.com/hello-world:latest
docker push ○○.dkr.ecr.ap-northeast-1.amazonaws.com/hello-world:latest
```

## 開発環境

```bush
# 初回
docker-compose up --build

# ビルドするとき
docker-compose build
```

work以下のファイルを変更したのち、コンテナを再起動すると修正が反映される。
