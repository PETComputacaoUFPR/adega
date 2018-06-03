# This commands will be run inside of the container web
# If ANY of this commands fails (return != 0) the container will be down
bash ./docker_scripts/wait_for_postgres.sh
python ./src/manage.py migrate
python ./src/manage.py runserver 0.0.0.0:8000
