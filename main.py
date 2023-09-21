import pandas as pd
import pyarrow.parquet as pq
from WooCommerceClient import WooCommerceClient


# def staging_woo_commerce(wc_client: WooCommerceClient) -> None:
#     objects_to_stage = [
#         {
#             "name": "products",
#             "select": [
#                 "id",
#                 "name",
#                 "date_created",
#                 "date_modified",
#                 "type",
#                 "status",
#                 "description",
#                 "price",
#                 "purchasable"
#             ],
#         },
#         {
#             "name": "orders",
#             "select": [
#                 "id",
#                 "status",
#                 "date_created",
#                 "date_modified",
#                 "total",
#                 "billing",
#                 "payment_method_title",
#                 "transaction_id",
#                 "date_paid",
#                 "line_items"
#             ]
#         }]
#     target_base_path = "./storage/010Raw/WooCommerce/"

#     for obj in objects_to_stage:
#         df = wc_client.get_object_by_name(obj['name'])
#         df = df[obj['select']]
#         # df.to_json(f"{target_base_path}{obj['name']}.json", orient='records')
#         df.to_csv(f"{target_base_path}{obj['name']}.csv", orient='records')


def run():
    wc_client = WooCommerceClient("./config.json")
    # staging_woo_commerce(wc_client=wc_client)
    df = wc_client.get_object_by_name("products")
    print(df.head(100))


if __name__ == "__main__":
    run()
