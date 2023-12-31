-- DROP VIEW V_OrderOverview;
CREATE VIEW V_OrderOverview AS
SELECT BestelNummer,
      MIN(Voornaam) AS Voornaam,
      MIN(Familienaam) AS Familienaam,
      MIN(EmailAdres) AS EmailAdres,
      MIN(TelefoonNummer) AS TelefoonNummer,
      MIN(BestelStatus) AS BestelStatus,
      MIN(BetaalMethode) AS BetaalMethode,
      MIN(DatumBesteld) AS DatumBesteld,
      MIN(DatumGewijzigd) AS DatumGewijzigd,
      MIN(DatumBetaald) AS DatumBetaald,
      MIN(Totaal) AS Totaal,
      SUM(AantalTicketsRoeselare) AS AantalTicketsRoeselare,
      SUM(AantalTicketsBeselare) AS AantalTicketsBeselare
FROM (
            SELECT o.Id AS BestelNummer,
                  o.client_first_name AS Voornaam,
                  o.client_last_name AS Familienaam,
                  o.client_email AS EmailAdres,
                  o.client_phone AS TelefoonNummer,
                  o.Status AS BestelStatus,
                  o.payment_method_title AS BetaalMethode,
                  o.date_created AS DatumBesteld,
                  o.date_paid AS DatumBetaald,
                  o.date_modified AS DatumGewijzigd,
                  o.total AS Totaal,
                  oli.quantity,
                  CASE
                        WHEN oli.product_id IN (758, 757, 756, 755) THEN oli.quantity
                        ELSE 0
                  END AS [AantalTicketsRoeselare],
                  CASE
                        WHEN oli.product_id IN (754, 752, 749) THEN oli.quantity
                        ELSE 0
                  END AS [AantalTicketsBeselare]
            FROM orders AS o
                  LEFT JOIN order_line_items AS oli ON o.id = oli.order_id
            WHERE product_id IN (754, 752, 749, 758, 757, 756, 755)
      )
GROUP BY BestelNummer