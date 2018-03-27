#!/usr/bin/bash


(cd src; python manage.py collectstatic)

mv src/static .


if ! sudo -u postgres psql adega
then
	sudo -u postgres psql < postgres/create.sql
fi


python manage.py migrate

sudo -u postgres psql < postgres/harden.sql



