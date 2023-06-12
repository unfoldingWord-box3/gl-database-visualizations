with recursive all_polygons as (
select
ARRAY [name] as name,
ST_Multi (geom) as geom
from challenge_polygons
union
select
ARRAY [p1. name] | | p2.name as name,
ST_CollectionExtract (ST_Intersection (p1. geom, p2. geom), 3) as geom
from challenge_polygons p1
inner join all_polygons p2 on p1. name < p2. name [1] and not (ARRAY [p1.name] <@ p2. name)
),
exclusive_polygons as (
select p1.name,
case when ST_Union (p2. geom) is null then p1. geom
else ST_Difference (pl.geom, ST_Union (P2, geom))
end as geom
from all_polygons p1
left join all_polygons p2 on p1.name <> p2.name and p1.name <@ p2. name
group by p1.name, p1. geom
)
select array_to_string (polygon.name," "), count (*)
from exclusive_polygons polygon
inner join challenge_points point on St_Intersects (polygon. geom, point. geom)
group by polygon.name, polygon. geom




