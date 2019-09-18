 #Pre-built alpine docker image with nginx and python3 installed
FROM tiangolo/uwsgi-nginx:python3.7

# web ports
ENV LISTEN_PORT=8000
EXPOSE 8000

# mysqlclient
#RUN apk add mariadb-dev build-base
#RUN sudo apt-get install libmysqlclient-dev
RUN apt-get install default-libmysqlclient-dev

# Indicate where uwsgi.ini lives
ENV UWSGI_INI uwsgi.ini

# Copy the app files to a folder and run it from there
WORKDIR /app
ADD . /app

RUN chmod g+w /app

RUN pip install --upgrade pip
# Make sure dependencies are installed
RUN python -m pip install -r requirements.txt