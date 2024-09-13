using Microsoft.SqlServer.Management.Smo;

namespace Microsoft.SqlServer.SmoSamples
{

using VisualStudio.TestTools.UnitTesting;
using Management.Sdk.Sfc;
using NUnit.Framework;
using Assert=NUnit.Framework.Assert;

    [TestClass]
    public class UrnSamples
    {
        public VisualStudio.TestTools.UnitTesting.TestContext TestContext {get;set;}

        [TestMethod]
        public virtual void Urn_attribute_values_require_escaping()
        {
            var connection = TestContext.GetTestConnection();
            var server = new Management.Smo.Server(connection);
            TestContext.ExecuteWithDbDrop((database) =>
            {
                var table = new Table(database, "Name'With'Quotes");
                table.Columns.Add(new Column(table, "col1", DataType.Int));
                table.Create();
                Assert.That(table.Urn.GetNameForType(Table.UrnSuffix), Is.EqualTo("Name'With'Quotes"), "Urn Value");
                Assert.Throws<FailedOperationException>(() =>
                    table = (Table) server.GetSmoObject(
                        $"Server/Database[@Name='{database.Name}']/Table[@Name='Name'With'Quotes']"));
                table = (Table)server.GetSmoObject(
                    $"Server/Database[@Name='{database.Name}']/Table[@Name='{Urn.EscapeString("Name'With'Quotes")}']");
                Assert.That(table.Name, Is.EqualTo("Name'With'Quotes"), "Table with escaped name");
            });
        }

        [TestMethod]
        public virtual void Server_Urn_has_Name_matching_InstanceName()
        {
            var connection = TestContext.GetTestConnection();
            var server = new Management.Smo.Server(connection);
            Assert.That(server.Urn.Value, Is.EqualTo($"Server[@Name='{Urn.EscapeString(connection.TrueName)}']"), "Server URN");
        }

        [TestMethod]
        public virtual void Urn_Type_is_the_last_item()
        {
            var urn = new Urn("Server[@Name='server']/Database[@Name='database']/Table[@Name='table']");
            Assert.That(urn.Type, Is.EqualTo(Table.UrnSuffix), "Urn Type");
        }
    }
}