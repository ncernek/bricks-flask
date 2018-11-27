
# Deploying the App to Google Cloud 

`app.yaml` has the configuration for your app in the cloud.

`.gcloudignore` is the `.gitignore` equivalent for GCP.

GCP will install dependencies defined in `requirements.txt`.

When you want to deploy, use this from within the directory: `gcloud app deploy --project bricks-app`. `bricks-app` is the name of the project as seen in the GCP console.

If  you want to run the GCP sdk dev server locally, run `dev_appserver.py --application=bricks-app app.yaml --port=5000`. 
If you get an error about Python 3 not being supported, that's just because dev_appserver.py is written in 
python 2.7 and needs explicit instruction in the shebang to call up that interpreter.

# Deploying the DB to Google Cloud
The name of the service is Cloud SQL.
The name of the db is `bricks-db` (subject to change).

Follow these steps to create a Postgres instance: https://cloud.google.com/sql/docs/postgres/create-instance

# Connect the App to the DB in Google Cloud
https://cloud.google.com/appengine/docs/standard/python3/using-cloud-sql

# Managing your deployed app
To shut your app down:
https://console.cloud.google.com/appengine/settings?project=bricks-app&serviceId=default

# Connecting local app to Deployed DB
Use the Google Cloud Proxy service instructions:
https://cloud.google.com/sql/docs/postgres/connect-admin-proxy

Remember that if you're ever connecting to a prod instance, you should use a public/private key (which isnt the default).

Set GAE_ENV to `standard` in your env. Now anything you run, such as `gunicorn` to launch the app, or `python manage.py db upgrade`
will connect to the Cloud SQL Proxy

# Connect locally via command line to Prod DB
start the Cloud SQL proxy: `./cloud_sql_proxy -dir=/cloudsql &`

Connect your local psql: `psql "sslmode=disable host=/cloudsql/bricks-app:us-west2:bricks-db user=postgres"`