FROM python:3.9.15-slim-bullseye
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r  requirements.txt
EXPOSE 8080
ENV PYTHONUNBUFFERED True

# transformersをオフラインで使う前提なので TRANSFORMERS_OFFLINE で強制する
ENV TRANSFORMERS_OFFLINE=1

WORKDIR /app
COPY main.py .

# cp -rf routers . と同じ振る舞いをさせたい時に、例えば
# COPY routers .
# とすると、routersディレクトリの中身がカレントディレクトリに展開されるので、
# 期待と異なることに注意。
COPY routers/ ./routers/
COPY models/ ./models/

# uvicorn main:app --host 0.0.0.0 --port 8080
# ローカルで動作確認するなら --reload オプションをつけると便利。
# またコンテナを用いず動作確認するなら、環境変数の設定が必要なので、下記のように実行すると便利。
# TRANSFORMERS_OFFLINE=1 uvicorn main:app --host 0.0.0.0 --port 8080 --reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
