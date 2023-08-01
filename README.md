# Shoppers-Store

The repository contains web pages using Django web development framework in python language. This project has been made, in an approach to make the selling of the items, quite easier for the shop keeper's and the consumer's can easily see all the items that are being sold.

This website has been integrated with Paypal Payment Gateway, for smooth transactions.
 
## Getting Started
 

Open terminal using Ctrl + Alt + T. Run the following command <br>
```ruby 
   git clone https://github.com/aayushray/Library-Management-System.git
```

Create and activate virtual environment using <br>
```ruby
   mkvirtualenv venv
   workon venv
```
<br>

Install requirements needed for the project, from requirement.txt
```ruby
    pip install -r requirements.txt
``` 


### Run Steps:

Create SuperUser to access Staff status to view admin panel.
```ruby 
   python manage.py createsuperuser
```
<br>

Make packaging up your model changes into individual migration files.
```ruby 
   python manage.py makemigrations
```
<br>

Roll out migrations to the server
```ruby 
   python manage.py migrate
``` 
<br>

Run Local Server at port 127.0.0.1:8000
```ruby 
   python manage.py runserver
``` 
