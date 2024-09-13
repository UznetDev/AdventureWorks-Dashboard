using Microsoft.AspNetCore.Http;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Threading.Tasks;

namespace ManagedInstanceAutomation.Core
{
    static class FunctionUtils
    {
        public async static Task<T> ParseRequestAsync<T>(HttpRequest req)
        {
            if (req == null)
                throw new ArgumentNullException("req");

            using (var rdr = new StreamReader(req.Body))
            {
                var requestBody = await rdr.ReadToEndAsync().ConfigureAwait(false);
                if(string.IsNullOrEmpty(requestBody))
                    throw new Exception("Request body should not be empty.");

                return JsonConvert.DeserializeObject<T>(requestBody);
            }
        }
    }
}
