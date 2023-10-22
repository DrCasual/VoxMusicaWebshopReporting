SELECT [Date] AS [Datum],
    COUNT(oli.line_item_id) as [TicketVerkocht]
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