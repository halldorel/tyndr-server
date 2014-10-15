Týndr-server
============

####Running the Týndr server *locally*
* Install node.js `> brew install node`
* Install StrongLoop globally `npm install -g strongloop`
* Create a PostgreSQL database named 'tyndr'
* Currently, there are *two* `datasources.json`-files. To run locally, we need to rename `_local_datasources.json` -> `datasources.json` before running locally (make sure not to commit the renamed `datasources.json`). I will fix this soon, and have SL read the database uri from an environment file.
* In the root of the project run `slc run`
