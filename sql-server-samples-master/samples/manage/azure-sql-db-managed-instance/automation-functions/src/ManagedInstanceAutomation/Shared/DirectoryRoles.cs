using System;
using System.Collections.Generic;
using System.Text;

namespace ManagedInstanceAutomation.Shared
{
    public class DirectoryRole
    {
        public string ObjectType { get; set; }
        public string ObjectId { get; set; }
        public object DeletionTimestamp { get; set; }
        public string Description { get; set; }
        public string DisplayName { get; set; }
        public bool IsSystem { get; set; }
        public bool RoleDisabled { get; set; }
        public string RoleTemplateId { get; set; }
    }

    public class DirectoryRoles
    {
        public DirectoryRole[] Value { get; set; }
    }
}
