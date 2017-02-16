# Whoa there!
    
If you are interested on hacking on this and contributing to this project, then stick around. These docs are for you.

However, if you are only interested in standing up your own 3cosystem service, then please head on up to the
flight-deck:

  - https://github.com/3cosystem/flight-deck. 
  
That is the meta-repo with all the sexy task-runners and glue that gets this whole damn thing off the ground.

Still here? Then let's dig in!

# Development
We live in a Docker world, and I'm a Docker girl. That means the preferred way to develop, test, and deploy
 is using Docker.

That said, you should still be using flight-deck to stand up the entire stack. 

## Required environment variables
Configuration is done through environment variables:

| Key | Description |
| --- | ----------- |
| `DJANGO_SECRET_KEY`| A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value.| 
| `DJANGO_LOG_LEVEL`| Set the logging verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `ALLOWED_HOSTS`| CSV line of allowed hosts. ip addresses or hostnames (eg  - "192.168.99.100,localhost,bob.com") |
| `DB_HOST` | Database hostname |
| `DB_NAME` | Database name |
| `DB_USER` | Database username |
| `DB_PASS` | Database user password |
| `SERVER_EMAIL` | The email address that emails are sent from (user@host.com) |
| `EMAIL_HOST` | Domain name or IP address of your smtp server |
| `EMAIL_PORT` | SMTP server port |
| `EMAIL_USER` | SMTP server user |
| `EMAIL_PASS` | SMTP user password |
| `DEV_ENV` | the development environment you are in. Defaults to 'dev' if no value is given.| 
| `PYTHONUNBUFFERED` | Default `1`. Set this to keep python from buffering console output|
| `GOOGLE_ANALYTICS` | UA-\*\*\*\*\*\*\*\*\* Key for google analytics|
| `SITE_VERSION` | The software version of the website. Note, this is set in the docker image when it is built. DO NOT SET THIS VARIABLE WHEN YOU START THE CONTAINER! Check the Dockerfile |

## Various django commands
There is a `Makefile` task-runner to help you run database migrations and load fixtures.  

  - `make migrate` will run Django `manage.py makemigrations && manage.py migrate` (this will load countries, cities, and their long, lat)
  - `make fixtures` will run Django load fixtures into a newly provisioned database
  - `make cachetable` will have Django create the cache table in postgres for view caching.

## Building the docker image
Take note that when updating the docker image you must update the SITE_VERSION variables in the top of the makefile.
This is, admidettly, not the most ideal way to track versions, but that will have to wait I guess.

We don't have a clever way yet of this piece of build automation. JUST. BE. CAREFUL.
