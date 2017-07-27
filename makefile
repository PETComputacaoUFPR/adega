SITE-OWNER = www-data
SITE-OWNER-GROUP = www-data

all:


clean:
	@rm -rf *~ *.pyc *.backup

clean-deploy: clean
	@rm -rf static db.sqlite3

coverage:
	coverage run --source='.' manage.py test
	coverage html
	xdg-open htmlcov/index.html


docs:
	@echo 'ainda não implementado'


deploy:
	python manage.py migrate
	python manage.py collectstatic -v0 --noinput
	chown $(SITE-OWNER):$(SITE-OWNER-GROUP) -R .

clean-docs:
	@rm -rf docs

install:
	apt-get install -y python3-dev
	apt-get install -y python3-pip
	pip3 install -U pip setuptools
	pip3 install -r requirements.txt

install-dev: install
	pip3 install -r requirements-dev.txt

create-db:
	mysql -u root < configure-db.sql
	python3 manage.py migrate
	
