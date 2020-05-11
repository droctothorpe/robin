FROM python:3.7-alpine

LABEL maintainer="mythicalsunlight@gmail.com"

ENV FLASK_APP robin.py
ENV FLASK_CONFIG docker

RUN adduser -D robin
USER robin

WORKDIR /home/robin

COPY --chown=robin:1000 . .
# COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install -r requirements/docker.txt

# COPY app app
# COPY migrations migrations
# COPY robin.py config.py boot.sh ./

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]