from threading import BoundedSemaphore
from concurrent.futures import ThreadPoolExecutor
from opus_api.model import run, run_batch
from typing import List



MAX_PARALLEL = 4
sema = BoundedSemaphore(MAX_PARALLEL)
executor = ThreadPoolExecutor(max_workers=MAX_PARALLEL)

def sema_translate(text: str):
    with sema:
        return run(text)

def sema_translate_batch(text_list: List[str]):
    with sema:
        return run_batch(text_list)

async def translate(text: str):
    future = executor.submit(sema_translate, text)
    return [
        200, 
        {
            "translated_text": future.result()
        }
    ]

async def translate_batch(texts: List[str]):
    future = executor.submit(sema_translate_batch, texts)
    return [
        200, 
        {
            "translated_text": future.result()
        }
    ]

async def status(task_id: str): pass


