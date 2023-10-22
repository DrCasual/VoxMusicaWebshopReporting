SELECT DATE(date_created),
    count(1)
FROM [orders] AS [o]
    INNER JOIN [order_line_items] AS [oli] ON o.id = oli.order_id
    AND oli.product_id IN (754, 752, 749, 758, 757, 756, 755)
GROUP BY DATE(date_created)