# cardkingdom-db
"JSON to MySql-database" script for all current MTG cards. This is possible thanks to http://mtgjson.com/

![Image of cardkingdom-db script](http://cattaneo.uy/private/cardkingdom-db.png)

Main goal of this script is to process up-to-date _cards.json_ files, but we'll also try to keep an already generated _export.sql_ file up-to-date (includes the database structure and all it's processed records ready to insert)

## Installation and running
### Requirements
* `pip install -r requirements.txt`
* Updated _cards.json_ file (if needed, we'll try to keep this one up-to-date)
### Running
* Modify _local_settings.tmp_ to suit your needs and rename it to _local_settings.py_
* Run _generate.py_: `./generate.py` or `python generate.py`
* Go take a cup of coffee!
### Misc
Cards count: 19032