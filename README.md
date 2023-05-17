# project-savethehawkers
![ezgif com-video-to-gif](https://user-images.githubusercontent.com/79783660/235750189-1d93b4ea-4592-43e8-8776-897533c2a113.gif)
https://youtu.be/4W4Nuv7poSo
Directory of the hawker stalls with digital illiteracy


## Story
This was a passion project built by myself during the COVID-19 pandemic. With the hawkers facing issues with receiving exposure, I crafted my own geolocation system to find the nearest hawker stalls that are lacking delivery services.

I learned so much from this project, and I think it was a good experience.

## Apologies
The main code is very inefficient because I didn't know how to abstract code, so you can see functions that are repeated end on end...

## Running the code
1. Production Environment
http://savethehawkers.herokuapp.com/

2. Local Environment

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate --run-syncdb

python manage.py runserver
