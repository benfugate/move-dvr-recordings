FROM python:3.11-slim
COPY ./move_episode.py ./requirements.txt /app/
RUN touch /var/log/copier.log
WORKDIR /app
RUN pip install -r requirements.txt
COPY entrypoint.sh /
CMD ["/bin/sh", "/entrypoint.sh"]