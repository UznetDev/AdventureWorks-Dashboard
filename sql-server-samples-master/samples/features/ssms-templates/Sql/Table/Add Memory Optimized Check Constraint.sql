--======================================================
-- Add CHECK Constraint to a Memory Optimized Table Template
-- Use the Specify Values for Template Parameters command (Ctrl-Shift-M) to fill in the parameter values below.
-- This template adds a constraint to a memory optimized table.
--======================================================
USE [<database_name, sysname, memory_optimized_database>]
GO

ALTER TABLE [<schema_type, , dbo>].[<table_name, sysname, memory_optimized_table>]
	ADD CONSTRAINT <constraint_name, sysname, check_constraint_name>
		CHECK (<column_name, sysname, column_name> <logical_expression, , = 0>)
GO
