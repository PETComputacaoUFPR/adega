# ADEGA


Este software faz parte de um projeto do PET Computação UFPR para 
análise de dados dos cursos de graduação da UFPR. Veja a [wiki](http://gitlab.c3sl.ufpr.br/adega/adega/wikis/home).


## Versão
0.0.0



## Obtendo os códigos


Os códigos fonte do projeto estão disponíveis publicamente no [gitlab]
(gitlab.c3sl.ufpr.br/pet/adega).

E podem ser clonado com o comando

```bash
$ git clone git@gitlab.c3sl.ufpr.br:adega/adega.git
```
## Instalação e dependências com docker

Para executar o projeto com o docker, siga os seguintes passos:
```bash
$ git clone git@gitlab.c3sl.ufpr.br:adega/adega.git # Comando já executado
$ cd adega/
$ sudo make docker-install # Instala o docker.io e docker-compose
$ sudo make docker-up # Executa os containers postgres e webserver
```

## Desenvolvimento com o docker

### Dependências
Docker >=1.13.1


Docker-compose >=1.21.2

#### Possíveis erros:
*1*: O docker-compose padrão nos repositórios podem não conter a versão mais recente. Caso a etapa de instalação não funcione, consulte a [referência dos desenvolvedores](https://github.com/docker/compose/releases).


*2*: Seu computador pode ter problemas ao configurar o DNS. Neste caso, erros parecidos como os a seguir irão acontecer:
```bash
E: Unable to locate package python3-pip
E: Unable to locate package postgresql-client
```


Neste caso, consulte [este tutorial](https://development.robinwinslow.uk/2016/06/23/fix-docker-networking-dns/) para resolver o problema.


### Uso
Enquanto o `sudo make docker-up` estiver sendo executado, as alterações feitas nos arquivos do projeto serão compartilhadas com os arquivos do container docker. Ou seja, é possível alterar qualquer arquivo do projeto e haverá resultados em tempo real.


Assim como é possível realizar qualquer comando como seria feito no com o manage.py, também é possível por meio do comando `sudo make docker-manage`. Por exemplo:
```bash
$ sudo make docker-manage makemigrations uploads
$ sudo make docker-manage migrate
$ sudo make docker-manage createsuperuser
```

Para realizar esses comandos, certifique-se que o comando `make docker-up`está em execução (recomenda-se deixar uma aba no terminal para isso).

## Recomendações para o docker
É recomendado que o usuário configure o docker para que o mesmo possa ser executado sem necessidades de privilégios de superusuário, assim não haverá necessidade do uso de `sudo`. Caso contrário, os comandos realizados com `sudo make` poderão criar arquivos cujo proprietário é o usuário `root`. Caso a recomendação não for seguida, o seguinte comando irá alterar o proprietário dos arquivos para o usuário atual:
```bash
$ sudo make docker-fix
```

## Remover os containers + banco de dados
Para apagar os containers e o banco de dados, execute o seguinte comando:
```bash
$ sudo make docker-remove-all
```
*Observação*: Esse comando **não** irá deletar qualquer arquivo do projeto / diretório local, apenas os containers.   

## Instalação e dependências manuais (não recomendado)


```bash
sudo make install
make install-user
pipenv install --dev
```

Criar o banco de dados postgres

```
sudo -u postgres psql < postgres/create.sql
```


se você possui o arquivo do banco de dados compartilhado internamente pelos 
desenvolvedores do projeto coloque-o na home do projeto, ele vem com um usuário 
`pet` com senha `pet` pré-configurado para testes.


se você não possui o arquivo rode

```bash
python manage.py migrate
python manage.py createsuperuser
```


## Executando o projeto

Por padrão ele irá rodar no 127.0.0.1:8000, ative o virtualenv antes
```bash
pipenv shell
python manage.py runserver
```

Se estiver usando o cloud9 use o ip e a porta que ele libera, assim:
```bash
pipenv shell
python manage.py runserver $IP:$PORT
```

Então acesse pela url fornecida

Ao sair do projeto execute `exit` para sair do virtualenv e evitar polui-lo

## Transformando o seu usuário em um professor

Após você logar no sistema com o seu super usuário você terá acesso ao `URL_DO_SITE/admin`, graças ao [Django admin](https://docs.djangoproject.com/en/1.10/ref/contrib/admin/) nesta tela você é capaz de gerenciar os dados salvos nas models do projeto.   
Para transformar o seu usuário em professor basta clicar em `professor`e então selecionar o seu usuário e o curso. Agora se você voltar para a página inicial do sistema você deve ver uma listagem dos seus cursos. 


## Gerar diagrama do projeto

Basta executar:
```bash
python manage.py graph_models -a -o diagrama.png
```

### Entendendo as dependências do projeto:

* [Django](https://www.djangoproject.com/) - Framework base. Trata a requisição dos clientes e chama as devidas rotinas.
* [Bootstrap](http://getbootstrap.com/) - Framework css. Usamos os seus componentes para deixar as telas bonitas
* [Charts.js](http://www.chartjs.org/) - Biblioteca javascript para desenhar gráficos.
* [Pandas](http://pandas.pydata.org/) - usada para importação dos dados
* [django-extensions](https://django-extensions.readthedocs.io/en/latest/) - Várias extensões para o django. Estamos usando para gerar o diagrama do projeto.


## Contato


Email - pet@inf.ufpr.br

Facebook - pt-br.facebook.com/petcompufpr
