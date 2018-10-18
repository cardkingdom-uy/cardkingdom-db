# cardkingdom-db

Main goal of these scripts is to maintain an up-to-date MTG cards database, including their market prices. We'll also try to keep an already generated and up-to-date _export.sql_ file (includes the database structure and all it's processed records ready to insert)

Latest _export.sql_ file can be downloaded [here](http://cattaneo.uy/private/export.sql.zip)

## generate.py
"JSON to MySql-database" python3 script for all current MTG cards. This is possible thanks to http://mtgjson.com/ (v4)

![Image of cardkingdom-db script](http://cattaneo.uy/private/cardkingdom-db-v2.png)

### Installation and running
#### Requirements
* Optional: _AllSets.json_ file. Only if `USE_LOCAL_JSON` is set `True`
* A MySql database
* python3
* `pip install -r requirements.txt`
#### Running
* Modify _local_settings.tmp_ to suit your needs and rename it to _local_settings.py_
* Run _generate.py_: `./generate.py` or `python generate.py`
* Go take a cup of coffee!
### Misc
Set's cards count: 44141

All row's count: 1182933

## update_prices.py
This script updates all cards prices

Currently supported websites:
* TODO (CK will be the first one)

### Installation and running
#### Requirements
* At least one successful _generate.py_ execution
#### Running
* Modify _local_settings.tmp_ to suit your needs and rename it to _local_settings.py_
* Run _update_prices.py_: `./update_prices.py` or `python update_prices.py`
* Go take a cup of coffee!