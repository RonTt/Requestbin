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

Modify line 19 of config/heroku.conf.py on redis details

`redis_url = urlparse.urlparse(os.environ.get("REDIS_URL", "redis://REDISTOGO_URL:REDISTOGO_PORT/0"))`

Now just deploy via git:

`$ git push heroku master`

It will push to Heroku and give you a URL that your own private RequestBin will be running.


Contributors
------------
 * Barry Carlyon <barry@barrycarlyon.co.uk>
 * Jeff Lindsay <progrium@gmail.com>