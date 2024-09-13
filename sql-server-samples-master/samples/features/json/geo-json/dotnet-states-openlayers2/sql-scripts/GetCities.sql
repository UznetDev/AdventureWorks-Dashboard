select
                'FeatureCollection' as [type],
                (
                    select
                        'Feature' as [type],
                        dbo.AsGeoJSON([Location]) as [geometry],
                        [CityName] as [properties.name],
                        ac.LatestRecordedPopulation as [properties.population]
                    from Application.Cities ac, Application.StateProvinces asp
                    where asp.StateProvinceCode = 'FL'
                        and ac.StateProvinceID = asp.StateProvinceID
                        and ac.LatestRecordedPopulation >= 20000
                    for json path
                ) as [features]
            for json path, without_array_wrapper