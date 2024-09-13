using System;
using System.Data;
using System.Data.SqlClient;
using System.Security;

class Program
{

    static SqlCredential CreateCredential(String username)
    {
        // Prompt the user for a password and construct SqlCredential
        SecureString password = new SecureString();
        Console.WriteLine("Enter password for " + username + ": ");

        ConsoleKeyInfo nextKey = Console.ReadKey(true);

        while (nextKey.Key != ConsoleKey.Enter)
        {
            if (nextKey.Key == ConsoleKey.Backspace)
            {
                if (password.Length > 0)
                {
                    password.RemoveAt(password.Length - 1);
                    // erase the last * as well
                    Console.Write(nextKey.KeyChar);
                    Console.Write(" ");
                    Console.Write(nextKey.KeyChar);
                }
            }
            else
            {
                password.AppendChar(nextKey.KeyChar);
                Console.Write("*");
            }
            nextKey = Console.ReadKey(true);
        }

        Console.WriteLine();
        Console.WriteLine();
        password.MakeReadOnly();
        return new SqlCredential(username, password);
    }

    static void Main()
    {
        SqlConnectionStringBuilder builder = new SqlConnectionStringBuilder();
        builder["Data Source"] = "aad-managed-demo.database.windows.net"; // replace with your server name
        builder["Initial Catalog"] = "demo"; // replace with your database name
        builder["Authentication"] = SqlAuthenticationMethod.ActiveDirectoryPassword;
        builder["Connect Timeout"] = 30;
        string username = "bob@cqclinic.onmicrosoft.com"; // replace with your username

        using (SqlConnection connection = new SqlConnection(builder.ConnectionString))
        {
            try
            {
                connection.Credential = CreateCredential(username);
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
