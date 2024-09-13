using Belgrade.SqlClient;
using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;

// For more information on enabling Web API for empty projects, visit http://go.microsoft.com/fwlink/?LinkID=397860

namespace GeoJson.Controllers
{
    [Route("api/[controller]")]
    public class GeoController : Controller
    {
        IQueryPipe sqlQuery = null;

        string getAllStates =
            @"select
                'FeatureCollection' as [type],
                (
                    select
                        'Feature' as [type],
                        JSON_QUERY(dbo.AsGeoJSON(Border)) as [geometry],
                        StateProvinceID as [properties.id],
                        [StateProvinceName] as [properties.name],
                        [StateProvinceCode] as [properties.code],
                        [Border].STArea() / 1000000 as [properties.area],
                        [LatestRecordedPopulation] as [properties.population]
                    from Application.StateProvinces
                    for json path
                ) as [features]
            for json path, without_array_wrapper";

        string getCities =
            @"select
                'FeatureCollection' as [type],
                (
                    select
                        'Feature' as [type],
                        JSON_QUERY(dbo.AsGeoJSON(Location)) as [geometry],
                        [CityName] as [properties.name],
                        LatestRecordedPopulation as [properties.population]
                    from Application.Cities ac
                    where StateProvinceID = {0}
                    and LatestRecordedPopulation > 50000
                    for json path
                ) as [features]
            for json path, without_array_wrapper";

        public GeoController(IQueryPipe sqlQueryService)
        {
            this.sqlQuery = sqlQueryService;
        }

        public async Task Get()
        {
            await sqlQuery.Stream(getAllStates, Response.Body, "{}");
        }

        // GET /api/geo/Towns/?stateID=....
        [HttpGet("Towns")]
        public async Task Towns(int stateID)
        {
            await sqlQuery.Stream(string.Format(getCities, stateID), Response.Body, "{}");
        }
    }
}