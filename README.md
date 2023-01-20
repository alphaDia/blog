This repository is about a blog application built with django and the postgresql  
database management system. 

## Try out the project using docker 

The repository include a **docker compose** file to let anyone try out this project easily without  
the hassle of setting up adevelopment environment.  
Download the repository and fire the following command

> **docker-compose up** 

This will download both **alphadev224/blog** and **postgresql:15-alipine**  
images and then lunch the corresponding containers.

The web app will be available at **localhost:8080/blog** but you will find no blog post  
since there is no post inside the database. 

There is actually a django fixture file named **blog_data.json** that we are going to use  
to load some data inside our database, to do so execute the following command

>**docker-compose exec web python manage.py migrate**

> **docker-compose exec web python manage.py loaddata blog_data.json**


Now head over to **localhost:8080/blog** you'll find three posts, if you want to add  
new post by yourself you can login with these credentials **username**=admin   
and **password**=1234 to the django admin interface.


## Try out the project using a virtual environment
First of all you need to have python installed, then you can create a virtual environment  
using **venv** or **pipenv** or any other python library that allows you   
to create a virtual environments.  

### Create a virtual environment using venv
> python -m venv blog

### Activate the virtual environment

>**windows -> blog/Scripts/activate**

>**linux -> source blog/bin/activate**

### Install the dependencies of the project
> **pip install -r requirements.txt**

Then the next step is to create the database and execute the migration files.  
You can inspect the **settings.py** file to see the database configurations  

> **python manage.py migrate**

There is a file named **blog_data.json** which has sample data that you can  
directly insert into the database, just type the following  

> **python manage.py loaddata blog_data.json** 

This command will create some posts inside the database and a   
superuser (username=admin, password=1234) which you can use to create post.

## Features of the blog application
The blog application is composed of the following features:

1. Managing post state (**publish/draft**)
2. Commenting posts
3. Sharing post by e-mail
4. Recommending post by similarity
5. Categorizing posts by using tags
6. Searching posts by using postgresql full text search engine
7. A list of most commented post
8. A list of recent post
9. An Rss feed to connect to
10. A sitemap for search engines
11. Genarate SEO Friendly link for a post

