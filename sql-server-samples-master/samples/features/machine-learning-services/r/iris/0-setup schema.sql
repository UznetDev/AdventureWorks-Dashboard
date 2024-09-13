
CREATE DATABASE sqlr;
GO
USE sqlr;
GO
/* Step 1: Setup schema */
drop table if exists iris_data, iris_models;
go
create table iris_data (
		id int not null identity primary key
		, "Sepal.Length" float not null, "Sepal.Width" float not null
		, "Petal.Length" float not null, "Petal.Width" float not null
		, "Species" varchar(100) null
);
create table iris_models (
	model_name varchar(30) not null primary key,
	model varbinary(max) not null,
	native_model varbinary(max) not null
);
go

/* Step 2: Populate test data from iris dataset in R */
insert into iris_data
("Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width", "Species")
execute   sp_execute_external_script
			@language = N'R'
			, @script = N'iris_data <- iris;'
			, @input_data_1 = N''
			, @output_data_1_name = N'iris_data';
go


