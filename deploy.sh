#!/usr/bin/bash


(cd src; python manage.py collectstatic)


if ! sudo -u postgres psql adega
then
    sudo -u postgres psql < postgres/create.sql
fi


python manage.py migrate




