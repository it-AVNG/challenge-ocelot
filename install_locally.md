# Install the project on local PC
This guide will walk you through the steps to install the application locally. Before you begin, make sure you have the following prerequisites installed on your system:
If you haven’t already, you’ll need to install Git and Docker. You can download them from their official websites:
+ [Git](https://github.com/git-guides/install-git)
+ [Docker](https://www.docker.com/get-started/)
+ [Docker-compose](https://docs.docker.com/compose/install/)

It is better for set up git with SSH key, this guide will follow the SSH key method from git

Remember to follow the guide and set the permission for docker appropriately.
It is important to enable docker service and agent, please check the official document to properly set up docker.

## Foreword:
This application is built using Django, Django REST frameworks and in python 3.11.6 environment for package dependencies, please refer to [requirements.txt](https://github.com/it-AVNG/challenge-ocelot/blob/main/requirements.txt)
However, this guide will walk through the app installation using docker and everything will be run using `docker-compose` command prefix. Thus install python and set up env is unecessary. Docker will create and setup its own environment using `dockerfile` and `docker-compose.yml`

## Step1: Clone the repos

Create a dedicated directory for cloning the app
Clone the repo at [link](https://github.com/it-AVNG/challenge-ocelot)

```shell
mkdir django-app
cd django-app
git clone git@github.com:it-AVNG/challenge-ocelot.git
cd challenge-ocelot
```

## Step2: Run docker
In the directory, run docker to build the image

```shell
docker build .
```

After docker has finished building, run `docker-compose`

```shell
docker-compose up
```
to check if the app run properly the out put should be similar as below

```shell
> System check identified 1 issue (0 silenced).
> November 17, 2023 - 12:28:05
> Django version 4.2.7, using settings 'app.settings'
> Starting development server at http://0.0.0.0:8000/
> Quit the server with CONTROL-C.
```

Now, if you navigate to `127.0.0.1:8000/api/docs` you should be able to see the API endpoint documentation.

press Crtl-C to stop the shell, the following step will help you to understand how to run management command locally

## Step3: create super user

to create super user, we use the following `docker-compose` command

```shell
docker-compose run --rm app sh -c "python manage.py createsuperuser"
```
Follow the prompt instructions and you have successfully create an adminstrator for the app.

to run tests

```shell
docker-compose run --rm app sh -c "python manage.py test"
```

to run Linting

```shell
docker-compose run --rm app sh -c "flake8"
```

To spin the container back up
```shell
docker-compose up
```
you can navigate to `127.0.0.1:8000/admin` to login to the admin app.

**Note**: it is necessary to add the options to the `docker-compose run` command because it is preventing built-up of the images inside your machine.

## Step4: spin down the app

As we have finished with the app, we can spin the container down using

```shell
docker-compose down
```

