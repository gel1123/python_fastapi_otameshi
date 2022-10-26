from fastapi import APIRouter
from transformers import T5Tokenizer, AutoModelForCausalLM
import time

# ---- rinna/japanese-gpt2-medium ----
# https://huggingface.co/rinna/japanese-gpt2-medium
model_path = "models/rinna/japanese-gpt2-medium"
print(f"Loading {model_path}")
before = time.time()
tokenizer = T5Tokenizer.from_pretrained(model_path)
tokenizer.do_lower_case = True
model = AutoModelForCausalLM.from_pretrained(model_path)
after = time.time()
print(f"Loaded {model_path} in {round(after - before, 1)} seconds")

router = APIRouter()


@router.get("/rinna/gpt2", tags=["rinna"])
def gpt2(text: str):
    """
    ## 概要
    引数の文章の後に続く文章を予測する。

    ## 例

    ```sh
    # http://localhost:8080/rinna/gpt2?text=春になればそこかしこに
    curl --get --data-urlencode 'text=春になればそこかしこに' http://localhost:8080/rinna/gpt2
    ```

    上記クエリで下記のような応答が返る。

    ```json
    {"generated_text":"春になればそこかしこに綺麗な花を咲かせていますが、まだつぼみが多い季節なので その姿も華やかです。そんな春の陽気に誘われて行楽地にも出かけたくなるお天気に恵まれました"}
    ```


    """
    # repetition_penaltyを設定して、ループせず最適な文章を出すようにする
    input_ids = tokenizer.encode(text, return_tensors="pt")
    outputs = model.generate(
        input_ids, min_length=10, max_length=50,
        repetition_penalty=2.0, do_sample=True,
        top_k=400, top_p=0.95, num_return_sequences=3,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"generated_text": generated_text}
