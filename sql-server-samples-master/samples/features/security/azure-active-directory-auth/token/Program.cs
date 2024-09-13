using System;
using System.Data;
using System.Data.SqlClient;

namespace ClinicService
{
    class Program
    {
        static void Main()
        {
            SqlConnectionStringBuilder builder = new SqlConnectionStringBuilder();
            builder["Data Source"] = "aad-managed-demo.database.windows.net"; // replace with your server name
            builder["Initial Catalog"] = "demo"; // replace with your database name
            builder["Connect Timeout"] = 30;

            string accessToken = TokenFactory.GetAccessToken();
            if (accessToken == null)
            {
                Console.WriteLine("Fail to acuire the token to the database.");
            }
            using (SqlConnection connection = new SqlConnection(builder.ConnectionString))
            {
                try
                {
                    connection.AccessToken = accessToken;
                    connection.Open();
                    Console.WriteLine("Connected to the database");
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.Message);
                }
            }
            Console.WriteLine("Please press any key to stop");
            Console.ReadKey();
        }
    }
}