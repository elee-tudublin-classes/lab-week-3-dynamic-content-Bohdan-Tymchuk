#FROM ubuntu:latest
#LABEL authors="TEST1"
#
#ENTRYPOINT ["top", "-b"]
#

FROM python:3.12-slim

WORKDIR /app

#COPY .env .env

COPY . .


RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]


#docker build -t fastapi-app .
#docker run --env-file .env -d -p 8000:80 fastapi-app