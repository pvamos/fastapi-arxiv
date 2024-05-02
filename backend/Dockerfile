FROM python:3.12-alpine3.19

WORKDIR /code

COPY ./backend/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
#RUN apk add --no-cache --upgrade bash

COPY ./backend/app /code/app
COPY ./wait-for.sh /code/wait-for.sh
RUN chmod +x /code/wait-for.sh

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

