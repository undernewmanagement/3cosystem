# INSTALLATION

  1. Provision Postgres database with Postgis Extensions. You can do that 
using the shell scripts from the azure-utils repo. `pg-create-database-and-user.sh` 

  2. Setup you local environment variables. 
```
  - DB_HOST='example.com'
  - DB_NAME='dbname'
  - DB_USER='dbuser'
  - DB_PASS='dbpass'
  - DJANGO_SETTINGS_MODULE='website.settings.dev'  or 'website.settings.prod'
```
  3. run `manage.py migrate`
  4. run `manage.py loaddata fixtures/geography.json` (this will load countries, cities, and their long, lat)
  5. Done


## Development
Use docker-compose to get up and running in development
