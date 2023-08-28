FROM python:3.10.13
ENV PYTHONUNBUFFERED=1
WORKDIR /srv/www/social_network

RUN mkdir -p /var/log/uwsgi/

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD [ "uwsgi", "--ini", "uwsgi.ini" ]
