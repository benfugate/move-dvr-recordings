FROM python:3.11-slim
COPY ./src /app
RUN touch /var/log/copier.log
COPY requirements.txt entrypoint.sh /
RUN apt-get update && \
    apt-get install -y --no-install-recommends gosu && \
    rm -rf /var/lib/apt/lists/* && \
    pip install -r requirements.txt && \
    rm requirements.txt && \
    chmod +x /entrypoint.sh
WORKDIR /app
CMD ["/bin/sh", "/entrypoint.sh"]