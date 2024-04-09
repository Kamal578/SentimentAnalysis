FROM python:3.10.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["hypercorn", "main:app", "--bind", "0.0.0.0:8000"]

# build: docker build -t my-fastapi-app .
# run: docker run -d -p 8000:8000 my-fastapi-app