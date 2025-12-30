from fastapi import FastAPI
from fastapi.responses import Response, RedirectResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from translation_queue import translate, translate_batch, status
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
        task = translate(input_text)
        #print(type(task)); print(dir(task))
        status_code, result = await status(task.id)
        return JSONResponse(status_code=status_code, content=result)
    return Response(status_code= 400)


@app.post('/api/translate')
async def translate_post(request_body: PostRequestBody):
    if isinstance(request_body.input_texts, list) and len(request_body.input_texts):
        task = translate_batch(request_body.input_texts)
        status_code, result = await status(task.id)
        return JSONResponse(status_code=status_code, content=result)
    return Response(status_code= 400)


@app.get('/api/translate/<task_id>')
async def task_id(task_id: str):
    status_code, result = await status(task_id)
    return JSONResponse(status_code=status_code, content=result)


""" @app.post('/')
async def default_post(request_body: DefaultSugoiRequestBody):
    if isinstance(request_body.content, list) and len(request_body.content) and request_body.message == "translate sentences":
        task_id = str(uuid.uuid4())
        redis_client.lpush(queue_key, json.dumps({
            "id": task_id,
            "input": request_body.content
        })) # left push
        result = query_translation(task_id)
        if result is not None: return { "translations": ast.literal_eval(result) }
        else: return JSONResponse(status_code= 529, content={"error": "Server overloaded"})
    return Response(status_code= 400) """




