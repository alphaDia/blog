# A blog application with a postgresql relational database system
## Features of the blog application
The blog application is composed of the following features:

- [x] Managing post state (**publish/draft**)
- [x] Commenting posts
- [x] Sharing post by e-mail
- [x] Recommending post by similarity
- [x] Categorizing posts by using tags
- [x] Searching posts by using postgresql full text search engine
- [x] A list of most commented post
- [x] A list of recent post
- [x] An Rss feed to connect to
- [x] A sitemap for search engines
- [x] Genarate SEO Friendly link for a post

## Dependencies

- python
- django
- django-taggit
- markdown
- sycopg2-binary

## Setting up with Dokcer
Make sure you have docker on your computer or download docker from [Docker](https://docker.com/)

we will be using these two images
  - alphadev224/blog
  - postgresql:15-alpine

## Lunch Containers

> docker-compose up 

The web app will be available at **localhost:8080/blog**.  

## Load Sample Data

To load the sample data just run the following command inside the container  

> docker-compose exec web ./init.sh

Now head over to **localhost:8080/blog** to see some posts.  
## Logging to the admin interface
  - username: admin
  - password: 1234
 


## Setting up a virtual environment

- venv
- pipenv

### Create a virtual environment using venv
> python -m venv blog

### Activate virtual environment
- windows: blog/Scripts/activate
- linux: source blog/bin/activate

### Install project dependencies
> pip install -r requirements.txt

## Initialize the database

> python manage.py migrate

## Load sample data 

> python manage.py loaddata blog_data.json

## Log to the admin interface
- username: admin
- password: 1234


