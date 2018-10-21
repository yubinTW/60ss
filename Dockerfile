FROM python:3.7

# Install Python and Package Libraries
RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
    net-tools \
    vim

# Project Files and Settings
ARG PROJECT=60ss
ARG PROJECT_DIR=/var/www/${PROJECT}

RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR
COPY . ./

# Server
EXPOSE 8000
STOPSIGNAL SIGINT
RUN chmod +x ./start.sh
RUN pip install pipenv
RUN pipenv install
CMD ./start.sh