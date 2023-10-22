from WooCommerceClient import WooCommerceClient
import sqlite3


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
    df_order_line_items.drop("line_items", inplace=True, axis=1)
    df_order_line_items.to_sql("order_line_items", con, index=False, if_exists='replace')
    # df.to_sql("orders", con, index=False, if_exists="replace")


def rebuild_db():
    sql("DROP TABLE Orders;")
    sql("DROP TABLE Products;")
    setup_db()    
    
if __name__ == "__main__":
    stage_orders()
    # stage_products()
    # stage_orders()
    

