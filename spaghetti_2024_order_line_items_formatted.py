import pandas as pd
import sqlite3
import numpy as np 
import json


def swap_quotes_s_d(str):
    return str.replace("'", '"')


def get_portion(x: dict) -> str:
    val = x["key"]
    return "1l" if "1l" in val else "0,3l"


def format_line_items(df_order_line_items):
    index_cols = ["order_id", "total"]

    # Convert metadata to json
    df_order_line_items["metadata"] = df_order_line_items["metadata"].apply(swap_quotes_s_d)
    df_order_line_items["metadata"] = df_order_line_items["metadata"].apply(json.loads)

    # Explode metadata -> 1 record per subtype
    df_order_line_items = df_order_line_items.explode("metadata")

    # Extract Needed values
    df_order_line_items["portion"] = df_order_line_items["metadata"].apply(get_portion)
    df_order_line_items["type"] = df_order_line_items["metadata"].apply(lambda x: x["value"])

    # drop unneeded
    df_order_line_items.drop("metadata", axis=1, inplace=True) # unpacked, OG not needed
    df_order_line_items.drop("name", axis=1, inplace=True) # name not relevant in this context
    df_order_line_items.drop("line_item_id", axis=1, inplace=True) # no longer relevant due to changed granularity
    df_order_line_items.drop("product_id", axis=1, inplace=True) # no longer relevant due to changed granularity

    # pivot, group by order_id, total
    df_order_line_items = df_order_line_items.pivot_table(index =index_cols , columns = ["type", "portion"], values = "quantity", aggfunc="sum")

    # flatten multi-index into columns
    df_order_line_items.columns = list(map('_'.join, df_order_line_items.columns.values))

    # reset index
    df_order_line_items = df_order_line_items.reset_index()

    # fill na values with 0 and convert to int
    cols_to_fill = [col for col in df_order_line_items.columns if col not in index_cols]
    for col in cols_to_fill:
        df_order_line_items[col] = df_order_line_items[col].fillna(0)
        df_order_line_items[col] = df_order_line_items[col].apply(np.int64)

    # return
    return df_order_line_items


def main():
    # setup connection to sqlite
    con = sqlite3.connect("./webshop-vox.db")
    
    # read in the data
    df_order_line_items = pd.read_sql_query("SELECT * FROM order_line_items WHERE product_id IN (991, 987, 983)", con)
    
    # transform data
    df_order_line_items = format_line_items(df_order_line_items)
    
    # write data to table
    df_order_line_items.to_sql("spaghetti_2024_order_line_items_formatted", con, index=False, if_exists='replace')


if __name__ == "__main__":
    main()