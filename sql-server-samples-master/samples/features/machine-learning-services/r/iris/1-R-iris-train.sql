USE sqlr;
GO

/* Step 1: Create procedure for training model */
create or alter procedure generate_iris_model
(@trained_model varbinary(max) OUTPUT, @native_trained_model varbinary(max) OUTPUT)
as
begin
	execute sp_execute_external_script
	  @language = N'R'
	, @script = N'
# Build decision tree model to predict species based on sepal/petal attributes
iris_model <- rxDTree(Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width, data = iris_rx_data);

# Serialize model to binary format for storage in SQL Server
trained_model <- as.raw(serialize(iris_model, connection=NULL));

# Serialize model to native binary format for scoring using PREDICT function in SQL Server
native_trained_model <- rxSerializeModel(iris_model, realtimeScoringOnly = TRUE)
'
	, @input_data_1 = N'
select "Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width", "Species"
from iris_data'
	, @input_data_1_name = N'iris_rx_data'

	, @params = N'
@trained_model varbinary(max) OUTPUT, @native_trained_model varbinary(max) OUTPUT'
	, @trained_model = @trained_model OUTPUT
	, @native_trained_model = @native_trained_model OUTPUT;
end;
go

/* Step 2: Train & store a decision tree model that will predict species of flowers */
declare @model varbinary(max), @native_model varbinary(max);
exec generate_iris_model @model OUTPUT, @native_model OUTPUT;
delete from iris_models where model_name = 'iris.dtree';
insert into iris_models (model_name, model, native_model) values('iris.dtree', @model, @native_model);
select model_name, datalength(model)/1024. as model_size_kb, datalength(native_model)/1024. as native_model_size_kb
  from iris_models;
go


