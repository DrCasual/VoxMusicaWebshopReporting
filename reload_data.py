import pandas as pd
import sqlite3

from datetime import datetime, timedelta
from WooCommerceClient import WooCommerceClient


con = sqlite3.connect("./webshop-vox.db")
wcc = WooCommerceClient("./config.json")

def sql(query: str) -> None:
    cur = con.cursor()
    cur.execute(query)
    cur.close()


def setup_db():
    sql("CREATE TABLE IF NOT EXISTS products(id, name, date_created, date_modified, type, status, description, price, purchasable)")
    sql("CREATE TABLE IF NOT EXISTS orders(id, status, date_created, date_modified, total, payment_method_title, transaction_id, date_paid, client_first_name, client_last_name, client_email, client_phone)")
    
    
def stage_products():
    df = wcc.get_object_by_name("products")
    df = df[["id", "name", "date_created", "date_modified", "type", "status", "description", "price", "purchasable"]]
    df.to_sql("products", con, index=False, if_exists="replace")
    
    
def stage_orders():
    df = wcc.get_object_by_name("orders")
    df_orders = df[["id", "status", "date_created", "date_modified", "total", "payment_method_title", "transaction_id", "date_paid"]]
    col_orders_client = df["billing"]
    df_orders['client_first_name'] = col_orders_client.apply(lambda x: x["first_name"]) 
    df_orders['client_last_name'] = col_orders_client.apply(lambda x: x["last_name"]) 
    df_orders['client_email'] = col_orders_client.apply(lambda x: x["email"])
    df_orders['client_phone'] = col_orders_client.apply(lambda x: x["phone"])
    df_orders.to_sql("orders", con, index=False, if_exists='replace')
    
    df_order_line_items = df[["id", "line_items"]]
    df_order_line_items["order_id"] = df_order_line_items["id"]
    df_order_line_items.drop("id", inplace=True, axis=1)
    df_order_line_items = df_order_line_items.explode("line_items")
    col_order_line_items = df_order_line_items["line_items"]
    df_order_line_items["line_item_id"] = col_order_line_items.apply(lambda x: x["id"])
    df_order_line_items["name"] = col_order_line_items.apply(lambda x: x["name"])
    df_order_line_items["product_id"] = col_order_line_items.apply(lambda x: x["product_id"])
    df_order_line_items["quantity"] = col_order_line_items.apply(lambda x: x["quantity"])
    df_order_line_items["total"] = col_order_line_items.apply(lambda x: x["total"])
    df_order_line_items["metadata"] = col_order_line_items.apply(lambda x: str(x["meta_data"]))
    df_order_line_items.drop("line_items", inplace=True, axis=1)
    df_order_line_items.to_sql("order_line_items", con, index=False, if_exists='replace')
    # df.to_sql("orders", con, index=False, if_exists="replace")


def rebuild_db():
    sql("DROP TABLE Orders;")
    sql("DROP TABLE Products;")
    setup_db()   
    
    
def create_date_dimension(year):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    date_list = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

    date_dimension = pd.DataFrame({'Date': date_list})
    date_dimension['Year'] = date_dimension['Date'].dt.year
    date_dimension['Month'] = date_dimension['Date'].dt.month
    date_dimension['Day'] = date_dimension['Date'].dt.day
    date_dimension['DayOfWeek'] = date_dimension['Date'].dt.dayofweek  # Monday is 0, Sunday is 6

    return date_dimension 

def main():
    stage_products()
    stage_orders() 
    
if __name__ == "__main__":
    main()