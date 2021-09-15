
Gestão e preenchimento de listas de verificação
-
Criar ambiente
> python3 -m venv venv

Ativar ambiente
> (unix) source venv/bin/activate
> 
> (win) ./venv/scripts/activate.bat

Instalar pacotes
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

Alterar branch
> git checkout -b main
