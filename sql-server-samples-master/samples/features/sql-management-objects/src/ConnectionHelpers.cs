using Microsoft.SqlServer.Management.Common;
using Microsoft.SqlServer.Management.Smo;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using NUnit.Framework;
using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Diagnostics;
using System.Reflection;
using System.Text;
using Assert = NUnit.Framework.Assert;
namespace Microsoft.SqlServer.SmoSamples
{
    /// <summary>
    /// Used by test classes to initialize and retrieve a ServerConnection for use in the tests themselves
    /// </summary>
    static class ConnectionHelpers
    {

        /// <summary>
        /// Returns a ServerConnection based on the connectionString parameter defined in the runsettings file
        /// </summary>
        public static ServerConnection GetTestConnection(this VisualStudio.TestTools.UnitTesting.TestContext context, ConnectionType connectionType = ConnectionType.Default)
        {
            var connectionString = context.GetConnectionString();
            var connectionStrBuilder = new SqlConnectionStringBuilder(connectionString);
            var instanceName = connectionStrBuilder.DataSource;
            var sqlServerLogin = connectionStrBuilder.UserID;
            var password = connectionStrBuilder.Password;
            if (connectionType == ConnectionType.SqlConnection)
            {
                return new ServerConnection(new SqlConnection(connectionString));
            }
            if (connectionType == ConnectionType.Integrated)
            {
                return new ServerConnection(instanceName);
            }
            if (connectionType == ConnectionType.SqlAuth )
            {
                if (string.IsNullOrWhiteSpace(sqlServerLogin) || string.IsNullOrWhiteSpace(password))
                {
                    throw new ArgumentException("username and password values are missing from test connection string");
                }
                return new ServerConnection(instanceName, sqlServerLogin, password);
            }
            if (string.IsNullOrEmpty(sqlServerLogin))
            {
                return new ServerConnection(instanceName);
            }
            return new ServerConnection(instanceName, sqlServerLogin, password);
        }

        /// <summary>
        /// Returns a connection string based on the connectionString parameter defined in the runsettings file
        /// Placeholders may be included in the connection string if the caller has set corresponding environment variables.
        /// [hostname] -> TEST_HOSTNAME environment variable
        /// [username] -> TEST_USERNAME
        /// [password] -> TEST_PASSWORD
        /// [database] -> TEST_DATABASE
        /// </summary>
        public static string GetConnectionString(this VisualStudio.TestTools.UnitTesting.TestContext context)
        {
            var connectionString = context.Properties["connectionString"].ToString();
            Assert.That(connectionString, Is.Not.Empty, "connectionString must be set");
            connectionString = connectionString.Replace("[hostname]", Environment.GetEnvironmentVariable("TEST_HOSTNAME")).
                                                Replace("[username]", Environment.GetEnvironmentVariable("TEST_USERNAME")).
                                                Replace("[password]", Environment.GetEnvironmentVariable("TEST_PASSWORD")).
                                                Replace("[database]", Environment.GetEnvironmentVariable("TEST_DATABASE"));
            Console.WriteLine("Connection string: {0}", connectionString);
            return connectionString;
        }

        /// <summary>
        /// Returns the name of the database to use for the tests
        /// If TEST_DATABASE environment variable is set, that value is used, otherwise the
        /// testDatabase parameter from runsettings is used.
        /// </summary>
        /// <returns></returns>
        public static string GetTestDatabaseName(this VisualStudio.TestTools.UnitTesting.TestContext context)
        {
            var databaseName  = Environment.GetEnvironmentVariable("TEST_DATABASE");
            if (string.IsNullOrEmpty(databaseName))
            {
                databaseName = context.Properties["testDatabase"].ToString();
            }
            Assert.That(databaseName, Is.Not.Empty, "testDatabase must be set");
            Console.WriteLine("Test database: {0}", databaseName);
            return databaseName;
        }

        /// <summary>
        /// Returns the folder where result files should be written
        /// </summary>
        /// <param name="context"></param>
        /// <returns></returns>
        public static string GetResultsFolder(this VisualStudio.TestTools.UnitTesting.TestContext context)
        {
            var path = Environment.GetEnvironmentVariable("RESULTS_FOLDER");
            if (string.IsNullOrEmpty(path))
            {
                path = context.Properties.ContainsKey("resultsFolder") ? context.Properties["resultsFolder"].ToString() : null;
            }
            if (string.IsNullOrEmpty(path))
            {
                path = PathWrapper.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
                path = PathWrapper.Combine(path, "results");
            }
            return path;
        }

        /// <summary>
        /// creates a new database with a random name, runs the action, and drops the database
        /// </summary>
        /// <param name="context"></param>
        /// <param name="action"></param>
        /// <param name="preCreateAction"></param>
        public static void ExecuteWithDbDrop(this VisualStudio.TestTools.UnitTesting.TestContext context, Action<Database> action, Action<Database> preCreateAction = null)
        {
            var dbName = string.Format("{0}{1}", context.TestName, new Random().Next());
            var serverConnection = context.GetTestConnection();
            var server = new Management.Smo.Server(serverConnection);
            var database = new Database(server, dbName);
            preCreateAction?.Invoke(database);
            database.Create();
            try
            {
                action(database);
            }
            finally
            {
                try
                {
                    database.Drop();
                }
                catch (Exception e)
                {
                    Trace.TraceError("Unable to drop database {0}: {1}", dbName, e);
                }
            }
        }
    }

    enum ConnectionType
    {
        Default, // whatever is specified in the config
        Integrated, // integrated auth
        SqlAuth, // SQL auth
        SqlConnection // Create a SqlConnection first from the connection string
    }
}
