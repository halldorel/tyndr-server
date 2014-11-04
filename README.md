Týndr - Server
==============

Týndr server rewritten in Python 2.7 using the Google Cloud Endpoints and the Google App Engine
Currently running at https://tyndr-server.appspot.com/_ah/api/explorer

####Running locally
Download the Python Google App Engine SDK: https://cloud.google.com/appengine/downloads

Start the development server via

    path/to/go_appengine/dev_appserver.py path/to/project/folder/

If you want to clear the local datastore (e.g. if you've changed a model)

    path/to/go_appengine/dev_appserver.py --clear_datastore=yes path/to/project/folder/

Once the server is running, navigate to http://localhost:8080/_ah/api/explorer


####Interfacing with the API

All calls for adverts must be supplied with a label, denoting them as either lost_pets or found_pets

#####Creating an Advert

To create an advert you need to be authenticeted via OAuth 2.0 (more on that later). Send a POST request to https://tyndr-server.appspot.com/_ah/api/tyndr/v1/create with the following data:

    {
     "age": "7",
     "color": "beige",
     "description": "very nice",
     "label": "lost_pets",
     "name": "Halldór Eldjárn",
     "species": "dog",
     "subspecies": "border collie"
    }

#####Get N latest Adverts

Sending a GET request with the data {label: lost_pets} to https://tyndr-server.appspot.com/_ah/api/tyndr/v1/all/8 returns the 8 latest ads. Replace 8 with any integer.

#####Getting a specific Advert

Sending a GET request with the data {label: lost_pets} to https://tyndr-server.appspot.com/_ah/api/tyndr/v1/single/5838406743490560 returns the Advert for a lost pet with the ID 5838406743490560 (IDs are non-sequential) if it exists, else returns a JSON-string with an error element.
