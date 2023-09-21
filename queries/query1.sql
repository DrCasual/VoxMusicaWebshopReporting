SELECT o.Id                             AS BestelNummer
      ,o.client_first_name              AS Voornaam
      ,o.client_last_name               AS Familienaam
      ,o.client_email                   AS EmailAdres
      ,o.client_phone                   AS TelefoonNummer
      ,o.Status                         AS BestelStatus
      ,o.payment_method_title           AS BetaalMethode 
      ,o.total                          AS Totaal
      ,oli.name                         AS Product
FROM orders AS o
LEFT JOIN order_line_items AS oli
ON o.id = oli.order_id
