SELECT BestelStatus,
    count(1) AS AantalBestellingen,
    SUM(AantalTicketsBeselare) AS AantalTicketsBeselare,
    SUM(AantalTicketsRoeselare) AS AantalTicketsRoeselare,
    SUM(AantalTicketsBeselare) + SUM(AantalTicketsRoeselare) AS AantalTicketsTotaal
FROM V_OrderOverview
Group By [BestelStatus]