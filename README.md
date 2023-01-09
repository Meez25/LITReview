# Installation

## Clone the repo
``` bash
git clone https://github.com/Meez25/LITReview
```
Then go in the LITReview folder

# Create the virtual environement

``` bash
python3 -m venv env
source env/bin/activate
```

(env) should now be displayed on the left of your prompt

To download all the libraries, you can do this command 

``` bash
pip install -r requirements.txt
```

This will install all the dependancies necessary to run the Django Server

Then : 
``` bash
cd litreview
python manage.py runserver
```

A few user are already created with some content :
- admin with password toto
- user1 with password toto
- user2 with password toto
- user3 with password toto

With the admin account, you can go to http://127.0.0.1:8000/admin to log in as
the admin
