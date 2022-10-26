## これは何？

PythonのWebフレームワーク `FastAPI` に rinna社が公開する学習済みモデルを載せて動かすデモだよ。

ローカルでの開発＆動作確認は、VSCodeのリモートコンテナで出来るように devcontainer.json を構成しているよ。

実運用には、Google Cloud Run で動かすことを想定した Dockerfile を構成しているよ。
`deploy.example.sh` を参考に、自分のGCPプロジェクト向けにデプロイするシェルスクリプトを作成してね。

## 環境構築

Dockerで動かす前提だけど、その前にrinna社が公開している学習済みモデルを別のリポジトリから取得する必要があるよ。
だからそのために、まずはローカルで下記を実行してね。

```sh
./setup_models.sh
```

上記スクリプトにより、rinna社が公開している学習済みモデルを git clone で取得し、modelsディレクトリ配下に配置されるよ。これによりcloneした学習済みモデルを、オフラインでFastAPIが参照出来るようになるからね。

## 動作確認の方法

### ローカル（コンテナなし）で動作確認

コンテナを用いずローカル環境そのままで動作確認するなら、 `pip3 install --no-cache-dir -r  requirements.txt` で requirements.txt 記載のパッケージをインストールしてから、下記で uvicorn を起動してね。

```sh
TRANSFORMERS_OFFLINE=1 uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### VSCodeリモートコンテナで動作確認

読み込むモデルによっては重すぎてVSCodeリモートコンテナ上でうまく動作しないよ。具体的には、 `rinna/japanese-gpt-1b` とかは筆者環境では動かせなかった。

でも、`setup_models.sh` で現在 git clone させているモデルなら、いずれもコンテナ上で動くと思う。

VSCodeリモートコンテナで動かすなら、環境変数の指定は（Dockerfileで指定しているので）不要だよ。だから uvicorn を下記のように起動すれば動作確認できるからね。

```sh
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

## 環境構築中のメモ

### VSCodeリモートコンテナ起動後に自動でuvicornを動かしたいけど、単に postAttachCommand で `uvicorn main:app --host 0.0.0.0 --port 8080 --reload` を実行すると、 `Configuring Dev Server` がくるくる回り続けてしまうのが気になる

気にせず使うか、あるいはそもそも uvicorn の起動は postAttachCommand 等を使わず手動で行うのが良さそう。

もし気になる（かつ uvicorn をどうしてもVSCodeリモートコンテナ起動時に自動で立ち上げたい）なら、下記のように書けば、思った通りに動いてくれるはずだよ。

```js
{
  // ---- 中略 ----
  // バックグラウンドでuvicorn起動
  "postStartCommand": "nohup bash -c 'uvicorn main:app --host 0.0.0.0 --port 8080 --reload &'",
  // ターミナルで `Done. Press any key to close the terminal.` と聞かれるのを自動で飛ばす
  "postAttachCommand": "bash"
}
```

なお今回は上記を採用せず、VSCodeリモートコンテナの作業時には、都度自分でuvicornを起動させる方針としたよ。
（バックグラウンドで立ち上がるが故にuvicornのログが標準出力に出てこないのが使いにくいから）

#### 参考

- https://stackoverflow.com/questions/67800417/how-to-auto-start-node-server-after-creating-vs-code-development-container
- https://stackoverflow.com/questions/67591024/vscode-remote-container-open-user-terminal-after-postcommand
