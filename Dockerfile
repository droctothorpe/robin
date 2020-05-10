FROM python:3.7-alpine

LABEL maintainer="mythicalsunlight@gmail.com"

ENV FLASK_APP robin.py
ENV FLASK_CONFIG docker

RUN adduser -D robin
USER robin

WORKDIR /home/robin

COPY . .
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT /bin/ash
CMD gunicorn -b :5000 --access-logfile - --error-logfile - robin:app

# RUN apt-get update -y && \
# apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
# COPY ./requirements.txt /app/requirements.txt

# WORKDIR /app

# RUN pip install -r requirements.txt

# COPY . /app

# ENTRYPOINT [ "python" ]

# CMD [ "robin.py" ]