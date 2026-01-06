import os, uvicorn
from threading import Thread

from fastapi import FastAPI
from fastapi.responses import Response, RedirectResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from opus_api.translation_queue_semaphore import translate, translate_batch, status
from typing import List



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

class PostRequestBody(BaseModel):
    input_texts: List[str]

class DefaultSugoiRequestBody(BaseModel):
    message: str
    content: List[str]

#app.mount("/assets", StaticFiles(directory=DIST_DIR / "assets"), name="assets")
#app.mount("/public", StaticFiles(directory=DIST_DIR / "public"), name="public")


@app.get("/")
async def home():
    #return FileResponse(DIST_DIR / "index.html")
    return RedirectResponse(url="/docs")

@app.get('/api/translate')
async def translate_get(text: str):
    input_text = text
    if isinstance(input_text, str) and len(input_text) > 0:
        status_code, result = await translate(input_text)
        return JSONResponse(status_code=status_code, content=result)
    return Response(status_code= 400)


@app.post('/api/translate')
async def translate_post(request_body: PostRequestBody):
    if isinstance(request_body.input_texts, list) and len(request_body.input_texts):
        status_code, result = await translate_batch(request_body.input_texts)
        return JSONResponse(status_code=status_code, content=result)
    return Response(status_code= 400)


@app.post('/')
async def sugoi_default_post(request_body: DefaultSugoiRequestBody):
    if isinstance(request_body.content, list) and len(request_body.content) and request_body.message == "translate sentences":
        status_code, result = await translate_batch(request_body.content)
        return JSONResponse(status_code=status_code, content=result)
    return Response(status_code= 400)


""" @app.get("/api/translate/{task_id}")
async def task_id(task_id: str):
    status_code, result = await status(task_id)
    return JSONResponse(status_code=status_code, content=result) """

#Thread(target=lambda: os.system("huey_consumer opus_api.translation_queue_huey.huey --workers 4"), daemon=True).start()


def main():
    uvicorn.run("opus_api.app_uvi:app", host="0.0.0.0", port=7860, reload=False)

if __name__ == "__main__":
    main()


