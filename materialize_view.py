import pandas as pd
import sqlite3

def materialize_view(view_name, con, table_name = None):
    table_name = view_name.lstrip("V_") if table_name is None else table_name
    
    df = pd.read_sql_query(f"SELECT * FROM {view_name}", con)
    df.to_sql(table_name, con, index=False, if_exists='replace')


if __name__ == "__main__":
    con = sqlite3.connect("./webshop-vox.db")
    materialize_view("V_SpaghettiActieOverzicht2024", con, "SpaghettiActieOverzicht2024")