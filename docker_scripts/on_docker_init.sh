bash ./docker_scripts/wait-for-postgres.sh
python ./src/manage.py migrate
python ./src/manage.py runserver 0.0.0.0:8000
