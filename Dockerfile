FROM python:3.12-slim

ENV PYTHONUNBUFFERED True

RUN apt-get update && \
    apt-get install -y

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8083

CMD ["python", "manage.py", "runserver", "8083"]