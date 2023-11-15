SELECT m.miejsce_samolot_id, m.miejsce_id, b.miejsce_id, m.samolot_id, b.bilet_id
FROM (
    SELECT *
    FROM miejsce m
    WHERE m.samolot_id = (SELECT l.samolot_id FROM lot l WHERE l.lot_id = 6)
) AS m
LEFT JOIN (SELECT * FROM bilet b WHERE b.lot_id = 6) AS b 
ON m.miejsce_samolot_id = b.miejsce_id
