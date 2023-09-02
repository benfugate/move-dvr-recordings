FROM python:3.11-slim
COPY ./src /app
RUN touch /var/log/copier.log
COPY requirements.txt entrypoint.sh /
RUN pip install -r requirements.txt && \
    rm requirements.txt
WORKDIR /app
CMD ["/bin/sh", "/entrypoint.sh"]