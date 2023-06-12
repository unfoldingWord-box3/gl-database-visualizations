

WITH point_polygons AS (
  SELECT 
    pt.point_id, 
    string_agg(pg.name, ' ' ORDER BY pg.name) AS polygons
  FROM 
    challenge_points pt
  INNER JOIN challenge_polygons pg ON ST_Intersects(pt.geom, pg.geom)
  GROUP BY pt.point_id
)
SELECT polygons, string_agg(point_id::text, ', ') AS point_ids, count(*)
FROM point_polygons
GROUP BY polygons;