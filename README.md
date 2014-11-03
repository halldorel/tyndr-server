Týndr - Server
==============

Týndr server rewritten in Python 2.7 using the Google Cloud Endpoints and the Google App Engine

####Running locally
Download the Python Google App Engine SDK: https://cloud.google.com/appengine/downloads

Start the development server via

    path/to/go_appengine/dev_appserver.py path/to/project/folder/

If you want to clear the local datastore (e.g. if you've changed a model)

    path/to/go_appengine/dev_appserver.py --clear_datastore=yes path/to/project/folder/

Once the server is running, navigate to http://localhost:8080/_ah/api/explorer
