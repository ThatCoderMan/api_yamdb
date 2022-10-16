# **API for YamDB**

### technologies in the project
- Python 3.7
- Django 2.2.16
- Django rest framework 3.12.4
- DRF simplejwt 5.2.1

## Description
API for the APIYamDB project with registration capabilities; work with users;
posts; genres; categories; publications; reviews and comments on them.

## Installation
- Clone the repository from GitHub and go to it
    ~~~
    git clone https://github.com/ThatCoderMan/api_yamdb.git
    cd api_yamdb
  ~~~
- Create and activate virtual environment, install dependencies from requirements.txt file
    ~~~
    python -m venv venv
    venv/Scripts/activate
    pip install -r requirements.txt
    ~~~
- Make migrations
    ~~~
    python api_yamdb/manage.py migrate
    ~~~
- Start server 
    ~~~
    python api_yamdb/manage.py runserver
    ~~~
  
## API examples

**Rights for users:**

- _anonymous_ - can view descriptions of works, read reviews and comments.

- _authenticated user_ - can read everything, like Anonymous, can publish reviews and rate works (films / books / songs), can comment on reviews, edit and delete their reviews and comments, edit their own ratings of works;

- _moderator_ - the same rights as the Authenticated user, plus the right to delete and edit any reviews and comments;

- _administrator_ - can create and delete works, categories and genres, assign roles to users;

- _superuser_ - administrator rights, you can not change the role


#### The authors:
- [Артемий Березин](https://github.com/ThatCoderMan)
- [Вячеслав Шведов](https://github.com/Omen121)
- [Игорь Штенгелов](https://github.com/kontarkovi)