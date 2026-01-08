FROM python:3.11-slim

WORKDIR /code

COPY . .

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["python", "-u", "main.py"]