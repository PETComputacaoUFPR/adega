#!/bin/bash
# ---------------- flags -------------------
verbose=0

# ---------- functions ------------------
configure() {
	postgres psql < ../postgres/create.sql
		
	python3 manage.py makemigrations degree
	python3 manage.py makemigrations uploads
	python3 manage.py makemigrations educator
	python3 manage.py makemigrations adega
	python3 manage.py migrate
}


install() {
	
	if [ ! -d "base_dados" ]; then
		git clone git@gitlab.c3sl.ufpr.br:adega/base_dados.git
	fi
	docker build  -t adega .
}
usase() {
	echo -e "Options:\n
	\t-h, --help\t print this menu\n"



}
# -------------- main ------------------
while [[ $1 = -?* ]]; do
		case $1 in
			-i | --install) install ;;
			-c | --configure) configure ;;
			-v | --verbose) verbose=1 ;;
			-h | --help) usase ;;
		esac
