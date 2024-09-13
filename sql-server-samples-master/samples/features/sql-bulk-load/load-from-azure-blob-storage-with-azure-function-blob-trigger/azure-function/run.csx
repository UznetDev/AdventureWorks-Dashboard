using System.Configuration;
using Belgrade.SqlClient;
using Belgrade.SqlClient.SqlDb;

public static async Task Run(Stream myBlob, string name, TraceWriter log)
{
    log.Info($"C# Blob trigger function Processed blob\n Name:{name}");
    if(name.EndsWith(".dat")){
        string ConnectionString = ConfigurationManager.ConnectionStrings["azure-db-connection"].ConnectionString;
        log.Info($"Importing blob\n Name:{name}");
        string sql =
@"BULK INSERT Product
FROM '" + name + @"'
WITH (	DATA_SOURCE = 'MyAzureBlobStorage',
		FORMATFILE='product.fmt',
		FORMATFILE_DATA_SOURCE = 'MyAzureBlobStorage',
		TABLOCK); ";
        log.Info($"SQL query:{sql}");
        await (new Command(ConnectionString)).ExecuteNonQuery(sql);
    }
}