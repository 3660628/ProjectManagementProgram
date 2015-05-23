Follow the following instructions to run this application on your local machine. The instructions are for UNIX based machines (Linux/Mac). Windows machines will differ somewhat. 

Prerequisites: Your computer should have python installed (All Linux distributions and Apple computer already do. Windows machines don't) You will need to also have Pip and Git installed.

Install Python (Windows Only): https://www.python.org/downloads/release/python-279/
Install Pip: https://pip.pypa.io/en/latest/installing.html
Install Git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

Run the following commands:

mkdir test
cd test
git clone https://github.com/royroy21/ProjectManagementProgram.git
cd ProjectManagementProgram/CodeBase/CodeBase/ProjectManagementProgram/
source ../../venv/bin/activate
pip install django
pip install djangorestframework
python manage.py syncdb

At this stage you will be prompted to enter an admin username and password for use with the admin site.

python manage.py test

This will run all UnitTests for the application as specified in the tests.py file. These should all return without errors. 

python manage.py runserver

This will start a web browser running the application. Going to the URL http://127.0.0.1:8000/admin/ and entering the admin username and password will give you access to the admin site. Using this web browser you can also access the API calls created. For example going to http://127.0.0.1:8000/api/user/ will display the user you created when using the python manage.py syncdb command. Try adding another user using the form provided and refreshing the page. This will now display two users. Going to http://127.0.0.1:8000/api/user/1/ will display the user an id of 1. This will prompt you for authentication details. Other API URLs can be accessed in this way however this web service is only meant to be a development tool and should be turned off in production.
