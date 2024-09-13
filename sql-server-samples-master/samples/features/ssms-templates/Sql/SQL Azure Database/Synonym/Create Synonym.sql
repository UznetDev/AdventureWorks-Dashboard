--==================================================
-- Create synonym template for Azure SQL Database
--==================================================
CREATE SYNONYM <synonym_name, sysname, sample_synonym>
  FOR <schema_name, sysname, Production>.<object_name, sysname, Product>
GO
