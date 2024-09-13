-- =========================================
-- Create Graph Node Template
-- =========================================

IF OBJECT_ID('<schema_name, sysname, dbo>.<table_name, sysname, sample_nodetable>', 'U') IS NOT NULL
  DROP TABLE <schema_name, sysname, dbo>.<table_name, sysname, sample_nodetable>
GO

CREATE TABLE <schema_name, sysname, dbo>.<table_name, sysname, sample_nodetable>
(
    <column1_name, sysname, c1> <column1_datatype, , int> <column1_nullability, , NOT NULL>,
    <column2_name, sysname, c2> <column2_datatype, , char(10)> <column2_nullability, , NULL>,
    <column3_name, sysname, c3> <column3_datatype, , datetime> <column3_nullability, , NULL>,

    -- Unique index on $node_id is required.
    -- If no user-defined index is specified, a default index is created.
    INDEX ix_graphid UNIQUE ($node_id)
)
AS NODE
GO
