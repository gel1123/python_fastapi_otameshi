#!/bin/bash

# このスクリプトを配置したディレクトリに移動
cd "$(dirname "$0")"

# 認証しないと後でDockerイメージをpusuするときに下記のエラーが出る
#  - You don't have the needed permissions to perform this operation, and you may have invalid credentials.
gcloud auth configure-docker

GCP_PROJECT_ID='[GCP Project ID]'
DOCKER_IMAGE_NAME='python-fastapi-otameshi'
VERSION='latest'

# キャッシュを使いたくなければ --no-cache オプションをつける
#
# また、使っているPCが M1Mac なら --platform linux/amd64 オプションをつけないと、
# CloudRun にアップロードしたときに下記のエラーが生じるはず
#
# ````
# terminated: Application failed to start: Failed to create init process: failed to load /usr/local/bin/uvicorn: exec format error
# ```
#
# 参考： https://stackoverflow.com/questions/66127933/cloud-run-failed-to-start-and-then-listen-on-the-port-defined-by-the-port-envi
docker build --platform linux/amd64 --tag asia.gcr.io/${GCP_PROJECT_ID}/${DOCKER_IMAGE_NAME}:${VERSION} .

docker push asia.gcr.io/${GCP_PROJECT_ID}/${DOCKER_IMAGE_NAME}:${VERSION}
gcloud iam service-accounts create pfo-account --project $GCP_PROJECT_ID

# 東京リージョンにデプロイする（未認証でのアクセスを許可）
gcloud run deploy python-fastapi-otameshi \
  --image asia.gcr.io/${GCP_PROJECT_ID}/${DOCKER_IMAGE_NAME}:${VERSION} \
  --service-account pfo-account \
  --allow-unauthenticated \
  --region=asia-northeast1 \
  --cpu 2 \
  --memory 8Gi \
  --project $GCP_PROJECT_ID
