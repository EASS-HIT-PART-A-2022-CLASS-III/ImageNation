FROM python:3.9

WORKDIR /myImages

COPY ./requirements.txt myImages/requirements.txt

RUN pip install --no-cache-dir --upgrade -r myImages/requirements.txt

COPY . /myImages/app

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8800"]