using System;
using System.Data;
using System.Data.SqlClient;

class Program
{
    static void Main()
    {
        SqlConnectionStringBuilder builder = new SqlConnectionStringBuilder();
        builder["Data Source"] = "aad-managed-demo.database.windows.net"; // replace with your server name
        builder["Initial Catalog"] = "demo"; // replace with your database name
        builder["Authentication"] = SqlAuthenticationMethod.ActiveDirectoryIntegrated;
        builder["Connect Timeout"] = 30;

        using (SqlConnection connection = new SqlConnection(builder.ConnectionString))
        {
            try
            {
                connection.Open();
                using (SqlCommand cmd = new SqlCommand(@"SELECT SUSER_SNAME()", connection))
                {
                    Console.WriteLine("You have successfully logged on as: " + (string)cmd.ExecuteScalar());
                }
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
