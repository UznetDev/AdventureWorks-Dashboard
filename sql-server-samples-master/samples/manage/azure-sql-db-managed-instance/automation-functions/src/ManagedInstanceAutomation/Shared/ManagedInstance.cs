using System;
using System.Collections.Generic;
using System.Text;

namespace ManagedInstanceAutomation.Shared
{
    public class Identity
    {
        public string PrincipalId { get; set; }
        public string Type { get; set; }
        public string TenantId { get; set; }
    }

    public class Sku
    {
        public string Name { get; set; }
        public string Tier { get; set; }
        public string Family { get; set; }
        public int Capacity { get; set; }
    }

    public class Properties
    {
        public string FullyQualifiedDomainName { get; set; }
        public string AdministratorLogin { get; set; }
        public string SubnetId { get; set; }
        public string State { get; set; }
        public string LicenseType { get; set; }
        public int VCores { get; set; }
        public int StorageSizeInGB { get; set; }
        public string Collation { get; set; }
        public string DnsZone { get; set; }
        public bool PublicDataEndpointEnabled { get; set; }
    }

    public class ManagedInstance
    {
        public Identity Identity { get; set; }
        public Sku Sku { get; set; }
        public Properties Properties { get; set; }
        public string Location { get; set; }
        public string Id { get; set; }
        public string Name { get; set; }
        public string Type { get; set; }
    }
}
