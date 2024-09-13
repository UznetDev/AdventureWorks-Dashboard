using System;
using System.Collections.Generic;
using System.Text;

namespace ManagedInstanceAutomation.Shared
{
    public class DirectoryUser
    {
        public string ObjectType { get; set; }
        public string ObjectId { get; set; }
        public object DeletionTimestamp { get; set; }
        public bool AccountEnabled { get; set; }
        public object AgeGroup { get; set; }
        public object City { get; set; }
        public object CompanyName { get; set; }
        public object ConsentProvidedForMinor { get; set; }
        public object Country { get; set; }
        public object CreatedDateTime { get; set; }
        public object CreationType { get; set; }
        public object Department { get; set; }
        public bool? DirSyncEnabled { get; set; }
        public string DisplayName { get; set; }
        public object EmployeeId { get; set; }
        public object FacsimileTelephoneNumber { get; set; }
        public string GivenName { get; set; }
        public string ImmutableId { get; set; }
        public object IsCompromised { get; set; }
        public object JobTitle { get; set; }
        public DateTime? LastDirSyncTime { get; set; }
        public object LegalAgeGroupClassification { get; set; }
        public object Mail { get; set; }
        public string MailNickname { get; set; }
        public object Mobile { get; set; }
        public string OnPremisesDistinguishedName { get; set; }
        public string OnPremisesSecurityIdentifier { get; set; }
        public List<object> OtherMails { get; set; }
        public object PasswordPolicies { get; set; }
        public object PhysicalDeliveryOfficeName { get; set; }
        public object PostalCode { get; set; }
        public object PreferredLanguage { get; set; }
        public List<object> ProvisionedPlans { get; set; }
        public List<object> ProvisioningErrors { get; set; }
        public List<object> ProxyAddresses { get; set; }
        public DateTime? RefreshTokensValidFromDateTime { get; set; }
        public object ShowInAddressList { get; set; }
        public List<object> SignInNames { get; set; }
        public object SipProxyAddress { get; set; }
        public object State { get; set; }
        public object StreetAddress { get; set; }
        public string Surname { get; set; }
        public object TelephoneNumber { get; set; }
        public string UsageLocation { get; set; }
        public List<object> UserIdentities { get; set; }
        public string UserPrincipalName { get; set; }
        public object UserState { get; set; }
        public object UserStateChangedOn { get; set; }
        public string UserType { get; set; }
        public List<object> AddIns { get; set; }
        public List<string> AlternativeNames { get; set; }
        public object AppDisplayName { get; set; }
        public string AppId { get; set; }
        public object AppOwnerTenantId { get; set; }
        public bool? AppRoleAssignmentRequired { get; set; }
        public List<object> AppRoles { get; set; }
        public object ErrorUrl { get; set; }
        public object Homepage { get; set; }
        public object InformationalUrls { get; set; }
        public object LogoutUrl { get; set; }
        public List<object> Oauth2Permissions { get; set; }
        public List<object> PasswordCredentials { get; set; }
        public object PreferredTokenSigningKeyThumbprint { get; set; }
        public object PublisherName { get; set; }
        public List<object> ReplyUrls { get; set; }
        public object SamlMetadataUrl { get; set; }
        public List<string> ServicePrincipalNames { get; set; }
        public string ServicePrincipalType { get; set; }
        public object SignInAudience { get; set; }
        public List<object> Tags { get; set; }
        public object TokenEncryptionKeyId { get; set; }
    }

    public class DirectoryUsers
    {
        public DirectoryUser[] Value { get; set; }
    }
}
