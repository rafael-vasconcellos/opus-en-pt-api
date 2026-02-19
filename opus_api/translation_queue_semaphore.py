from threading import BoundedSemaphore
from concurrent.futures import ThreadPoolExecutor
from opus_api.model import Opus
from typing import List



MAX_PARALLEL = 4
sema = BoundedSemaphore(MAX_PARALLEL)
executor = ThreadPoolExecutor(max_workers=MAX_PARALLEL)

class Queue:
    model: Opus
    def set_model(self, model_name):
        self.model = Opus(model_name)

    def _sema_translate(self, text: str):
        with sema:
            return self.model.run(text)

    def _sema_translate_batch(self, text_list: List[str]):
        with sema:
            return self.model.run_batch(text_list)

    async def translate(self, text: str):
        future = executor.submit(self._sema_translate, text)
        return [
            200, 
            {
                "translated_text": future.result()
            }
        ]

    async def translate_batch(self, texts: List[str]):
        future = executor.submit(self._sema_translate_batch, texts)
        return [
            200, 
            {
                "translated_text": future.result()
            }
        ]




