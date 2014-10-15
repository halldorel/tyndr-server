Týndr-server
============
The development server is currently running at http://tyndr.herokuapp.com/

####Running the Týndr server *locally*
* Install node.js `> brew install node`
* Install StrongLoop globally `> npm install -g strongloop`
* Create a PostgreSQL database named 'tyndr'
* Currently, there are *two* `datasources.json`-files. To run locally, we need to rename `_local_datasources.json` -> `datasources.json` before running locally (make sure not to commit the renamed `datasources.json`). I will fix this soon, and have SL read the database uri from an environment file.
* In the root of the project run `slc run`


####Adding models to the *deployment* database
* Having installed the Heroku toolbelt on your machine, run `> heroku run bash` from the root of the project
* Once you have connected to the Heroku server run `> slc loopback:model` and follow the instructions from the wizard.


Communication with the back end
-------------------------------
Note: You can play around with the GET and POST requests at will on http://tyndr.herokuapp.com/explorer/

####*Creating* advert instances on the deployment back end

Create a POST request with the following data:

    {
      "name": "Halldór Eldjárn",
      "lost": true,
      "resolved": false,
      "location": "-21.89541,64.13548",
      "description": "Halldór er týndur :(",
      "reward": "Nei",
      "created_at": "2014-10-14T17:40:13.467Z"
    }
    
Note that "location" should be on the form "longitude,latitude". Also note, that if you send in an *id* in the POST request, you break the auto incrementation and everything will stop working. "created_at" is a timestamp that should eventually be automatically populated, however for now you will need to send a string with the *same* format as the example above.

Send this POST request to the following URL:
    http://tyndr.herokuapp.com/api/adverts

You will receive a status 200 response with the same information you sent, *plus* the unique id that got assigned to it!

####*Querying* the deployment back end for adverts
Querying is easy, you just specify a filter in a GET request and you receive a list of objects that match the query. Note that you may have to url-encode the strings, (e.g. turn spaces into `%20`, brackets from `[` and `]` into `%5B` and `%5D` respectively, etc.) In the following query, the data in the GET request are `{"filter[where][id]" : 3}`

    http://tyndr.herokuapp.com/api/adverts?filter[where][id]=3

Another example:

    http://tyndr.herokuapp.com/api/adverts?filter[where][name]=Halldór Eldjárn

An empty GET request (with no data) sent to `http://tyndr.herokuapp.com/api/adverts` will return all advert objects in the database

You can filter on any attribute of the model, see
    http://docs.strongloop.com/display/LB/Querying+models#Queryingmodels-Filters
