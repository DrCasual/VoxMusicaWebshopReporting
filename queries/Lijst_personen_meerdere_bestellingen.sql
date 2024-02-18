SELECT b.*
FROM (
        select Voornaam,
            Familienaam,
            EmailAdres,
            count(1) AantalBestelling
        from V_OrderOverview
        group by Voornaam,
            Familienaam,
            EmailAdres
        having AantalBestelling > 1
    ) a
    inner join V_OrderOverview b on a.Voornaam = b.Voornaam
    and a.Familienaam = b.Familienaam
    and a.EmailAdres = b.EmailAdres