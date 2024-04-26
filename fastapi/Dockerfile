FROM python:3.12-alpine3.19

WORKDIR /code

COPY ./fastapi/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN apk add --no-cache --upgrade bash

COPY ./fastapi/app /code/app
COPY ./wait-for-it.sh /code/wait-for-it.sh
RUN chmod +x /code/wait-for-it.sh

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

