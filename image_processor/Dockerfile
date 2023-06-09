FROM python:3.10

WORKDIR /ImageNation/image_processor

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8801

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8801","--reload"]

