A Little About Cinema
=

Something, just something related to the art of cinema

# v2.2
A complete API for info about movies (which you wouldn't get on Google!)

Build is up and running. Checkout my movie list at https://alac-api.herokuapp.com/

## Tech stack
- Django (core & rest framework)
- PostgreSQL

## Modules
- Movies
- Categories

## Requirements
- Python (perferably 3.6+)
- PostgreSQL

## Setup & Installation
### PostgreSQL setup
The default psql url is set to `postgresql://rick:rickdalton@localhost/alac` so configure as

- Database name: **alac**
- User: **rick**
- Password: **rickdalton**
- all privileges over alac to user rick

### Install required packages
Create a python virtual environment and run the command

```pip install -r requirements.txt```

### DB migrations
If your DB configuration is correct, you will be able to migrate the django models using the following command

```python manage.py migrate```

### Django super user
You will require a Django super user config and auth token to create & edit the db records. Create a super user by running the following command

```python manage.py createsuperuser```

The above command will prompt for a *username*, *email* and *password*.

### User Auth token
Create auth token for the user using the following command

```python manage.py drf_create_token <username>```

Note down this token, you will require to add it as **Authentication token** header while making requests. You will find help to configure this token for your Postman requests [here](https://learning.postman.com/docs/sending-requests/authorization/#oauth-20)

## First Run
Start the django server by running the command

```python manage.py runserver```

and voila, your server will run at port 8000. For a specific port, run the above command as ` runserver <PORT>`

## API
To understand the modules & endpoints, try going through the [API documentation](https://github.com/datmemerboi/A-Little-About-Cinema/blob/main/API%20Documentation.md)

# v1.0
Just .md documents of

- Aug 17, 2019 - **Eat.Sleep.Die.Repeat**
- Oct 08, 2019 - **Superhero movie without a Super Hero**
