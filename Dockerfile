FROM python:3.11-slim
RUN apt-get update && apt-get -y install cron --no-install-recommends

COPY ./move_episode.py /app/move_episode.py
COPY ./script-cron /etc/cron.d/script-cron
RUN chmod 0644 /etc/cron.d/script-cron && \
    crontab /etc/cron.d/script-cron
RUN touch /var/log/cron.log

WORKDIR /app
COPY entrypoint.sh /
CMD ["/bin/sh", "/entrypoint.sh"]