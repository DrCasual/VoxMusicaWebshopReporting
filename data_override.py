import logging
import sqlite3

import pandas as pd

logging.basicConfig(level=logging.INFO)
DEBUG_MODE = False


def override_order_johana(con):
    """
    Johana Delgrado Bestelling nr 1089
    Extra items erbij:
        - 1x veggie 1l
        - 3x carbonara 1l
    """
    cur = con.cursor()

    # insert order record
    cur.execute(
        """
        INSERT INTO `orders`
        SELECT `id` * -1 AS `id`
             , "on-hold" AS `status`
             , "2024-02-26T21:50:09" AS `date_created`
             , "2024-02-26T21:50:09" AS `date_modified`
             , "45.00" AS `total`
             , "cash" AS `payment_method_title`
             , NULL AS `transaction_id`
             , NULL AS `date_paid`
             , `client_first_name`
             , `client_last_name`
             , `client_email`
             , `client_phone`
        FROM orders
        WHERE id = 1089
        """
    )

    # insert order lines
    # 1x veggie 1l
    # 2x carbonara 1l
    cur.execute(
        """
        INSERT INTO `order_line_items`
        SELECT `order_id` * -1  AS `order_id`
             , -1               AS `line_item_id`
             , `name`
             , `product_id`
             , 1                AS `quantity`
             , 15               AS total
             , "[{'id': -1, 'key': '1l-saus', 'value': 'Veggie', 'display_key': '1L saus', 'display_value': 'Veggie'}]" AS metadata
        FROM order_line_items
        WHERE order_id = 1089
        AND line_item_id = 1078

        UNION ALL

        SELECT `order_id` * -1  AS `order_id`
             , -2               AS `line_item_id`
             , `name`
             , `product_id`
             , 2                AS `quantity`
             , 30               AS total
             , "[{'id': -1, 'key': '1l-saus', 'value': 'Carbonara', 'display_key': '1L saus', 'display_value': 'Carbonara'}]" AS metadata
        FROM order_line_items
        WHERE order_id = 1089
        AND line_item_id = 1078
        """
    )

    # persist result && close connection
    con.commit()
    cur.close()


def main():
    con = sqlite3.connect("./webshop-vox.db")
    logging.info("Running function override_order_johana...")
    override_order_johana(con)
    logging.info("function override_order_johana done!")

    logging.info("Validation res:")
    print(
        pd.read_sql_query(
            "SELECT * FROM order_line_items WHERE order_id = -1089", con
        ).head(10)
    )


if __name__ == "__main__":
    main()
