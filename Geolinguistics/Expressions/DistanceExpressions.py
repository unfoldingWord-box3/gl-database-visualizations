# MaxMin


array_to_string(
    array_foreach(
        string_to_array("overlaps"),
        round(
            distance(
                $geometry,
                boundary(
                    minimal_circle(
                        geometry(
                            get_feature('Reprojected_75985cbe_2864_4e7d_841c_e322844a447e', 'major_lng_iso', @element)
                        )
                    )
                )
            ) / 1000
        )
    )
)



# Min
array_to_string(
    array_foreach(
        string_to_array("overlaps", ','),
        to_string(distance($geometry, geometry(get_feature('Lines_a51771ca_c720_41bf_a509_2d808cb3241c', 'major_lng_iso', @element)))/1000)
    )
)



# Lookups

aggregate(
    layer:= 'Country_Info',
    aggregate:='sum',
    expression:= "population",
    filter:= "language_name" = attribute(@parent, 'language_name')
)


OR


attribute(
    get_feature('Country_Language', 'iso_code', "iso_code"),
    'language_name'
)
