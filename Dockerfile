FROM python:3.5
RUN apt-get update -qq
RUN apt-get install -y \
	python3-pip libpq-dev \ 
	postgresql-client 

RUN mkdir /adega
WORKDIR /adega

# Not necessary (only do the build slow)
# ADD . /adega

ADD requirements.txt /adega/requirements.txt

RUN pip3 install -r requirements.txt

# Not necessary. The migrate can be done by makefile or in docker-compose.yml
# Besides that, there is no database to migrate yet (while docker build)
# RUN ./install.sh --configure
