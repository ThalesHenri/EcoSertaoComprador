FROM python:3.10 

LABEL maintainer="Dennis"

EXPOSE 8080

RUN mkdir -p /opt/eco-sertao-app
WORKDIR /opt/eco-sertao-app

COPY ecoComprador .
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache -r requirements.txt 

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]