#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mysql.connector as db
import json
import sys
from collections import OrderedDict
try:
    from local_settings import *
except ImportError:
    pass

"""
JSON to MySql-database of all current MTG cards
JSON file should be obtained from http://mtgjson.com/
"""

"""Return sql compatible string"""
def build_sql_string(text):
    return "'%s'" % text.replace("'", "''")

"""Return sql compatible date"""
def build_sql_date(text):
    return "STR_TO_DATE('%s', '%%Y-%%m-%%d')" % text

"""Check for key existence and build the string"""
def check_key_string(dict_object, key_name):
    return "''" if dict_object.get(key_name) == None else build_sql_string(dict_object[key_name])

"""Check for key existence and return it's length"""
def check_key_length(dict_object, key_name):
    return 0 if dict_object.get(key_name) == None else len(dict_object[key_name])

"""Create DB structure"""
def create_structure(db_cursor, sql_file):
    file = open(sql_file, "r", encoding="utf-8")
    parsed_sql = ""
    # clean up export
    for line in file:
        if line.strip() != "" and line[:2] != "--":
            parsed_sql += line.replace('\n', ' ')
    sql_queries = parsed_sql.split(";")
    for query in sql_queries:
        db_cursor.execute(query)
    db_cursor.execute("commit")

"""Parse and insert each card record"""
def parse_json(db_cursor, json_file):
    with open(json_file, "r", encoding="utf-8") as json_file:
        json_text = json_file.read()
    cards = json.loads(json_text, object_pairs_hook=OrderedDict)
    count = 0
    errors = []
    for card in cards:
        queries = []
        count += 1
        current_card = cards[card]
        print("Processing JSON file... %i" % count, end='\r')
        sys.stdout.flush()
        name = check_key_string(current_card, "name") # Primary key
        current_name = name
        layout = check_key_string(current_card, "layout")
        mana_cost = check_key_string(current_card, "manaCost")
        cmc = current_card["cmc"]
        card_type = check_key_string(current_card, "type")
        text = check_key_string(current_card, "text")
        power = check_key_string(current_card, "power")
        toughness = check_key_string(current_card, "toughness")
        imageName = check_key_string(current_card, "imageName")
        hiddenId = count
        pictureUrl = build_sql_string("http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%s&type=card" % str(439389 + count))
        # Insert into 'cards' table
        queries.append("INSERT INTO `cards`(`name`, `currentName`, `layout`, `manaCost`, `cmc`, `type`, `text`, `power`, `toughness`, `imageName`, `hiddenId`, `pictureUrl`) VALUES (%s,%s,%s,%s,%i,%s,%s,%s,%s,%s,%i,%s)" % (name, current_name, layout, mana_cost, cmc, card_type, text, power, toughness, imageName, hiddenId, pictureUrl))
        # Insert into 'cards_colors' table
        if check_key_length(current_card, "colors") > 0:
            for current_color in current_card["colors"]:
                queries.append("INSERT INTO `cards_colors`(`color`, `name`) VALUES (%s,%s)" % (build_sql_string(current_color), name))
        # Insert into 'cards_types' table
        if check_key_length(current_card, "types") > 0:
            for current_type in current_card["types"]:
                queries.append("INSERT INTO `cards_types`(`type`, `name`) VALUES (%s,%s)" % (build_sql_string(current_type), name))
        # Insert into 'cards_printings' table
        if check_key_length(current_card, "printings") > 0:
            for current_printing in current_card["printings"]:
                queries.append("INSERT INTO `cards_printings`(`printing`, `name`) VALUES (%s,%s)" % (build_sql_string(current_printing), name))
        # Insert into 'cards_rulings' table
        if check_key_length(current_card, "rulings") > 0:
            ruling_count = 0
            for current_ruling in current_card["rulings"]:
                ruling_count += 1
                queries.append("INSERT INTO `cards_rulings`(`ruling`, `name`, `date`, `text`) VALUES (%i,%s,%s,%s)" % (ruling_count, name, build_sql_date(current_ruling["date"]), build_sql_string(current_ruling["text"])))
        # Insert into 'cards_subtypes' table
        if check_key_length(current_card, "subtypes") > 0:
            for current_subtype in current_card["subtypes"]:
                queries.append("INSERT INTO `cards_subtypes`(`subtype`, `name`) VALUES (%s,%s)" % (build_sql_string(current_subtype), name))
        # Insert into 'cards_coloridentity' table
        if check_key_length(current_card, "colorIdentity") > 0:
            for current_identity in current_card["colorIdentity"]:
                queries.append("INSERT INTO `cards_coloridentity`(`identity`, `name`) VALUES (%s,%s)" % (build_sql_string(current_identity), name))
        for query in queries:
            try:
                db_cursor.execute(query)
            except Exception as e:
                errors.append(e)
    if len(errors) > 0:
        print("\nThere's been some errors:")
        for error in errors:
            print(error)
    db_cursor.execute("commit")

def main():

    print("cardkingdom-db script")
    print("Contribute on https://github.com/cardkingdom-uy\n")

    # Connect to the mysql database
    db_connection = db.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        passwd=DB_PASS
    )

    print("Connected to %s" % DB_HOST)

    # Main db cursor
    db_cursor = db_connection.cursor()

    # Create database structure
    print("Creating structure using \"%s\"... " % DB_EXPORT, end='')
    try:
        create_structure(db_cursor, DB_EXPORT)
        print("done")
    except Exception as e:
        print("error: %s" % e)
        response = input("Continue anyway? [Y/N] ")
        if response.strip().upper() != 'Y':
            db_connection.close()
            exit()

    # Parse and insert all card records
    parse_json(db_cursor, JSON_CARDS)
    print("\nAll done!")

    # Close db connection
    db_connection.close()

if __name__ == "__main__":
    main()