SELECT [BestelNummer],
    [Familienaam],
    [Voornaam],
    CASE
        WHEN [BestelStatus] = 'processing' THEN 'JA'
        ELSE 'NEE'
    END AS [Betaald],
    [AantalTicketsBeselare] AS [AantalTickets]
FROM [V_OrderOverview]
WHERE [BestelStatus] not in ("cancelled")
    AND [AantalTicketsBeselare] > 0
ORDER BY [Familienaam]