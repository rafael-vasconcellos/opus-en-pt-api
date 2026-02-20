---
title: Opus EN to PT Api
emoji: 🐢
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
license: apache-2.0
short_description: An API to translate from EN to PT with the Opus model
---

# Opus EN→PT API

A lightweight FastAPI service that exposes the Opus translation models. The project wraps [Hugging Face Transformers](https://github.com/huggingface/transformers) and provides both single‑sentence and batch endpoints, plus a special compatibility route for the Sugoi Bot defaults.

## Features

- **GET** and **POST** endpoints for translation
- Batch processing with latency control via a semaphore queue
- Model can be adjusted via command‑line argument
- Automatically exposes OpenAPI docs at `/docs`
- Deployable with Docker or plain Python

---

## Quickstart

### Prerequisites

- Python 3.8+
- `pip` installed
- (Optional) CUDA‑capable GPU if using Torch with GPU support

### Install

```bash
$ pip install git+https://github.com/rafael-vasconcellos/opus-en-pt-api
```

### Run the server locally

```bash
$ opus_api
```

By default the API listens on `0.0.0.0:7860`. You can pass a different model with:

```powershell
$ opus_api --model "Helsinki-NLP/opus-mt-tc-big-en-pt"
# or
$ opus_api --m "Helsinki-NLP/opus-mt-tc-big-en-pt"
```

---

## API Endpoints 🔌

All responses are JSON unless otherwise noted. Errors return HTTP status codes with empty bodies.

### `GET /api/translate`

Translate a single string provided as a query parameter.

**Query parameters**

- `text` (string) – the English text to translate.

**Responses**

- `200` – translation result as `{ "translated": "..." }`
- `400` – bad request (missing/empty `text`).

**Example**

```bash
curl "http://localhost:7860/api/translate?text=Hello+world"
```

### `POST /api/translate`

Translate a batch of strings.

**Request body** (JSON)

```json
{
  "input_texts": ["First sentence", "Second sentence"]
}
```

**Responses**

- `200` – array of translated sentences.
- `400` – invalid body or empty list.

**Example**

```bash
curl -X POST http://localhost:7860/api/translate \
  -H "Content-Type: application/json" \
  -d '{"input_texts": ["One", "Two"]}'
```

### `POST /` (Sugoi default)

Special route for compatibility with the Sugoi Bot framework.

**Request body**

```json
{
  "message": "translate sentences",
  "content": ["Sentence A", "Sentence B"]
}
```

This behaves the same as a batch translate. Other messages or missing content return 400.

## Model & performance

The translation logic lives in `opus_api/model.py`. A local cache directory (`./models`) stores
downloaded weights. You may change the model by passing a different Hugging Face ID when starting
`app_uvi.py`.

Batch translation is throttled with a semaphore to avoid GPU/CPU contention; see
`opus_api/translation_queue_semaphore.py`.

## Docker

The provided `Dockerfile` can build a container with the same environment. Example build & run:

```powershell
docker build -t opus-en-pt-api .
docker run -p 7860:7860 opus-en-pt-api
```

## License

Apache‑2.0

---

For additional configuration options when deploying on Hugging Face Spaces, see the [spaces
config reference](https://huggingface.co/docs/hub/spaces-config-reference).
