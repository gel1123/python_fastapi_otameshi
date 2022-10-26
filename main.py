import routers
from fastapi import FastAPI
from os import environ

# transformers をオフラインで使う前提
assert environ["TRANSFORMERS_OFFLINE"] == "1"

# 別ファイルに定義した各ルートを登録する。
# さらにFastAPIはデフォルトで、下記のドキュメントルートを生成してくれる。
# - /docs : Swagger UI 形式のドキュメント
# - /redoc : ReDoc 形式のドキュメント
app = FastAPI()
app.include_router(routers.rinna.roberta.router)
app.include_router(routers.rinna.gpt2.router)
