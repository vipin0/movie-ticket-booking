FROM python:3.8.10-alpine
RUN addgroup appuser && adduser -S -G appuser appuser
ENV HOME=/home/appuser
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH $PATH:${HOME}/.local/bin
WORKDIR ${HOME}/app
# ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.8.0/wait /wait
# RUN chmod +x /wait
# CMD [ "./wait" ]
# For postgresql to work
RUN apk update --no-cache && apk add --no-cache --virtual .tmp postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN mkdir media && chown -R appuser:appuser ${HOME}/app
EXPOSE 8000
USER appuser
EXPOSE 8000
