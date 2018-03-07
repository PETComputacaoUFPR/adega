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
	apt-get update
	apt-get install -y python3-dev
	apt-get install -y python3-pip
	apt-get install -y libpq-dev
	apt-get install -y postgresql postgresql-contrib
	pip3 install --user -U pip setuptools pipenv==9.0.3
	pipenv install

install-dev: install
	pipenv install --dev

