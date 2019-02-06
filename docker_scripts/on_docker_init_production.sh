# This commands will be run inside of the container web
# If ANY of this commands fails (return != 0) the container will be down
bash ./docker_scripts/wait_for_postgres.sh
cd src
python manage.py makemigrations degree admission educator submission course
python manage.py migrate

python manage.py collectstatic --noinput
#chmod 775 -R adega/static
#python manage.py runserver 0.0.0.0:8000
gunicorn adega.wsgi:application --workers 2 --timeout 600 -b :8000
