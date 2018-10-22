#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mysql.connector as db
import requests
import sys
import threading
from time import sleep
from bs4 import BeautifulSoup
try:
    from local_settings import *
except ImportError:
    pass

"""
Updates all cards prices on the DB
"""

"""Print JSON progress count"""
def print_json_count(count):
    print("Processing cards prices... %i" % count, end='\r')
    sys.stdout.flush()

"""Return sql compatible string"""
def build_sql_string(text):
    return "'%s'" % text.replace("'", "''")

"""Update all cards' ck prices"""
def update_ck_prices(db_cursor, offset):

    # Fetch all db cards that have a ck set equiv.
    if offset == -1:
        db_cursor.execute("SELECT sc.setId, sc.uuid, sc.name, se.equiv FROM sets_cards sc INNER JOIN sets_equiv se ON se.setId = sc.setId ORDER BY sc.setId, sc.uuid")
    else:
        print("Offset: %i" % (offset * 1000))
        db_cursor.execute("SELECT sc.setId, sc.uuid, sc.name, se.equiv FROM sets_cards sc INNER JOIN sets_equiv se ON se.setId = sc.setId ORDER BY sc.setId, sc.uuid LIMIT 1000 OFFSET %i" % (offset * 1000))
    cards_result = db_cursor.fetchall()

    global_count = 0
    errors = []
    warnings = []
    queries = []
    current_proxy = 0

    # Loop thru all fetched cards
    for card in cards_result:

        global_count += 1
        print_json_count(global_count)

        # Card data
        set_id = card[0]
        card_uuid = card[1]
        card_name = card[2]
        set_equiv = card[3]

        #print("Card: %s %s" % (set_id, card_uuid))

        # Fetch current card last prices
        db_cursor.execute("SELECT nm_price, ex_price, vg_price, g_price FROM cards_prices WHERE uuid = '%s' and source = 'cardkingdom.com' ORDER BY source ASC, uuid ASC, date DESC LIMIT 1" % card_uuid)
        prices_result = db_cursor.fetchall()

        # Default zero prices
        old_nm_price = old_ex_price = old_vg_price = old_g_price = 0

        # Get current prices if there's any
        if len(prices_result) > 0:
            old_nm_price = float(prices_result[0][0])
            old_ex_price = float(prices_result[0][1])
            old_vg_price = float(prices_result[0][2])
            old_g_price = float(prices_result[0][3])

        #print("Current prices: %f %f %f %f" % (old_nm_price, old_ex_price, old_vg_price, old_g_price))

        # Build search url
        ck_url = "http://www.cardkingdom.com/catalog/view?filter%%5Bipp%%5D=60&filter%%5Bsort%%5D=most_popular&filter%%5Bsearch%%5D=mtg_advanced&filter%%5Bname%%5D=%s&filter%%5Bcategory_id%%5D=%s" % (card_name, set_equiv)

        # Try to get HTTP response
        power = 1
        while (power > 0):

            # Get HTTP result
            if USE_PROXY and len(PROXY_LIST) > 0:

                # Try current proxy or discard it
                try_proxy = True
                while try_proxy:

                    #print("Using proxy: %s" % PROXY_LIST[current_proxy])

                    # Build proxy dict.
                    proxyDict = { 
                        "http"  : "http://" + PROXY_LIST[current_proxy],
                        "https" : "https://" + PROXY_LIST[current_proxy],
                        "ftp"   : "ftp://" + PROXY_LIST[current_proxy]
                    }

                    # Try request using current proxy
                    try:
                        search_result = requests.get(ck_url, proxies=proxyDict)
                        try_proxy = False
                    except Exception as ex:
                        # Delete non-working proxy
                        del PROXY_LIST[current_proxy]
                        current_proxy = 0
                        # Switch back to regular request in case we run out of proxies
                        if len(PROXY_LIST) == 0:
                            search_result = requests.get(ck_url)
                            try_proxy = False
            else:
                # Regular request without proxy
                search_result = requests.get(ck_url)

            # Exit loop if we got HTTP 200, otherwise sleep and retry forever
            if search_result.status_code == 200:
                power = 0
            else:
                # Switch to next proxy
                if USE_PROXY and len(PROXY_LIST) > 0:
                    if current_proxy == len(PROXY_LIST) - 1:
                        current_proxy = 0
                    else:
                        current_proxy += 1
                delay = 2**power
                #print("Retrying later, we're at %s" % global_count)
                if delay > MAX_DELAY:
                    sleep(MAX_DELAY)
                else:
                    sleep(delay)
                    power += 1

        # Get content
        search_content = search_result.content.decode('utf-8')

        # BeautifulSoup html parser
        html_soup = BeautifulSoup(search_content, 'html.parser')

        # Get all card wrappers
        card_wrapper = html_soup.find_all('ul', class_ = 'addToCartByType')

        # Update prices if found any
        if len(card_wrapper) > 0:

            # Warning if got more than once result for the card
            if len(card_wrapper) > 1:
                warnings.append("More than once price for card: %s %s" % (set_id, card_uuid))
                #print("More than once price for card: %s %s" % (set_id, card_uuid))

            # Get all card prices tags
            card_prices = card_wrapper[0].find_all('span', class_ = 'stylePrice')

            # Get all clean prices
            new_nm_price = float(card_prices[0].text.strip()[1:])
            new_ex_price = float(card_prices[1].text.strip()[1:])
            new_vg_price = float(card_prices[2].text.strip()[1:])
            new_g_price = float(card_prices[3].text.strip()[1:])

            #print("New prices: %f %f %f %f" % (new_nm_price, new_ex_price, new_vg_price, new_g_price))

            # Check if there's any price difference
            if (new_nm_price != old_nm_price) or (new_ex_price != old_ex_price) or (new_vg_price != old_vg_price) or (new_nm_price != old_nm_price):
                nm_price = new_nm_price if (new_nm_price != old_nm_price) else old_nm_price
                ex_price = new_ex_price if (new_ex_price != old_ex_price) else old_ex_price
                vg_price = new_vg_price if (new_vg_price != old_vg_price) else old_vg_price
                g_price = new_g_price if (new_g_price != old_g_price) else old_g_price
                queries.append("INSERT INTO `cards_prices`(`source`, `uuid`, `nm_price`, `ex_price`, `vg_price`, `g_price`, `url`) VALUES (%s,%s,%f,%f,%f,%f,%s)" % (build_sql_string("cardkingdom.com"), build_sql_string(card_uuid), nm_price, ex_price, vg_price, g_price, build_sql_string("")))

            #print("")

        else:
            warnings.append("No prices for card: %s %s" % (set_id, card_uuid))

    # Print warnings
    if len(warnings) > 0:
        print("\nThere's been some warnings:")
        for warning in warnings:
            print(warning)

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
    print("cardkingdom-db - update_prices.py")
    print("Contribute on https://github.com/cardkingdom-uy/cardkingdom-db\n")

    # Connect to the mysql database
    db_connection = db.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        passwd=DB_PASS
    )

    # Main db cursor
    db_cursor = db_connection.cursor()

    # Get instance offset (optional)
    offset = -1
    if len(sys.argv) > 1:
        try:
            offset = float(sys.argv[1])
        except Exception as ex:
            pass

    # Update all cards' ck prices
    update_ck_prices(db_cursor, offset)

    print("\nAll done!")
    exit()

if __name__ == "__main__":
    main()