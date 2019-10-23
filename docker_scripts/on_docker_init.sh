# This commands will be run inside of the container web
# If ANY of this commands fails (return != 0) the container will be down
cp config.json src/config.json
bash ./docker_scripts/wait_for_postgres.sh
cd src
python manage.py makemigrations degree admission educator submission course
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
