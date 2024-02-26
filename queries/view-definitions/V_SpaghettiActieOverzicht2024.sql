/*DROP IF CHANGED; SEMI MANUAL; SQLITE Can't handle 2 statements in a script for some reason...*/
-- DROP VIEW IF EXISTS V_SpaghettiActieOverzicht2024; 

CREATE VIEW V_SpaghettiActieOverzicht2024
AS
SELECT 
    /*ORDER INFO*/
    MIN(o.id)                                                               AS `BestelNummer`,
    MIN(o.date_created)                                                     AS `BestelDatum`,
    MIN(o.total)                                                            AS `TotaalBedrag`,
    MIN(o.payment_method_title)                                             AS `BetaalMethode`,
    CASE WHEN MIN(o.status) IN ("processing", "completed") 
        THEN "JA" 
        ELSE "NEE" 
        END                                                                 AS `BetalingOK`,
    MIN(o.status)                                                           AS `BestelStatus`,

    /*CLIENT INFO*/
    MIN(o.client_first_name)                                                AS `Voornaam`,
    MIN(o.client_last_name)                                                 AS `Familienaam`,
    MIN(o.client_email)                                                     AS `EmailAdres`,
    MIN(o.client_phone)                                                     AS `TelefoonNummer`,

    /*ORDER CONTENT*/
    SUM(`Bolognese_0,3l`)                                                   AS `Bolognese_0,3l`,
    SUM(`Bolognese_1l`)                                                     AS `Bolognese_1l`,
    SUM(`Carbonara_0,3l`)                                                   AS `Carbonara_0,3l`,
    SUM(`Carbonara_1l`)                                                     AS `Carbonara_1l`,
    SUM(`Veggie_0,3l`)                                                      AS `Veggie_0,3l`,
    SUM(`Veggie_1l`)                                                        AS `Veggie_1l`,
    
    /*PASTA COMPUTATION*/
    -- Free pasta per 3x 0.3l and per 1x 1l
    (SUM(`Bolognese_0,3l`) + SUM(`Carbonara_0,3l`) + SUM(`Veggie_0,3l`)) / 3 + SUM(`Bolognese_1l`) + SUM(`Carbonara_1l`) + SUM(`Veggie_1l`) AS `GratisSoubryPasta`

    
FROM orders AS o 

INNER JOIN spaghetti_2024_order_line_items_formatted AS oli
ON o.id = oli.order_id

GROUP BY o.id