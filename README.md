## Init

##### Destroy docker containers and volumes
```bash
docker system prune -a
docker volume prune
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -a -q)
```

##### Docker (dev)
```bash
docker-compose run web python3 manage.py makemigrations
docker-compose run web python3 manage.py migrate
docker-compose run web python3 manage.py loaddata initial_data
docker-compose run web python3 manage.py makemessages -l ru
docker-compose run web python3 manage.py makemessages -l en
docker-compose run web python3 manage.py compilemessages -l ru
docker-compose run web python3 manage.py compilemessages -l en
docker-compose run web python3 manage.py createsuperuser
docker-compose build --no-cache
docker-compose up
docker-compose down --volume
docker-compose run --rm web python3 manage.py loaddata blink/main/fixtures/data.json 
```

##### .env file
```bash
DEBUG=True
SECRET_KEY==change_me
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_HOST=db
HTTPS=False
```