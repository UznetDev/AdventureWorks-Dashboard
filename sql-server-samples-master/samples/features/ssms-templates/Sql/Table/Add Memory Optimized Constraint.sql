--======================================================
-- Add Constraint to a Memory Optimized Table Template
-- Use the Specify Values for Template Parameters command (Ctrl-Shift-M) to fill in the parameter values below.
-- This template adds a constraint to a memory optimized table.
--======================================================
USE [<database_name, sysname, memory_optimized_database>]
GO

ALTER TABLE [<schema_type, , dbo>].[<table_name, sysname, memory_optimized_table>]
	ADD CONSTRAINT <contraint_name, sysname, default_constraint_name> <constraint_type, , DEFAULT> (<constraint_value, , 1.0>) FOR <constraint_column_name, sysname, column_name>
GO