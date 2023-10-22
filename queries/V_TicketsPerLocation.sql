SELECT Location AS Locatie,
    SUM(quantity) AS [#TicketsVerkocht]
FROM (
        select *,
CASE
                WHEN product_id IN (758, 757, 756, 755) THEN 'Roeselare'
                WHEN product_id IN (754, 752, 749) THEN 'Beselare'
                ELSE NULL
            END AS Location
        from order_line_items
    )
where Location IS NOT NULL
GROUP BY Location