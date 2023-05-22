FROM python:3.10

WORKDIR /myImages/app/frontend

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD [ "streamlit","run","Home.py"]

