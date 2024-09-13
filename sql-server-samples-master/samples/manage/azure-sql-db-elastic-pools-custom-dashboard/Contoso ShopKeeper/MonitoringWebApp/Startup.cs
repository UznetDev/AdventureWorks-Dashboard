using Microsoft.Owin;
using Owin;
using Owin.WebSocket.Extensions;

[assembly: OwinStartupAttribute(typeof(MonitoringWebApp.Startup))]
namespace MonitoringWebApp
{
    public partial class Startup
    {
        public void Configuration(IAppBuilder app)
        {
            app.MapWebSocketRoute<MyWebSocket>("/ws");
            ConfigureAuth(app);
        }
    }
}
