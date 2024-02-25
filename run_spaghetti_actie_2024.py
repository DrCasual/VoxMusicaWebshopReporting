import logging
import sqlite3

import reload_data
import spaghetti_2024_order_line_items_formatted
import data_override

from materialize_view import materialize_view

logging.basicConfig(level=logging.INFO)
 
if __name__ == "__main__":
    con = sqlite3.connect("./webshop-vox.db")
    # materialize_view("V_SpaghettiActieOverzicht2024", con, "SpaghettiActieOverzicht2024")
    materialize_view("V_SpaghettiActie2024Prijslijst", con, "SpaghettiActie2024Prijslijst")
    
    logging.info("Extracting data from source...")
    reload_data.main()
    logging.info("Data extraction done!")
    
    logging.info("Executing data overrides")
    data_override.main()
    logging.info("Data overriding done!")
    
    logging.info("Transforming data...")
    spaghetti_2024_order_line_items_formatted.main()
    logging.info("Data transformations done!")
    
    logging.info("Materializing view")
    materialize_view("V_SpaghettiActieOverzicht2024", con, "SpaghettiActieOverzicht2024")
    logging.info("View materialized!")