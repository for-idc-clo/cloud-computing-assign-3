FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY ./requirements.txt /

RUN pip install --upgrade pip && \
    pip install -r /requirements.txt

COPY ./src /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]