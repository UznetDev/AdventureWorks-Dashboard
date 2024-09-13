using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using NLog;
using NLog.Web;
using System.IO;

namespace ProductCatalog
{
    public class Program
    {
        public static void Main(string[] args)
        {
            NLogBuilder.ConfigureNLog("nlog.config");
            try
            {
                var host = new WebHostBuilder()
                    .UseKestrel()
                    .UseContentRoot(Directory.GetCurrentDirectory())
                    .UseIISIntegration()
                    .UseNLog()
                    .UseStartup<Startup>()
                    .Build();

                host.Run();
            } finally
            {
                LogManager.Shutdown();
            }
        }
    }
}
