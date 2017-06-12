# BaScouter

*** IMPORTANTE: Las instrucciones aquí dadas han sido probadas en Ubuntu 16.04 LTS. Para otros sistemas operativos
puede variar.

Para su ejecución es necesario tener instalado MySQL 5.7 y Python 3.5 junto con 
los siguientes módulos para éste:

	beautifulsoup4==4.5.3
	coverage==4.3.4
	decorator==4.0.11
	Django==1.10
	django-cachalot==1.4.1
	-e git+https://github.com/APSL/django-cookie-law.git@f6e15bd74c48f9e1e22c65f7edb36bb721590160#egg=django_cookie_law
	django-cookie-message==0.1
	django-countries==4.0
	django-debug-toolbar==1.6
	django-material==0.12.5
	django-registration==2.1.2
	djangorestframework==3.5.4
	ipdb==0.10.1
	ipython==4.0.0
	ipython-genutils==0.1.0
	mysqlclient==1.3.10
	olefile==0.44
	pexpect==4.2.1
	pickleshare==0.7.4
	Pillow==4.0.0
	pkg-resources==0.0.0
	ptyprocess==0.5.1
	python-memcached==1.58
	simplegeneric==0.8.1
	six==1.10.0
	sqlparse==0.2.3
	traitlets==4.3.2

*Nota: Debemos de tener un esquema en MySQL llamado bascouter y establecer las credenciales
correctas en el archivo bascouter/bascouter/settings.py. Para crear el esquema:
	
	mysql> CREATE DATABASE bascouter CHARACTER SET utf8 COLLATE utf8_general_ci;

Cumplidos estos requisitos, para la ejecución de la aplicación introducimos en la terminal
los siguientes comandos:

	> python manage.py makemigrations // migración del modelo de datos
	> python manage.py migrate // replicar migración en la base de datos
	> python manage.py createsuperuser // creamos usuario administrados
	> python manage.py populate_db // Alimentamos la base de datos con los datos extraídos
	
	// Las anteriores operaciones sólo son neceserias la primera vez que ejecutemos la aplicación.

	> python manage.py runserver 

La aplicación puede ser visitada desde la siguiente dirección: http://127.0.0.1:8000/ (puede variar
en función del host).

También puede verse online en la siguiente dirección: www.bascouter.es
