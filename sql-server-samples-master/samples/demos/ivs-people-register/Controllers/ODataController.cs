using Belgrade.SqlClient;
using Microsoft.AspNetCore.Mvc;
using SqlServerRestApi;
using System;
using System.Text;
using System.Threading.Tasks;

// For more information on enabling Web API for empty projects, visit http://go.microsoft.com/fwlink/?LinkID=397860
namespace Register.Controllers
{
    [Route("api/[controller]")]
    public class ODataController : Controller
    {
        IQueryPipe pipe = null;
        TableSpec tableSpec = new TableSpec("dbo", "People")
            .AddColumn("id", "int", isKeyColumn: true)
            .AddColumn("name","nvarchar")
            .AddColumn("surname","nvarchar")
            .AddColumn("address", "nvarchar")
            .AddColumn("town", "nvarchar");

        public string ODataMetadataUrl
        {
            get
            {
                return this.Request.Scheme + "://" + this.Request.Host + "/api/odata";
            }
        }

        public ODataController(IQueryPipe sqlQueryService)
        {
            this.pipe = sqlQueryService;
        }

        [Produces("application/json; odata.metadata=minimal")]
        [HttpGet]
        public string Get()
        {
            return ODataHandler.GetRootMetadataJsonV4(ODataMetadataUrl, new TableSpec[] { tableSpec });
        }


        [Produces("application/xml")]
        [HttpGet("$metadata")]
        public string Metadata()
        {
            return ODataHandler.GetMetadataXmlV4(new TableSpec[] { tableSpec }, "Demo.Models");
        }

        // GET api/odata/People
        [HttpGet("People")]
        public async Task People()
        {
            await this
                .OData(tableSpec, this.pipe, ODataHandler.Metadata.MINIMAL)
                .OnError(ex => Response.Body.Write(Encoding.UTF8.GetBytes(ex.Message), 0, (ex.Message).Length))
                .Get();
        }

        // GET api/odata/People/$count
        [HttpGet("People/$count")]
        public Task PeopleCount()
        {
            return this.People();
        }
    }
}