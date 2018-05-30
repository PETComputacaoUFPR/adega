#!/bin/bash
# ---------------- flags -------------------
verbose=0

# ---------- functions ------------------
configure() {
	postgres psql < postgres/create.sql
		
	python3 src/manage.py makemigrations degree
	python3 src/manage.py makemigrations uploads
	python3 src/manage.py makemigrations educator
	python3 src/manage.py makemigrations adega
	python3 src/manage.py migrate
}


function install() {
	PACKAGES="git docker docker-compose"
	declare -A osInfo;
	osInfo[/etc/arch-release]="pacman -S --noconfirm "
	osInfo[/etc/debian_version]="apt-get install -y"
	for f in ${!osInfo[@]}; do
		#verifica se o arquivo $f existe
		if [[ -f $f ]]; then 
			DISTRO=${osInfo[$f]}
		fi
	done	
	sudo $DISTRO $PACKAGES
	if [ ! -d "base_dados" ]; then
		git clone git@gitlab.c3sl.ufpr.br:adega/base_dados.git
	fi
	#docker build  --tag adega .
	docker-compose up
}
function usase() {
	echo -ne "
	Options: 
	-h, --help			imprime ajuda
	-v, --verbose		ativa o verbose
	-i, --install 		instala todas as depedências
	-c, --configure 	realiza a configuração
	
	" 
}
# -------------- main ------------------
if [ $# -gt 0 ]; then
	for argument in $*; do
		case $argument in
			-h |--help) usase ;;
			-i |--install) install ;;
			-c |--configure) configure ;;
			-v |--verbose) verbose=1 ;;
			-d |--deploy) deploy ;;
		esac
		shift
	done
fi
