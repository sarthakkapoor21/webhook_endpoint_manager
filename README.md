# webhook-endpoint-manager

This is a Simple project which helps us capture the Request Data, Headers and Query Params of a POST Request sent to a specific URL.

This project also has functionality to let us create endpoints, which can be used to send Requests and their data can be subsequently captured.

# System Requirements

* psql (PostgreSQL) 10+.
* Python v3.7.9

# Setup Instructions

* Install [pipenv](https://docs.pipenv.org/install/#installing-pipenv)
* Clone this project

    * git clone git@github.com:sarthakkapoor21/webhook_endpoint_manager.git
    * cd webhook_endpoint_manager

* Install Dependencies
    * pip install --dev
    
* Use the local_settings.py.template file to create a local_settings.py file (Make sure you populate correct DB settings)

* Activate pipenv Virtual Environment with `pipenv shell`

* Run `python manage.py migrate` to create all tables in DB.
  
* Run `python manage.py createsuperuser` to create a superuser which can be used to login to Django Admin at `localhost:port/admin`

* Run `python manage.py runserver` to start the server
    