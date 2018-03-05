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
	apt-get update
	apt-get install -y python3-dev
	apt-get install -y python3-pip
	apt-get install -y libpq-dev
	apt-get install -y postgresql postgresql-contrib
	pip3 install --user -U pip setuptools pipenv
	pipenv install

install-dev: install
	pipenv install --dev

