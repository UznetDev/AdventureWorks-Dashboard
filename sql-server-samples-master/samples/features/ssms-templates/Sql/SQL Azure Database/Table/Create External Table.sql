-- =====================================================
-- Create External Table Template for Azure SQL Database
-- =====================================================

IF OBJECT_ID('<schema_name, sysname, dbo>.<table_name, sysname, sample_external_table>', 'U') IS NOT NULL
    DROP EXTERNAL TABLE <schema_name, sysname, dbo>.<table_name, sysname, sample_external_table>
GO

CREATE EXTERNAL TABLE <schema_name, sysname, dbo>.<table_name, sysname, sample_external_table>
(
    <column1_name, sysname, c1> <column1_datatype, , int> <column1_nullability, , NOT NULL>,
    <column2_name, sysname, c2> <column2_datatype, , char(10)> <column2_nullability, , NULL>,
    <column3_name, sysname, c3> <column3_datatype, , datetime> <column3_nullability, , NULL>
)
WITH
(
    DATA_SOURCE = <data_source_name, sysname, sample_data_source>,
    -- The sharding column name is only applicable when using SHARDED distribution.
    DISTRIBUTION = <distribution, nvarchar(20), sample_distribution>(<sharding_column_name, sysname, c1>)
)
GO