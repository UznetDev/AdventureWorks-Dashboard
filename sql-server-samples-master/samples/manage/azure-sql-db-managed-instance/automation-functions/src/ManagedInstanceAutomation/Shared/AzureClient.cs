using ManagedInstanceAutomation.Core;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace ManagedInstanceAutomation.Shared
{
    public class AzureClient
    {
        public async Task<ManagedInstance> GetManagedInstanceAsync(string id)
        {
            var restApiClient = new RestApiClient("https://management.azure.com", "2015-05-01-preview");
            return await restApiClient.GetJsonAsync<ManagedInstance>(id).ConfigureAwait(false);
        }

        public async Task<DirectoryRoles> GetAzureADRolesAsync(string tenantId)
        {
            var restApiClient = new RestApiClient("https://graph.windows.net", "1.6");
            return await restApiClient.GetJsonAsync<DirectoryRoles>($"/{tenantId}/directoryRoles").ConfigureAwait(false);
        }

        public async Task<DirectoryRoleTemplates> GetAzureADRoleTemplatesAsync(string tenantId)
        {
            var restApiClient = new RestApiClient("https://graph.windows.net", "1.6");
            return await restApiClient.GetJsonAsync<DirectoryRoleTemplates>($"/{tenantId}/directoryRoleTemplates").ConfigureAwait(false);
        }

        public async Task<DirectoryUsers> GetAzureADDirectoryRoleMembersAsync(string tenantId, string roleObjectId)
        {
            var restApiClient = new RestApiClient("https://graph.windows.net", "1.6");
            return await restApiClient.GetJsonAsync<DirectoryUsers>($"/{tenantId}/directoryRoles/{roleObjectId}/members").ConfigureAwait(false);
        }

        private class EnableAzureADRoleFunctionArguments
        {
            public string RoleTemplateId { get; set; }
        }

        public async Task<DirectoryRole> EnableAzureADRoleAsync(string tenantId, string roleTemplateId)
        {
            var restApiClient = new RestApiClient("https://graph.windows.net", "1.6");
            return await restApiClient.PostJsonAsync<DirectoryRole, EnableAzureADRoleFunctionArguments>($"/{tenantId}/directoryRoles", new EnableAzureADRoleFunctionArguments { RoleTemplateId = roleTemplateId }).ConfigureAwait(false);
        }

        private class AddAzureADDirectoryRoleMembersArguments
        {
            public string Url { get; set; }
        }

        public async Task<bool> AddAzureADDirectoryRoleMembersAsync(string tenantId, string roleObjectId, string memberId)
        {
            var restApiClient = new RestApiClient("https://graph.windows.net", "1.6");
            var url = $"https://graph.windows.net/{tenantId}/directoryObjects/{memberId}";
            return await restApiClient.PostAsync($"/{tenantId}/directoryRoles/{roleObjectId}/$links/members", new AddAzureADDirectoryRoleMembersArguments { Url = url }).ConfigureAwait(false);
        }
    }
}
