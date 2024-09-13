using Microsoft.Azure.Services.AppAuthentication;
using Newtonsoft.Json;
using Newtonsoft.Json.Serialization;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Formatting;
using System.Net.Http.Headers;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace ManagedInstanceAutomation.Core
{
    public class RestApiClient
    {
        private string ResourceType { get; set; }
        private string ApiVersion { get; set; }

        public RestApiClient(string resourceType, string apiVersion)
        {
            ResourceType = resourceType;
            ApiVersion = apiVersion;
        }

        private async Task<string> GetAccessTokenAsync()
        {
            try
            {
                var provider = new AzureServiceTokenProvider();
                return await provider.GetAccessTokenAsync(ResourceType).ConfigureAwait(false);
            }
            catch
            {
                throw new Exception("Managed Service Identity (MSI) is not assigned.");
            }
        }

        private string GetUrl(string path)
        {
            return $"{ResourceType.TrimEnd('/')}/{path.TrimStart('/')}?api-version={ApiVersion}";
        }

        public Task<T> GetJsonAsync<T>(string path)
        {
            var cts = new CancellationTokenSource();
            return GetJsonAsync<T>(path, cts.Token);
        }

        public async Task<T> GetJsonAsync<T>(string path, CancellationToken cancellationToken)
        {
            var httpClientHandler = new HttpClientHandler();
            httpClientHandler.AutomaticDecompression = System.Net.DecompressionMethods.GZip;

            var client = new HttpClient(httpClientHandler);

            var accessToken = await GetAccessTokenAsync();

            client.DefaultRequestHeaders.Add("Authorization", $"Bearer {accessToken}");

            var response = await client.GetAsync(GetUrl(path), cancellationToken).ConfigureAwait(false);
            if (response != null &&
                (response.IsSuccessStatusCode))
            {
                var responseContent = await response.Content.ReadAsStringAsync().ConfigureAwait(false);
                return JsonConvert.DeserializeObject<T>(responseContent);
            }
            else
            {
                if(response == null)
                    throw new Exception($"Call to '{path}' failed.");

                var message = response.ReasonPhrase;
                throw new Exception($"[{message}]: '{path}'.");
            }
        }
        public Task<TResult> PostJsonAsync<TResult, T>(string path, T value)
        {
            var cts = new CancellationTokenSource();
            return PostJsonAsync<TResult, T>(path, value, cts.Token);
        }

        public async Task<TResult> PostJsonAsync<TResult, T>(string path, T value, CancellationToken cancellationToken)
        {
            var httpClientHandler = new HttpClientHandler();
            httpClientHandler.AutomaticDecompression = System.Net.DecompressionMethods.GZip;

            var serializerSettings = new JsonSerializerSettings();
            serializerSettings.ContractResolver = new CamelCasePropertyNamesContractResolver();

            var client = new HttpClient(httpClientHandler);

            var accessToken = await GetAccessTokenAsync();

            client.DefaultRequestHeaders.Add("Authorization", $"Bearer {accessToken}");

            var json = JsonConvert.SerializeObject(value, serializerSettings);

            var content = new StringContent(json, UnicodeEncoding.UTF8, "application/json");

            var response = await client.PostAsync(GetUrl(path), content, cancellationToken).ConfigureAwait(false);
            if (response != null &&
                (response.IsSuccessStatusCode))
            {
                var responseContent = await response.Content.ReadAsStringAsync().ConfigureAwait(false);
                return JsonConvert.DeserializeObject<TResult>(responseContent);
            }
            else
            {
                if (response == null)
                    throw new Exception($"Call to '{path}' failed.");

                var message = response.ReasonPhrase;
                throw new Exception($"[{message}]: '{path}'.");
            }
        }

        public Task<bool> PostAsync<T>(string path, T value)
        {
            var cts = new CancellationTokenSource();
            return PostAsync<T>(path, value, cts.Token);
        }

        public async Task<bool> PostAsync<T>(string path, T value, CancellationToken cancellationToken)
        {
            var httpClientHandler = new HttpClientHandler();
            httpClientHandler.AutomaticDecompression = System.Net.DecompressionMethods.GZip;

            var serializerSettings = new JsonSerializerSettings();
            serializerSettings.ContractResolver = new CamelCasePropertyNamesContractResolver();

            var client = new HttpClient(httpClientHandler);

            var accessToken = await GetAccessTokenAsync();

            client.DefaultRequestHeaders.Add("Authorization", $"Bearer {accessToken}");

            var json = JsonConvert.SerializeObject(value, serializerSettings);

            var content = new StringContent(json, UnicodeEncoding.UTF8, "application/json");

            var response = await client.PostAsync(GetUrl(path), content, cancellationToken).ConfigureAwait(false);
            if (response != null &&
                (response.IsSuccessStatusCode))
            {
                return true;
            }
            else
            {
                if (response == null)
                    throw new Exception($"Call to '{path}' failed.");

                var message = response.ReasonPhrase;
                throw new Exception($"[{message}]: '{path}'.");
            }
        }
    }
}
