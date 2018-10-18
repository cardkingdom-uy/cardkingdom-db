#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mysql.connector as db
import json
import sys
import requests
import zipfile
import os
import hashlib
from collections import OrderedDict
try:
    from local_settings import *
except ImportError:
    pass

"""
JSON to MySql-database of all current MTG cards
JSON file gets automatically obtained from mtgson 4 (http://mtgjson.com/)
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

"""Check for key existence and return a date"""
def check_key_date(dict_object, key_name):
    if dict_object.get(key_name) == None:
        return build_sql_date("0000-00-00")
    else:
        return build_sql_date(dict_object[key_name])

"""Check for key existence and return 0/1"""
def check_key_bool(dict_object, key_name):
    if dict_object.get(key_name) == None:
        return 0
    else:
        if dict_object[key_name]:
            return 1
        else:
            return 0

"""Check for key existence and return its number"""
def check_key_number(dict_object, key_name):
    return 0 if dict_object.get(key_name) == None else dict_object[key_name]

"""Check for key existence or emptiness"""
def check_key_length(dict_object, key_name):
    if dict_object.get(key_name) == None:
        return False
    else:
        if len(dict_object[key_name]) > 0:
            return True
        else:
            return False

"""Print JSON progress count"""
def print_json_count(count):
    print("Processing JSON file... %i" % count, end='\r')
    sys.stdout.flush()

"""Create DB structure"""
def create_structure(db_cursor, sql_file):
    file = open(sql_file, "r", encoding="utf-8")
    parsed_sql = ""

    # clean up export
    for line in file:
        if line.strip() != "" and line[:2] != "--":
            parsed_sql += line.replace('\n', ' ')

    file.close()

    sql_queries = parsed_sql.split(";")

    # Execute all queries
    for query in sql_queries:
        db_cursor.execute(query)

    # Commit all
    db_cursor.execute("commit")

"""Parse and insert each card record"""
def parse_json(db_cursor, json_file):

    with open(json_file, "r", encoding="utf-8") as json_file:
        json_text = json_file.read()

    sets = json.loads(json_text, object_pairs_hook=OrderedDict)

    global_count = 0
    errors = []
    queries = []

    # Loop thru all sets
    for set_id in sets:

        global_count += 1
        print_json_count(global_count)

        current_set = sets[set_id]

        # Set data
        set_id_name = build_sql_string(set_id) # primary
        set_block = check_key_string(current_set, "block")
        set_code = check_key_string(current_set, "code")
        set_isonlineonly = check_key_bool(current_set, "isOnlineOnly")
        set_mtgo_code = check_key_string(current_set, "mtgoCode")
        set_name = check_key_string(current_set, "name")
        set_release_date = check_key_date(current_set, "releaseDate") # date
        set_type = check_key_string(current_set, "type")

        # Insert into 'sets' table
        queries.append("INSERT INTO `sets`(`setId`, `block`, `code`, `isOnlineOnly`, `mtgoCode`, `name`, `releaseDate`, `type`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)" % (set_id_name, set_block, set_code, set_isonlineonly, set_mtgo_code, set_name, set_release_date, set_type))
        
        card_count = 0

        # Loop thru all set's cards if there's any
        if check_key_length(current_set, "cards"):
            for card in current_set["cards"]:

                global_count += 1
                print_json_count(global_count)

                card_count += 1

                # Card data
                card_artist = check_key_string(card, "artist")
                card_bordercolor = check_key_string(card, "borderColor")
                card_convertedmanacost = check_key_number(card, "convertedManaCost") # decimal
                card_frameversion = check_key_string(card, "frameVersion")
                card_isfoilonly = check_key_bool(card, "isFoilOnly") # bool
                card_hasfoil = check_key_bool(card, "hasFoil") # bool
                card_hasnonfoil = check_key_bool(card, "hasNonFoil") # bool
                card_isonlineonly = check_key_bool(card, "isOnlineOnly") # bool
                card_isoversized = check_key_bool(card, "isOversized") # bool
                card_isreserved = check_key_bool(card, "isReserved") # bool
                card_layout = check_key_string(card, "layout")
                card_loyalty = check_key_string(card, "loyalty")
                card_manacost = check_key_string(card, "manaCost")
                card_multiverseid = check_key_number(card, "multiverseId") # integer
                card_name = check_key_string(card, "name")
                card_number = check_key_string(card, "number")
                card_originaltext = check_key_string(card, "originalText")
                card_originaltype = check_key_string(card, "originalType")
                card_power = check_key_string(card, "power")
                card_rarity = check_key_string(card, "rarity")
                card_text = check_key_string(card, "text")
                card_toughness = check_key_string(card, "toughness")
                card_type = check_key_string(card, "type")
                card_flavortext = check_key_string(card, "flavorText")
                card_watermark = check_key_string(card, "watermark")
                #card_uuid = check_key_string(card, "uuid") # primary (TODO: maybe go back to mtgjsonv4 uuid when it's fixed, there's been some duplicates; or at least keep it on another column)
                card_uuid = build_sql_string(hashlib.md5((set_id_name + card_name + str(card_count)).encode('utf-8')).hexdigest()) # primary

                # Insert into 'sets_cards' table
                queries.append("INSERT INTO `sets_cards`(`setId`, `uuid`, `artist`, `borderColor`, `convertedManaCost`, `frameVersion`, `isFoilOnly`, `hasFoil`, `hasNonFoil`, `isOnlineOnly`, `isOversized`, `isReserved`, `layout`, `loyalty`, `manaCost`, `multiverseId`, `name`, `number`, `originalText`, `originalType`, `power`, `rarity`, `text`, `toughness`, `type`, `flavorText`, `watermark`) VALUES (%s,%s,%s,%s,%f,%s,%i,%i,%i,%i,%i,%i,%s,%s,%s,%i,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (set_id_name, card_uuid, card_artist, card_bordercolor, card_convertedmanacost, card_frameversion, card_isfoilonly, card_hasfoil, card_hasnonfoil, card_isonlineonly, card_isoversized, card_isreserved, card_layout, card_loyalty, card_manacost, card_multiverseid, card_name, card_number, card_originaltext, card_originaltype, card_power, card_rarity, card_text, card_toughness, card_type, card_flavortext, card_watermark))

                # Insert into 'cards_coloridentity' table
                if check_key_length(card, "colorIdentity"):
                    for current_identity in card["colorIdentity"]:
                        queries.append("INSERT INTO `cards_coloridentity`(`identity`, `uuid`) VALUES (%s,%s)" % (build_sql_string(current_identity), card_uuid))
                
                # Insert into 'cards_colors' table
                if check_key_length(card, "colors"):
                    for current_color in card["colors"]:
                        queries.append("INSERT INTO `cards_colors`(`color`, `uuid`) VALUES (%s,%s)" % (build_sql_string(current_color), card_uuid))

                # Insert into 'cards_foreigndata' table
                if check_key_length(card, "foreignData"):
                    foreigndata_count = 0
                    for current_foreigndata in card["foreignData"]:
                        foreigndata_count += 1
                        foreigndata_language = check_key_string(current_foreigndata, "language")
                        foreigndata_flavortext = check_key_string(current_foreigndata, "flavorText")
                        foreigndata_multiverseid = check_key_number(current_foreigndata, "multiverseId")
                        foreigndata_name = check_key_string(current_foreigndata, "name")
                        foreigndata_text = check_key_string(current_foreigndata, "text")
                        foreigndata_type = check_key_string(current_foreigndata, "type")
                        queries.append("INSERT INTO `cards_foreigndata`(`foreigndata`, `uuid`, `language`, `flavorText`, `multiverseId`, `name`, `text`, `type`) VALUES (%i,%s,%s,%s,%i,%s,%s,%s)" % (foreigndata_count, card_uuid, foreigndata_language, foreigndata_flavortext, foreigndata_multiverseid, foreigndata_name, foreigndata_text, foreigndata_type))

                # Insert into 'cards_legalities' table
                if check_key_length(card, "legalities"):
                    current_legality = card["legalities"]

                    legality_1v1 = check_key_string(current_legality, "1v1")
                    legality_brawl = check_key_string(current_legality, "brawl")
                    legality_commander = check_key_string(current_legality, "commander")
                    legality_duel = check_key_string(current_legality, "duel")
                    legality_frontier = check_key_string(current_legality, "frontier")
                    legality_legacy = check_key_string(current_legality, "legacy")
                    legality_modern = check_key_string(current_legality, "modern")
                    legality_standard = check_key_string(current_legality, "standard")
                    legality_vintage = check_key_string(current_legality, "vintage")

                    queries.append("INSERT INTO `cards_legalities`(`format`, `uuid`, `legality`) VALUES (%s,%s,%s)" % (build_sql_string("1v1"), card_uuid, legality_1v1))
                    queries.append("INSERT INTO `cards_legalities`(`format`, `uuid`, `legality`) VALUES (%s,%s,%s)" % (build_sql_string("brawl"), card_uuid, legality_brawl))
                    queries.append("INSERT INTO `cards_legalities`(`format`, `uuid`, `legality`) VALUES (%s,%s,%s)" % (build_sql_string("commander"), card_uuid, legality_commander))
                    queries.append("INSERT INTO `cards_legalities`(`format`, `uuid`, `legality`) VALUES (%s,%s,%s)" % (build_sql_string("duel"), card_uuid, legality_duel))
                    queries.append("INSERT INTO `cards_legalities`(`format`, `uuid`, `legality`) VALUES (%s,%s,%s)" % (build_sql_string("frontier"), card_uuid, legality_frontier))
                    queries.append("INSERT INTO `cards_legalities`(`format`, `uuid`, `legality`) VALUES (%s,%s,%s)" % (build_sql_string("legacy"), card_uuid, legality_legacy))
                    queries.append("INSERT INTO `cards_legalities`(`format`, `uuid`, `legality`) VALUES (%s,%s,%s)" % (build_sql_string("modern"), card_uuid, legality_modern))
                    queries.append("INSERT INTO `cards_legalities`(`format`, `uuid`, `legality`) VALUES (%s,%s,%s)" % (build_sql_string("standard"), card_uuid, legality_standard))
                    queries.append("INSERT INTO `cards_legalities`(`format`, `uuid`, `legality`) VALUES (%s,%s,%s)" % (build_sql_string("vintage"), card_uuid, legality_vintage))

                # Insert into 'cards_names' table
                # TODO: Maybe remove "nameId" int(10), using it for now because found some duplicates on mtgjsonv4
                if check_key_length(card, "names"):
                    names_count = 0
                    for current_name in card["names"]:
                        names_count += 1
                        #queries.append("INSERT INTO `cards_names`(`name`, `uuid`) VALUES (%s,%s)" % (build_sql_string(current_name), card_uuid))
                        queries.append("INSERT INTO `cards_names`(`nameId`, `name`, `uuid`) VALUES (%i,%s,%s)" % (names_count, build_sql_string(current_name), card_uuid))

                # Insert into 'cards_printings' table
                if check_key_length(card, "printings"):
                    for current_printing in card["printings"]:
                        queries.append("INSERT INTO `cards_printings`(`printing`, `uuid`) VALUES (%s,%s)" % (build_sql_string(current_printing), card_uuid))

                # Insert into 'cards_rulings' table
                if check_key_length(card, "rulings"):
                    ruling_count = 0
                    for current_ruling in card["rulings"]:
                        ruling_count += 1
                        ruling_date = check_key_date(current_ruling, "date")
                        ruling_text = check_key_string(current_ruling, "text")
                        queries.append("INSERT INTO `cards_rulings`(`ruling`, `uuid`, `date`, `text`) VALUES (%i,%s,%s,%s)" % (ruling_count, card_uuid, ruling_date, ruling_text))

                # Insert into 'cards_subtypes' table
                if check_key_length(card, "subtypes"):
                    for current_subtype in card["subtypes"]:
                        queries.append("INSERT INTO `cards_subtypes`(`subtype`, `uuid`) VALUES (%s,%s)" % (build_sql_string(current_subtype), card_uuid))

                # Insert into 'cards_supertypes' table
                if check_key_length(card, "supertypes"):
                    for current_supertypes in card["supertypes"]:
                        queries.append("INSERT INTO `cards_supertypes`(`supertype`, `uuid`) VALUES (%s,%s)" % (build_sql_string(current_supertypes), card_uuid))

                # Insert into 'cards_types' table
                if check_key_length(card, "types"):
                    for current_type in card["types"]:
                        queries.append("INSERT INTO `cards_types`(`type`, `uuid`) VALUES (%s,%s)" % (build_sql_string(current_type), card_uuid))

        token_count = 0

        # Loop thru all set's tokens if there's any
        if check_key_length(current_set, "tokens"):
            for token in current_set["tokens"]:

                global_count += 1
                print_json_count(global_count)

                token_count += 1

                # Token data
                token_artist = check_key_string(card, "artist")
                token_bordercolor = check_key_string(card, "borderColor")
                token_loyalty = check_key_string(card, "loyalty")
                token_name = check_key_string(card, "name")
                token_number = check_key_string(card, "number")
                token_power = check_key_string(card, "power")
                token_text = check_key_string(card, "text")
                token_toughness = check_key_string(card, "toughness")
                token_type = check_key_string(card, "type")
                token_watermark = check_key_string(card, "watermark")                
                #token_uuid = check_key_string(card, "uuid") # primary (TODO: maybe go back to mtgjsonv4 uuid when it's fixed, there's been some duplicates; or at least keep it on another column)
                token_uuid = build_sql_string(hashlib.md5((set_id_name + token_name + str(token_count)).encode('utf-8')).hexdigest()) # primary

                # Insert into 'sets_cards' table
                queries.append("INSERT INTO `sets_tokens`(`setId`, `uuid`, `artist`, `borderColor`, `loyalty`, `name`, `number`, `power`, `text`, `toughness`, `type`, `watermark`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (set_id_name, token_uuid, token_artist, token_bordercolor, token_loyalty, token_name, token_number, token_power, token_text, token_toughness, token_type, token_watermark))

                # Insert into 'tokens_coloridentity' table
                if check_key_length(token, "colorIdentity"):
                    for current_identity in token["colorIdentity"]:
                        queries.append("INSERT INTO `tokens_coloridentity`(`identity`, `uuid`) VALUES (%s,%s)" % (build_sql_string(current_identity), token_uuid))

                # Insert into 'tokens_colors' table
                if check_key_length(token, "colors"):
                    for current_color in token["colors"]:
                        queries.append("INSERT INTO `tokens_colors`(`color`, `uuid`) VALUES (%s,%s)" % (build_sql_string(current_color), token_uuid))

                # Insert into 'tokens_reverserelated' table
                # TODO: Maybe remove "reverserelated" int(10), using it for now because found some duplicates on mtgjsonv4
                if check_key_length(token, "reverseId"):
                    reverserelated_count = 0
                    for current_name in token["reverseRelated"]:
                        reverserelated_count += 1
                        queries.append("INSERT INTO `tokens_reverserelated`(`reverseId`, `uuid`, `name`) VALUES (%i,%s,%s)" % (reverserelated_count, token_uuid, build_sql_string(current_name)))

    print("\nAbout to execute all %s SQL queries" % str(len(queries)))

    query_count = 0

    # Execute all queries
    for query in queries:
        query_count += 1
        try:
            print("Processing SQL queries... %i" % query_count, end='\r')
            sys.stdout.flush()
            db_cursor.execute(query)
        except Exception as e:
            errors.append(e)

    # Print errors
    if len(errors) > 0:
        print("\nThere's been some errors:")
        for error in errors:
            print(error)

    # Commit all
    db_cursor.execute("commit")

def main():

    # Show welcome message
    print("cardkingdom-db - generate.py")
    print("Contribute on https://github.com/cardkingdom-uy/cardkingdom-db\n")

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

    # Download cards.json
    if not USE_LOCAL_JSON:
        print("Downloading JSON zip file from \"%s\"... " % JSON_URL, end='')
        remote_file = requests.get(JSON_URL)
        local_file = open("tmp.zip", "wb")
        local_file.write(remote_file.content)
        local_file.close()
        # Remove if exists before extraction
        if os.path.exists(JSON_FILE):
            os.remove(JSON_FILE)
        # Extract file
        if os.path.exists("AllSets.json"):
            os.remove("AllSets.json")
        zip_file = zipfile.ZipFile("tmp.zip", "r")
        zip_file.extractall()
        zip_file.close()
        # Rename extracted file
        if JSON_FILE != "AllSets.json":
            os.rename("AllSets.json", JSON_FILE)
        # Clean up
        os.remove("tmp.zip")
        print("done")

    # Parse and insert all set/card records
    parse_json(db_cursor, JSON_FILE)

    # Remove JSON file
    if not USE_LOCAL_JSON:
        os.remove(JSON_FILE)

    # Close db connection
    db_connection.close()

    # Exit
    print("\nAll done!")
    exit()

if __name__ == "__main__":
    main()