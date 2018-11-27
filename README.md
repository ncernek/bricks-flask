
# Flask App Deployment

### Deploying the App to Google App Engine (GAE)

* Go through the Quickstart [instructions](https://cloud.google.com/appengine/docs/standard/python3/) on GAE because this will set up the `gcloud` cli on your system, which will be essential to use GAE's features.

* Set up the bricks project. You need to go through each step in the "How-to Guides".

* `app.yaml` is the file you create that GAE looks at to know how to run your app. Don't put env variables here (even though GAE's docs suggest it). Instead rely on python-dotenv to read your `.env` file.

* `.gcloudignore` is the `.gitignore` equivalent for GAE.

* GAE will install dependencies as defined in your `requirements.txt`.

* When you want to deploy, use this from within the directory: `gcloud app deploy --project bricks-app`.

### Testing your deployment locally

* If  you want to run the GAE SDK dev server locally, run `dev_appserver.py --application=bricks-app app.yaml --port=5000`. 
`dev_appserver.py` exists in some random folder but for some reason it was on my path, as I could run it from my repo. If you get an error about Python 3 not being supported, that's just because dev_appserver.py is written in python 2.7. The dirty fix is to change the shebang (in the file) to call up the python3 interpreter.

### Managing your deployed app
[Shut your app down](https://console.cloud.google.com/appengine/settings?project=bricks-app&serviceId=default) so it can't incur expenses.


# Postgres DB Deployment

### Deploying the DB to Google Cloud SQL
* The name of the db is `bricks-db` (subject to change).
* Follow these [steps](https://cloud.google.com/sql/docs/postgres/create-instance) to create a Postgres instanceon Cloud SQL. 

### Connect the App to the DB in Google Cloud
https://cloud.google.com/appengine/docs/standard/python3/using-cloud-sql

### Connecting Local App to Deployed DB
The point of this is to be able to run migrations. I haven't succeeded in accessing the console for the GAE instance to run the migrations from there.

* Follow the Google Cloud Proxy service [instructions](https://cloud.google.com/sql/docs/postgres/connect-admin-proxy).

* start the Cloud SQL proxy: `./cloud_sql_proxy -dir=/cloudsql &`

* First connect your local psql so you can validate the changes your migrations make: `psql "sslmode=disable host=/cloudsql/bricks-app:us-west2:bricks-db user=postgres"`

* Remember that if you're ever connecting to a prod instance, you should use a public/private key (which isnt the default).

* When your Flask app is deployed, GAE sets GAE_ENV to `standard` in your env as a way for your app to know it is deployed. You can use this trick to use the deployed connection (set in `config.py`), because the specs to connect to Cloud SQL from GAE are the same as the specs to connect your local app to Cloud SQL Proxy. Now anything you run, such as `gunicorn` to launch the app, or `python manage.py db upgrade` will connect to the Cloud SQL Proxy, ie to the prod instance of your app.
