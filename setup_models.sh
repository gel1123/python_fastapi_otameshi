#!/bin/bash

# このスクリプトを配置したディレクトリに移動
cd "$(dirname "$0")"

# ---- 前提 ----
# 学習済みモデルは基本的にサイズが大きく、100MBを超えるので git lfs が必要。
# なければ、Macなら brew install git-lfs などでインストールしておく。
git lfs install

# ---- rinna/japanese-roberta-base ----
mkdir -p models/rinna/japanese-roberta-base
git clone --depth 1 https://huggingface.co/rinna/japanese-roberta-base models/rinna/japanese-roberta-base

# ---- rinna/japanese-gpt2-medium ----
mkdir -p models/rinna/japanese-gpt2-medium
git clone --depth 1 https://huggingface.co/rinna/japanese-gpt2-medium models/rinna/japanese-gpt2-medium

# ---- 補足 ----
# 単に各モデルの最新版を利用したいだけなので、
# 上記で git clone コマンドに depth オプションに 1 を指定している。
#
# depthオプションは git clone 時に取得する履歴の数を指定するものであり、
# --depth 1 なら、最新の 1 件の履歴だけを取得する。
#
# このように --depth 1 でサイズを抑えた git clone のことを
# 一般に shallow clone と呼ばれている。

echo "Done."
