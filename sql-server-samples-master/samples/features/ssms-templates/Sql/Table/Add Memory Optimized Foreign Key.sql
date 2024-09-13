--======================================================
-- Add Foreign Key Constraint to a Memory Optimized Table Template
-- Use the Specify Values for Template Parameters command (Ctrl-Shift-M) to fill in the parameter values below.
-- This template adds a constraint to a memory optimized table.
--======================================================
USE [<database_name, sysname, memory_optimized_database>]
GO

ALTER TABLE [<schema_type, , dbo>].[<table_name, sysname, memory_optimized_table>]
	ADD CONSTRAINT <constraint_name, sysname, fk_constraint_name>
		FOREIGN KEY([<column_name, sysname, column_name>])
		REFERENCES [<schema_type, , dbo>].[<referenced_table_name, sysname, memory_optimized_table>] ([<referenced_column_name, sysname, referenced_column_name>])
GO
