from pydoc import doc
from fastapi import APIRouter
from transformers import T5Tokenizer, RobertaForMaskedLM
import torch
import time

# ---- rinna/japanese-roberta-base ----
# https://huggingface.co/rinna/japanese-roberta-base
model_path = "models/rinna/japanese-roberta-base"
print(f"Loading {model_path}")
before = time.time()
tokenizer = T5Tokenizer.from_pretrained(model_path)
tokenizer.do_lower_case = True
model = RobertaForMaskedLM.from_pretrained(model_path)
after = time.time()
print(f"Loaded {model_path} in {round(after - before, 1)} seconds")

router = APIRouter()


@router.get("/rinna/roberta", tags=["rinna"])
def roberta(text: str):
    """
    ## 概要
    引数の文字列に[MASK]があれば、その部分を予測する。

    ## 例

    ```sh
    # http://localhost:8080/rinna/roberta?text=春になればそこかしこに[MASK]が咲きます。
    curl --get --data-urlencode 'text=春になればそこかしこに[MASK]が咲きます。' http://localhost:8080/rinna/roberta
    ```

    上記クエリで下記のような応答が返る。

    ```json
    {"prediction_words":["桜","サクラ","梅","花","さくら","バラ","コスモス","ひまわり","椿"]}
    ```
    """

    text = "[CLS]" + text
    tokens = tokenizer.tokenize(text)
    print("tokens:", tokens)

    # [MASK]の位置を取得
    masked_index = tokens.index("[MASK]")

    token_ids = tokenizer.convert_tokens_to_ids(tokens)
    token_tensor = torch.LongTensor([token_ids])
    position_ids = list(range(0, token_tensor.size(1)))
    position_id_tensor = torch.LongTensor([position_ids])
    with torch.no_grad():
        outputs = model(input_ids=token_tensor,
                        position_ids=position_id_tensor)
        predictions = outputs[0][0, masked_index].topk(10)

    # 予測結果を表示する。
    # なおその際、下記をおこなっている。
    # - 単語から "_" を除去する
    # - 候補から "<unk>" を除外する
    # - 重複を除去する
    prediction_words = list(dict.fromkeys([
        tokenizer.convert_ids_to_tokens([index_t.item()])[0].replace("▁", "")
        for index_t in predictions.indices
        if tokenizer.convert_ids_to_tokens([index_t.item()])[0] != "<unk>"
    ]))
    return {"prediction_words": prediction_words}
