
Gestão e preenchimento de listas de verificação
-
Criar ambiente
> python3 -m venv venv

Ativar ambiente
> (unix) source venv/bin/activate
> 
> (win) ./venv/scripts/activate.bat

Instalar pacotes
> pip install -r requirements.txt
> 
> ou individualmente
>
> pip install Django
> 
> pip install django-widget-tweaks
> 
> pip install django-filter
> 
> pip install django-extensions

Conector postgreSQL
> (unix) pip install psycopg2-binary
> 
> (win) pip install psycopg2

Criar projeto Django
-
> django-admin startproject checklist

Criar Django admin
> python manage.py createsuperuser

Migrations
> python manage.py makemigrations checklist
> 
> python manage.py migrate checklist

Executar servidor de testes
> python manage.py runserver localhost:5000

SSH - github

> https://gist.github.com/xirixiz/b6b0c6f4917ce17a90e00f9b60566278

GIT
-
Criar novo repositorio
>  git init

Exibir status dos arquivos alterados
> git status

Alterar branch
> git checkout -b main

Adicionar arquivo ao indice ou para atualizacao no repositorio remoto
> git add exemplo.txt

Commit - confirmar alteracoes
> git commit -m "DESCRIBE COMMIT IN A FEW WORDS"

Push - envia as alteracoes para o repositorio remoto
> git push

Pull (Pull, fetch)
> git pull
