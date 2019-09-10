# UserDataBase

#### Simple project

## Description of Entities

* front - Front server. Responsible for proxying requests to microservices and distributing statics.

* auth - Authorization server. Responsible for request authentication and authorization.

* logic - REST server. Responsible for core business logic.

* database - MYSQL Database

## Access control of microservices used by JWT

* level 1 - read only (GET)
* level 2 - edit (GET, PATCH)
* level 3 or more - create/read/edit/delete (POST, GET, PATCH, PUT, DELETE)

## Locations

* / - Editable user table. Displays internal and external users. The username must be unique. The access level must be a number from 1 to 3. External users cannot be edited.

* /login - Form of atorization. 

## Documentation

https://app.swaggerhub.com/apis/alexgreendev/UserDataBase/1.0.0

## Dependencies

* make
* docker
* docker-compose

## Instruction

1. Build docker images
> make build

2. Start server
> make start

3. Stop server
> make stop