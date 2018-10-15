# cardkingdom-db
"JSON to MySql-database" python3 script for all current MTG cards. This is possible thanks to http://mtgjson.com/

![Image of cardkingdom-db script](http://cattaneo.uy/private/cardkingdom-db.png)

Main goal of this script is to process up-to-date _cards.json_ files, but we'll also try to keep an already generated and up-to-date _export.sql_ file (includes the database structure and all it's processed records ready to insert)

Current _export.sql_ file can be downloaded [here](http://cattaneo.uy/private/export.sql)

## Installation and running
### Requirements
* Optional: _cards.json_ file. Only if `USE_LOCAL_JSON` is set `True`
* A MySql database
* python3
* `pip install -r requirements.txt`
### Running
* Modify _local_settings.tmp_ to suit your needs and rename it to _local_settings.py_
* Run _generate.py_: `./generate.py` or `python generate.py`
* Go take a cup of coffee!
### Misc
Cards count: 19032