
-- DROP MANUALLY AND RECREATE ON CHANGE
-- DROP VIEW V_SpaghettiActie2024Prijslijst;

CREATE VIEW V_SpaghettiActie2023Prijslijst
AS
SELECT
    "Bolognese_0,3l" AS Artikel,
    6.5 AS Prijs,
    CAST(1 AS FLOAT) / 3 AS Hoeveelheid

UNION ALL

SELECT
    "Carbonara_0,3l" AS Artikel,
    6.5 AS Prijs,
    CAST(1 AS FLOAT) / 3 AS Hoeveelheid

UNION ALL

SELECT
    "Veggie_0,3l" AS Artikel,
    6.5 AS Prijs,
    CAST(1 AS FLOAT) / 3 AS Hoeveelheid

UNION ALL

SELECT
    "Bolognese_1l" AS Artikel,
    15 AS Prijs,
    CAST(1 AS FLOAT) AS Hoeveelheid

UNION ALL

SELECT
    "Carbonara_1l" AS Artikel,
    15 AS Prijs,
    CAST(1 AS FLOAT) AS Hoeveelheid

UNION ALL

SELECT
    "Veggie_1l" AS Artikel,
    15 AS Prijs,
    CAST(1 AS FLOAT) AS Hoeveelheid