Contribute!

Contributors
------------
 * Barry Carlyon <barry@barrycarlyon.co.uk>
 * Jeff Lindsay <progrium@gmail.com>

License
-------
MIT

Installation
============

RequestBin can be used in three ways:

1. Use the hosted service at requestb.in
1. Deploy your own instance using Heroku
1. Run it locally from the command line (coming soon)

## Deploy your own instance using Heroku
Create a Heroku account if you haven't, then grab the RequestBin source using git:

`$ git clone git://github.com/progrium/requestbin.git`

From the project directory, create a Heroku application:

`$ heroku create --stack cedar`

Add Heroku's addon for redistogo

`$ heroku addons:add redistogo:nano --app {app_name}`

Find your redistogo connection details

`$ heroku config --app {app_name} | grep REDISTOGO_URL`

Modify line 19 of config/heroku.conf.py on redis details

`redis_url = urlparse.urlparse(os.environ.get("REDIS_URL", "redis://REDISTOGO_URL:REDISTOGO_PORT/0"))`

Now just deploy via git:

`$ git push heroku master`

It will push to Heroku and give you a URL that your own private RequestBin will be running.

## Run it locally from the command line
Although this is possible now by checking out the source and poking around, our intention is to release an easy to install version of RequestBin that you can use from the command line to quickly debug local HTTP requests. This is coming soon.
