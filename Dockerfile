FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
# download the model
RUN python model.py
EXPOSE 7860


CMD ["uvicorn", "app_uvi:app", "--host", "0.0.0.0", "--port", "7860"]
# uvicorn app_uvi:app --host 0.0.0.0 --port 7860 --reload
#CMD sh -c '{ uvicorn app_uvi:app --host 0.0.0.0 --port 7860 & huey_consumer.py translation_queue.huey & wait; }'

