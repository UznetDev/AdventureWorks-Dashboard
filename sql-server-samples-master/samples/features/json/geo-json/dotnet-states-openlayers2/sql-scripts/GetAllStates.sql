select
	'FeatureCollection' as [type],
	(
		select
			'Feature' as [type],
			dbo.AsGeoJSON([Border]) as [geometry],
			[StateProvinceName] as [properties.name],
			[StateProvinceCode] as [properties.code],
			[Border].STArea() as [properties.area],
			[LatestRecordedPopulation] as [properties.population]
		from Application.StateProvinces
		where StateProvinceName like 'A%'
		for json path
	) as [features]
for json path, without_array_wrapper