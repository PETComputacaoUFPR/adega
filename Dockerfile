FROM python:3.5
Run apt-get update -qq
Run apt-get install -y \
	python3-pip libpq-dev \ 
	postgresql-client 
Run mkdir /adega
WORKDIR /adega
ADD . /adega
Run pip3 install -r requirements.txt
run ./install.sh --configure
