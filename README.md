Taskstate
======

simple Django app that changes the object behavior based on its state

Development
-----------

Development is running using docker.

The following details how to deploy this application.

To build:

    make build

To get up and running use:

    make up

You can now access on <http://0.0.0.0:8000/>

To migrate your changes:

    make makemigrations
    make migrate

To restart:

    make restart

To launch shell\_plus from manage.py:

    make shell

To launch bash straight in the container run:

    make bash

### Email Server

In development, it is often nice to be able to see emails that are being
sent from your application. For that reason local SMTP server
[MailHog](https://github.com/mailhog/MailHog) with a web interface is
available as docker container.

Container mailhog will start automatically when you will run all docker
containers.

With MailHog running, to view messages that are sent by your
application, open your browser and go to `http://127.0.0.1:8025`

### Standard ipdb

To start debugging stop service and run the following command:

    make debug django

Then restart

Testing
-------

To run all tests on a separate container than the one is running
in:

    make test

To run all tests on the same container is running in:

    make test_local

To run a specific file/class/def:

    make test path/to/file/class/def
    make test_local path/to/file/class/def

Translation
-----------

### Application translation

To create the translation file run the following command in the django
container.

    ./manage.py makemessages --no-location -l ar
