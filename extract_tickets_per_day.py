import pandas as pd
import sqlite3

CON = sqlite3.connect("./webshop-vox.db")

def get_by_query(qry: str, columns: list) -> pd.DataFrame:
    cur = CON.cursor()
    cur.execute(qry)
    df = pd.DataFrame(cur.fetchall(), columns=columns)
    cur.close()
    return df


if __name__ == "__main__":

    qry = """
        SELECT [Date]
            , COUNT(oli.line_item_id)
        FROM [dim_date] [dd]
            LEFT JOIN [orders] [o] ON DATE([o].[date_created]) = date([dd].[date])
            LEFT JOIN [order_line_items] [oli] ON [o].[id] = [oli].[order_id]
        WHERE [dd].[Date] >= '2023-09-01'
            AND [dd].[date] <= CURRENT_DATE
            AND (
                [oli].[product_id] IN (754, 752, 749, 758, 757, 756, 755)
                OR [o].[id] IS NULL
            )
        GROUP BY DATE
        ORDER BY DATE
    """

    cols = ["Datum", "AantalTickets"]

    df = get_by_query(qry, cols)
    # df.to_csv("./data-exports/tickets per dag.csv", sep="|", header=True, index=False, mode='w')
    df.to_excel("./data-exports/tickets per dag.xlsx", header=True, index=False)