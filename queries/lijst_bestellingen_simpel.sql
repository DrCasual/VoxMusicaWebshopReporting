SELECT [BestelNummer],
    [Familienaam],
    [Voornaam],
CASE
        WHEN [BestelStatus] = 'processing' THEN 'JA'
        ELSE 'NEE'
    END AS [Betaald],
    [Totaal],
    [AantalTicketsBeselare],
    [AantalTicketsRoeselare]
FROM [V_OrderOverview]
WHERE [BestelStatus] not in ("cancelled")
order by Familienaam