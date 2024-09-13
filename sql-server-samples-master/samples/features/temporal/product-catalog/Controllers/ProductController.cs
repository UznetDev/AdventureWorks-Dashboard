using Belgrade.SqlClient;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Data.SqlClient;
using System.Threading.Tasks;

// For more information on enabling Web API for empty projects, visit http://go.microsoft.com/fwlink/?LinkID=397860

namespace ProductCatalog.Controllers
{
    [Route("api/[controller]")]
    public class ProductController : Controller
    {
        IQueryPipe sqlQuery = null;
        ICommand sqlCmd = null;
        private readonly string EMPTY_PRODUCTS_ARRAY = "{\"data\":[]}";

        public ProductController(IQueryPipe sqlQueryService, ICommand sqlCommandService)
        {
            this.sqlQuery = sqlQueryService;
            this.sqlCmd = sqlCommandService;
        }

        [HttpGet]
        [Produces("application/json")]
        public async Task Get(DateTime? date)
        {
            if (date == null)
                await this.sqlQuery.Stream("EXEC GetProducts", this.Response.Body, EMPTY_PRODUCTS_ARRAY);
            else
            {
                var cmd = new SqlCommand("GetProductsAsOf");
                cmd.CommandType = System.Data.CommandType.StoredProcedure;
                cmd.Parameters.AddWithValue("@date", date);
                await this.sqlQuery.Stream(cmd, this.Response.Body, EMPTY_PRODUCTS_ARRAY);
            }
        }

        [HttpGet("restore")]
        [Produces("application/json")]
        public void RestoreVersion(int ProductId, DateTime ValidFrom)
        {
            var cmd = new SqlCommand("RestoreProduct");
            cmd.CommandType = System.Data.CommandType.StoredProcedure;
            cmd.Parameters.AddWithValue("@productid", ProductId);
            cmd.Parameters.AddWithValue("@date", ValidFrom);
            this.sqlCmd.ExecuteNonQuery(cmd);
        }
    }
}