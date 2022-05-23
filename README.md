# API-Passport

# DOCKER

Crear imagen de FastAPI

    sudo docker build -t fastapi-passport:0.1 .

Correr imagen creada de FastAPI

    sudo docker run -p 9090:9090 --name api-passport fastapi-passport:0.1


Correr imagen de mysql asignando la contraseña

    sudo docker run -d -p 3306:3306 --name mysql-db -e MYSQL_ROOT_PASSWORD=password mysql

Ejecutar mysql para entrar a la terminal y crear base de datos o querys

    sudo docker exec -it mysql-5.7.38-oracle  mysql -p



