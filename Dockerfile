FROM python:3.9.12-slim-b



# Install dependancies
RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/* 


WORKDIR /app


COPY boot.sh /
RUN chmod +x /boot.sh

ADD Requirements.txt /app/Requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r Requirements.txt

ADD . /app
RUN echo "${VERSION}" > version


EXPOSE 80
ENV WORKERS 1
ENV THREADS 1
ENV TIMEOUT 3000

CMD ["/boot.sh"]