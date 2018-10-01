# This commands will be run inside of the container web
# If ANY of this commands fails (return != 0) the container will be down
bash ./docker_scripts/wait_for_postgres.sh
cd src
python manage.py makemigrations degree admission educator uploads course
python manage.py migrate
#python manage.py runserver 0.0.0.0:8000

python manage.py collectstatic
chmod 775 -R adega/static
gunicorn adega.wsgi:application -w 2 -b :8000
