# pull official base image
FROM python:3.7.0

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

WORKDIR /Health_Care_WebApp 

# run gunicorn
CMD gunicorn Health_Care_WebApp.wsgi --bind 0.0.0.0:$PORT --workers 4