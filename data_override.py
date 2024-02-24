import logging
import sqlite3
import pandas as pd

logging.basicConfig(level=logging.INFO)
DEBUG_MODE = False

def override_order_johana(con):
    """
    Johana Delgrado Bestelling nr 1089
    WAS: 10l bolognese, 1l carbonara
    WORDT: 9l bolognese, 1l carbonara, 1l veggie
    """
    cur = con.cursor()
    
    # update existing line item
    cur.execute(
        """
        UPDATE `order_line_items`
        SET `quantity` = 9
        WHERE `order_id` = 1089
        AND `line_item_id` = 1078;
        """
    )
    
    # add new line item (id's == -1; no tracability in system possible)
    cur.execute(
        """
        INSERT INTO `order_line_items`
        SELECT `order_id`
            , -1 AS `line_item_id`
            , `name`
            , `product_id`
            , 1 AS `quantity`
            , 0 AS total -- zetten we op 0
            , "[{'id': -1, 'key': '1l-saus', 'value': 'Veggie', 'display_key': '1L saus', 'display_value': 'Veggie'}]" AS metadata
        FROM order_line_items
        WHERE order_id = 1089
        AND line_item_id = 1078
        """
    )
    
    # persist result && close connection
    if not DEBUG_MODE:
        con.commit()
    cur.close()


def main():
    con = sqlite3.connect("./webshop-vox.db")
    logging.info("Running function override_order_johana...")
    override_order_johana(con)
    logging.info("function override_order_johana done!")
    
    logging.info("Validation res:")
    print(pd.read_sql_query("SELECT * FROM order_line_items WHERE order_id = 1089", con).head(10))


if __name__ == "__main__":
    main()