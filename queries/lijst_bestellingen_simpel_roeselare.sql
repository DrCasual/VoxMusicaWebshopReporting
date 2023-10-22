SELECT [BestelNummer],
    [Familienaam],
    [Voornaam],
    CASE
        WHEN [BestelStatus] = 'processing' THEN 'JA'
        ELSE 'NEE'
    END AS [Betaald],
    [AantalTicketsRoeselare] AS [AantalTickets]
FROM [V_OrderOverview]
WHERE [BestelStatus] not in ("cancelled")
    AND [AantalTicketsRoeselare] > 0
order by [Familienaam]