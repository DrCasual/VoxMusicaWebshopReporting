import logging
import sqlite3

import reload_data
import spaghetti_order_line_items_formatted

from materialize_view import materialize_view

logging.basicConfig(level=logging.INFO)
 
if __name__ == "__main__":
    con = sqlite3.connect("./webshop-vox.db")
    materialize_view("V_SpaghettiActieOverzicht2024", con, "SpaghettiActieOverzicht2024")
    
    logging.info("Extracting data from source...")
    reload_data.main()
    logging.info("Data extraction done!")
    
    logging.info("Transforming data...")
    spaghetti_order_line_items_formatted.main()
    logging.info("Data transformations done!")
    
    logging.info("Materializing view")
    materialize_view("V_SpaghettiActieOverzicht2024", con, "SpaghettiActieOverzicht2024")
    logging.info("View materialized!")