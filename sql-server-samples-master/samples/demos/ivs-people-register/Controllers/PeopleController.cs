using Belgrade.SqlClient;
using Microsoft.AspNetCore.Mvc;
using SqlServerRestApi;
using System.Text;
using System.Threading.Tasks;

// For more information on enabling Web API for empty projects, visit http://go.microsoft.com/fwlink/?LinkID=397860
namespace Register.Controllers
{
    [Route("api/[controller]")]
    public class PeopleController : Controller
    {
        IQueryPipe pipe = null;
        TableSpec tableSpec = new TableSpec("dbo", "People", "name,surname,address,town");

        public PeopleController(IQueryPipe sqlQueryService)
        {
            this.pipe = sqlQueryService;
        }

        /// <summary>
        /// Method that returns all data that will be processed by JQuery DataTables in client-side processing mode.
        /// </summary>
        /// <returns></returns>
        // GET api/People/All
        [HttpGet("All")]
        public async Task GetAll()
        {
            await pipe.Stream("select name, surname, address, town from people for json path, root('data')", Response.Body, @"{""data"":[]");
        }

        /// <summary>
        /// Endpoint that exposes People information using OData protocol.
        /// </summary>
        /// <returns>OData response.</returns>
        // GET api/People/odata
        [HttpGet("odata")]
        public async Task OData()
        {
            Response.ContentType = "application/json";
            await this
                    .OData(tableSpec, pipe)
                    .Process();
        }

        /// <summary>
        /// Method that process server-side processing JQuery DataTables HTTP request
        /// and returns data that should be shown.
        /// </summary>
        /// <returns></returns>
        // GET api/People
        [HttpGet]
        public async Task Get()
        {
            await this
                    .JQueryDataTables(tableSpec, pipe)
                    .OnError(ex => Response.Body.Write(Encoding.UTF8.GetBytes(ex.Message), 0, ex.Message.Length))
                    .Process();
        }
    }
}