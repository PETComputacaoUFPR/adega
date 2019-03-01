SITE-OWNER = www-data
SITE-OWNER-GROUP = www-data

all:


clean:
	@rm -rf *~ *.pyc *.backup

clean-deploy: clean
	@rm -rf static db.sqlite3

coverage:
	(cd src; coverage run --source='.' manage.py test; coverage html)
	mv src/htmlcov .


docs:
	@echo 'ainda não implementado'


deploy:
	python manage.py migrate
	python manage.py collectstatic -v0 --noinput
	chown $(SITE-OWNER):$(SITE-OWNER-GROUP) -R .

clean-docs:
	@rm -rf docs

install:
	apt-get update -qq
	apt-get install -y python3-dev python3-pip libpq-dev postgresql postgresql-contrib

install-user:
	pip3 install --user -U pip setuptools pipenv==9.0.3
	pipenv install


# TODO: Create the files in docker with $USER owner	
docker-fix:
	chown -R $USER:$USER *

docker-up:
	docker-compose --project-directory . -f docker_scripts/docker-compose.yml -p adega up

docker-production:
	docker-compose --project-directory . -f docker_scripts/docker-production.yml -p adega up

docker-remove-all:
	docker rm adega_web adega_db
	docker rmi adega_web


# Maybe this will not works in all OS systems
docker-install:
	apt-get install docker
	apt-get install docker-compose


# The follows commands permit to use manage.py with make. Examples:
# make docker-manage migrate
# make docker-manage makemigrations uploads

%:
	@:
args = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`


docker-manage:
	@echo $(call args,"")
	docker exec -it adega_web bash -c "cd src; python3 manage.py $(call args,'')"  
	

