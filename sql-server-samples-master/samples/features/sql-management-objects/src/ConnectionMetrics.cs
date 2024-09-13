using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Diagnostics;
using System.Text;
using System.Threading;
using Microsoft.SqlServer.Management.Common;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace Microsoft.SqlServer.SmoSamples
{
    class ConnectionMetrics : IDisposable
    {
        public int ConnectionCount;
        public long BytesRead;
        public long BytesSent;
        public int QueryCount;
        public readonly ServerConnection ServerConnection;
        private readonly GenericSqlProxy proxy;

        public ConnectionMetrics(ServerConnection serverConnection, GenericSqlProxy proxy)
        {
            this.proxy = proxy;
            ServerConnection = serverConnection;
            proxy.OnConnect += Proxy_OnConnect;
            proxy.OnWriteHost += Proxy_OnWriteHost;
            proxy.OnWriteClient += Proxy_OnWriteClient;
            serverConnection.StatementExecuted += ServerConnection_StatementExecuted;
        }

        public void Reset()
        {
            ConnectionCount = 0;
            BytesRead = BytesSent = 0;
            QueryCount = 0;
        }

        private void ServerConnection_StatementExecuted(object sender, StatementEventArgs e)
        {
            QueryCount++;
        }

        private void Proxy_OnWriteClient(object sender, StreamWriteEventArgs e)
        {
            BytesRead += e.BytesWritten;
        }

        private void Proxy_OnWriteHost(object sender, StreamWriteEventArgs e)
        {
            BytesSent += e.BytesWritten;
        }

        private void Proxy_OnConnect(object sender, ProxyConnectionEventArgs e)
        {
            ConnectionCount++;
        }

        public void Dispose()
        {
            proxy.OnConnect -= Proxy_OnConnect;
            proxy.OnWriteHost -= Proxy_OnWriteHost;
            proxy.OnWriteClient -= Proxy_OnWriteClient;
            ServerConnection.StatementExecuted -= ServerConnection_StatementExecuted;
            ServerConnection.SqlConnectionObject.Dispose();
            proxy.Dispose();
        }

        public static ConnectionMetrics SetupMeasuredConnection(TestContext testContext, int latencyPaddingMs = 0)
        {
            var connectionString = testContext.GetConnectionString();
            var proxy = new GenericSqlProxy(connectionString);
            if (latencyPaddingMs > 0)
            {
                proxy.OnWriteClient += (o,e) => DelayWrite(latencyPaddingMs, e);
            }
            // If running these tests in a container you may need to set a specific port
            // and expose that port in the dockerfile
            var port = testContext.Properties.ContainsKey("proxyPort")
                ? Convert.ToInt32(testContext.Properties["proxyPort"])
                : 0;
            var sqlConnection = new SqlConnection(proxy.Initialize(port));
            var serverConnection = new ServerConnection(sqlConnection);
            return new ConnectionMetrics(serverConnection, proxy);
        }

        static void DelayWrite(long delay, StreamWriteEventArgs args)
        {
            Thread.Sleep(Convert.ToInt32(delay));
        }
    }


}
