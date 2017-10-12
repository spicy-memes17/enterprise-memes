# enterprise-memes
A professional enterprise meme portal

## Getting started
Everything you need to do to work on the project.

### Prerequisites
In order to run this project, you need
```
Python 3
pip
virtualenv
Django
```
The virtualenv is mostly used to manage project dependencies separate from your other python dependencies, so it is optional, but should be used!

### Setup
I will assume you have Python 3 and pip installed, as it may be slightly different, depending on your OS. The following steps should illustrate, how you can clone the project and install Django in a virtualenv.

First, run
```
[sudo] pip install virtualenv
```
to install the virtualenv package system-wide.

Now you need to clone the project to a location of your liking, using
```
git clone https://github.com/spicy-memes17/enterprise-memes.git
```
to clone via HTTPS. Navigate into that folder and run
```
mkdir .venv
cd .venv
virtualenv django-dev
```
to create a new virtual environment called "django-dev" inside a hidden folder, which git ignores.
Next, you need to activate the virtualenv. If you use a linux bash, run
```
source django-dev/bin/activate
```
to activate the environment. 

On a Windows system, run 
```
django-dev\Scripts\activate.bat 
```
instead of the source-command above. Now, every dependency is loaded from "django-dev". In order to install Django, simply run
```
pip install Django
```
while the virtualenv is active. Django is now available until you deactivate the environment, using
```
deactivate
```
(All of these steps where tested using a linux bash.)

### Configure PyCharm to user virtualenv

- Open the Settings and enter ```Project Interpreter``` in the search box. Then click ```Project Interpreter```.
- Click the gear icon on the top right, then click ```add local```
- Select the python binary from the virtual enviroment you just set up. In my case this is ```~/git/enterprise-memes/.venv/django-dev/bin/python```
- Click OK a couple of times


Happy coding!
