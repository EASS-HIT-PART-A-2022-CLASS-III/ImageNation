FROM python:3.10

WORKDIR /ImageNation/backend/

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8800

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8800","--reload"]