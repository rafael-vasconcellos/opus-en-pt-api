import time
import requests
from typing import List


def test(text: str): 
    start_time = time.perf_counter()
    response = requests.get(f"http://localhost:7860/api/translate?text={text}")
    print(response.status_code)
    print(response.content)
    end_time = time.perf_counter()
    print(f"Tempo de execução: {end_time - start_time:.4f} segundos")

def test_batch(texts: List[str]): 
    start_time = time.perf_counter()
    response = requests.post("http://localhost:7860/api/translate", json={
        "input_texts": texts
    })
    print(response.status_code)
    print(response.content)
    end_time = time.perf_counter()
    print(f"Tempo de execução: {end_time - start_time:.4f} segundos")


if __name__ == "__main__":
    test("Now let's make my mum's favourite. So three mars bars into the pan. Then we add the tuna and just stir for a bit, just let the chocolate and fish infuse. A sprinkle of olive oil and some tomato ketchup. Now smell that. Oh boy this is going to be incredible.")
    test_batch([
        "Tom tried to stab me.",
        "He has been to Hawaii several times."
    ])


