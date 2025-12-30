import time, sys
from transformers import MarianMTModel, MarianTokenizer
from typing import List



src_text_test1 = [
    ">>por<< Tom tried to stab me.",
    ">>por<< He has been to Hawaii several times."
]

src_text_test2 = "Now let's make my mum's favourite. So three mars bars into the pan. Then we add the tuna and just stir for a bit, just let the chocolate and fish infuse. A sprinkle of olive oil and some tomato ketchup. Now smell that. Oh boy this is going to be incredible."

def get_prompt(text_list: List[str]):
    return [f">>por<< {text}" for text in text_list]

model_name = "Helsinki-NLP/opus-mt-tc-big-en-pt"
local_dir = "./models"
tokenizer = MarianTokenizer.from_pretrained(model_name, cache_dir=local_dir)
model = MarianMTModel.from_pretrained(model_name, cache_dir=local_dir)

def run(text: str):
    prompt = get_prompt([ text ])
    translated = model.generate(**tokenizer(prompt, return_tensors="pt", padding=True))
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    #print(translated_text)
    return translated_text

def run_batch(text_list: List[str]):
    prompt = get_prompt(text_list)
    translated = model.generate(**tokenizer(prompt, return_tensors="pt", padding=True))
    return tokenizer.decode(translated, skip_special_tokens=True)

if __name__ == "__main__":
    if "-test" in sys.argv:
        start_time = time.perf_counter()
        print(run(src_text_test2))
        end_time = time.perf_counter()
        print(f"Tempo de execução: {end_time - start_time:.4f} segundos")


