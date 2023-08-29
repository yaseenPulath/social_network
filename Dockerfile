FROM python:3.10.13

ENV PYTHONUNBUFFERED=1
ENV WAIT_VERSION 2.7.2

WORKDIR /srv/www/social_network

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

RUN mkdir -p /var/log/uwsgi/

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD [ "uwsgi", "--ini", "uwsgi.ini" ]
