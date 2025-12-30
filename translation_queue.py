import time, os
import asyncio
from huey import SqliteHuey
from model import run, run_batch
from typing import List


os.makedirs('mydb', exist_ok=True)
huey = SqliteHuey(filename='mydb/queue.db')

@huey.task()
def translate(text: str):
    return run(text)

@huey.task()
def translate_batch(text_list: List[str]):
    return run_batch(text_list)

async def status(task_id: str):
    timeout = 30  # segundos max esperando
    check_interval = 1  # checagens

    start = time.time()
    while time.time() - start < timeout:
        result = huey.result(task_id, preserve=False)
        #print(type(result))
        if result is not None:
            return [200, {
                "id": task_id, 
                "status": "done", 
                "result": result
            }]

        await asyncio.sleep(check_interval)

    # se passou do timeout, manda que ainda tá rolando
    return [202, {
        "id": task_id, 
        "status": "pending",
    }]


