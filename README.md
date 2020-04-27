# TrueLayer Coding Challenge

## Quickstart

### Local Development

Install local dependencies

`pip install -r requirements.txt`

Set a local environment variable for `FLASK_APP`, e.g.

`export FLASK_APP=app.main:app`

and then

`flask run`

The app will be available under http://localhost:5000

### Docker Image

To build the docker image you can:

`docker build . -t truelayer`

and then

`docker run --name truelayer truelayer`

To access the container, run network

`docker network create dev_network`
`docker network connnect dev_network truelayer`

## Design

Looking at the design, it looked like this would involve two API calls, once to the Pokemon API and one to the 
Translation API, and no DB.  This seems overkill for Django, so I've gone with a bare level Flask app.  Flask isn't
something I'm completely familiar with, so it's been fun to learn.  

I used the Pokebase API because it was there and because it caches, which is always a good thing.  Caching would be a
sensible next step with an app like this, especially as it would be unlikely for the data to change a lot, and with the 
rate limiting on the Pokebase and Translation APIs.

Flask is also Dockerised.  

## Code

The main code is in `main.py`

Turns out there are three API calls, one to grab the Pokemon, one to grab the species and then a 
call to the shakespearian translator, which is done via the `request` library directly.

## Tests

Test use `unittest` and can be run with:

`python -m unittest tests.test_apps`

## ToDo

* Caching
* Better error handling