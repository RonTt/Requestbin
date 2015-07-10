# [RequestBin](http://requestb.in)
## A Runscope community project.

Originally Created by [Jeff Lindsay](http://progrium.com)

License
-------
MIT


Looking to self-host?
=====================

## Deploy your own instance using Heroku
Create a Heroku account if you haven't, then grab the RequestBin source using git:

`$ git clone git://github.com/Runscope/requestbin.git`

From the project directory, create a Heroku application:

`$ heroku create`

Add Heroku's addon for redistogo

`$ heroku addons:add redistogo:nano --app {app_name}`

Find your redistogo connection details

`$ heroku config --app {app_name} | grep REDISTOGO_URL`

Open `requestbin/config.py` and locate variables `REDIS_URL` and `REDIS_PORT`. Edit them with the connection details you got in the previous step:

```python
REDIS_URL = "REDISTOGO_URL"
REDIS_HOST = "localhost"
REDIS_PORT = REDISTOGO_PORT
```

Now just deploy via git:

`$ git push heroku master`

It will push to Heroku and give you a URL that your own private RequestBin will be running.


Contributors
------------
 * Barry Carlyon <barry@barrycarlyon.co.uk>
 * Jeff Lindsay <progrium@gmail.com>
