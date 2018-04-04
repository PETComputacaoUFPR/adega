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


## Instalação e dependências


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
