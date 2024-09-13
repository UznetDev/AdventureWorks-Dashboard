using System;
using System.Collections.Generic;
using System.Text;

namespace ManagedInstanceAutomation.Shared
{
    public class DirectoryRoleTemplate
    {
        public string objectType { get; set; }
        public string objectId { get; set; }
        public object deletionTimestamp { get; set; }
        public string description { get; set; }
        public string displayName { get; set; }
    }

    public class DirectoryRoleTemplates
    {
        public DirectoryRoleTemplate[] Value { get; set; }
    }
}
