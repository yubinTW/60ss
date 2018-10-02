#/bin/bash
pipenv run python web60ss/manage.py makemigrations
pipenv run python web60ss/manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'password')" | pipenv run python web60ss/manage.py shell
pipenv run python web60ss/manage.py loaddata dump.json
pipenv run python web60ss/manage.py runserver 0.0.0.0:8000